#
#Adapted from tinyvox/data_preparation/talkbank_audio_scrapper.py. Crawls only the corpus folder you name,
#downloads only audio files, and with --list it counts files and total size.
#

import argparse
import asyncio
import getpass
import os
import re
import sys
from urllib.parse import urljoin, urlparse, unquote

import aiohttp
from bs4 import BeautifulSoup

#CHANGE THIS IF YOU WANT TO SAVE FILES SOMEWHERE ELSE
DOWNLOAD_DIR = "/mnt/na1/eecs/srdesign/csar/data/raw"

LOGIN_URL = "https://sla2.talkbank.org/logInUser"
MEDIA_ROOT = "https://media.talkbank.org"
AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".aac", ".wma", ".flac", ".ogg"}
MAX_CONCURRENT = 4


def human(n):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


async def login(session):
    email = input("TalkBank email: ").strip()
    password = getpass.getpass("TalkBank password: ")
    async with session.post(LOGIN_URL, json={"email": email, "pswd": password}) as resp:
        cookie = resp.cookies.get("talkbank")
        if not resp.ok or cookie is None:
            sys.exit(f"Login failed (HTTP {resp.status}). Check your email/password.")
    del password
    return cookie.value


def clean_url(url):
    """Drop the query string and collapse repeated slashes (TalkBank lists some folders as 'X//')."""
    u = urlparse(url.split("?")[0])
    return u._replace(path=re.sub(r"/{2,}", "/", u.path)).geturl()


async def crawl(session, cookies, url, prefix, seen):
    """Return all audio file URLs under `url`, never leaving `prefix`."""
    if url in seen:
        return []
    seen.add(url)
    print(f"  scanning {unquote(urlparse(url).path)}")

    async with session.get(url, headers=cookies) as resp:
        if resp.status != 200:
            print(f"  ! HTTP {resp.status} for {url}")
            return []
        html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")
    files, subdirs = [], []
    for a in soup.find_all("a", href=True):
        full = clean_url(urljoin(url, a["href"].replace(":443", "")))
        if not full.startswith(prefix) or full.rstrip("/") == url.rstrip("/"):
            continue  # skip parent links and anything outside the corpus
        ext = os.path.splitext(urlparse(full).path)[1].lower()
        row = a.find_parent("tr")
        is_dir = full.endswith("/") or "📁" in (row.text if row else a.text) or ext == ""
        if is_dir:
            subdirs.append(full.rstrip("/") + "/")
        elif ext in AUDIO_EXTENSIONS:
            files.append(full)

    if not files and not subdirs and len(seen) == 1:
        print("  ! No folders or audio links on this page. First part of what the server returned:")
        print("    " + html[:800].replace("\n", "\n    "))

    for sub in subdirs:
        files.extend(await crawl(session, cookies, sub, prefix, seen))
    return files


def local_path(url, out_dir, corpus_url):
    """OUT/<CorpusName>/<path inside the corpus>, e.g. data/raw/Cougar/<child>/<file>.wav"""
    corpus_root = unquote(urlparse(corpus_url).path)
    corpus_name = os.path.basename(corpus_root.rstrip("/"))
    rel = unquote(urlparse(url).path)[len(corpus_root):]
    return os.path.join(out_dir, corpus_name, rel)


class Progress:
    """Counts finished files so the script can print 'n/total' as it goes."""
    def __init__(self, total):
        self.total, self.done, self.bytes = total, 0, 0

    def step(self, nbytes=0):
        self.done += 1
        self.bytes += nbytes
        return f"[{self.done}/{self.total}]"


async def file_size(session, cookies, url, sem, progress):
    size = 0
    async with sem:
        try:
            async with session.head(url + "?f=save", headers=cookies, allow_redirects=True,
                                    timeout=aiohttp.ClientTimeout(total=60)) as resp:
                size = int(resp.headers.get("Content-Length", 0))
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
            size = 0
    tag = progress.step(size)
    print(f"\r  checked {tag}  running total {human(progress.bytes)}   ", end="", flush=True)
    return size


async def download(session, cookies, url, dest, sem, progress, retries=3):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        print(f"  {progress.step()} skip {os.path.basename(dest)} (already here)")
        return "skip"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    part = dest + ".part"
    async with sem:
        for attempt in range(1, retries + 1):
            try:
                async with session.get(url + "?f=save", headers=cookies) as resp:
                    if resp.status != 200:
                        raise aiohttp.ClientError(f"HTTP {resp.status}")
                    if "text/html" in resp.headers.get("Content-Type", ""):
                        raise aiohttp.ClientError("got an HTML page (login expired?)")
                    with open(part, "wb") as f:
                        async for chunk in resp.content.iter_chunked(1 << 20):
                            f.write(chunk)
                os.replace(part, dest)
                size = os.path.getsize(dest)
                print(f"  {progress.step(size)} ok   {os.path.basename(dest)} "
                      f"({human(size)}, {human(progress.bytes)} so far)")
                return "ok"
            except (aiohttp.ClientError, asyncio.TimeoutError, OSError) as e:
                if os.path.exists(part):
                    os.remove(part)
                if attempt == retries:
                    print(f"  {progress.step()} FAILED {dest}: {e}")
                    return "fail"
                await asyncio.sleep(5 * attempt)


async def main():
    p = argparse.ArgumentParser(description="Download the audio files of one TalkBank corpus.")
    p.add_argument("database", choices=["homebank", "childes", "phon"])
    p.add_argument("corpus_path", help="e.g. Password/Cougar (path after the database name)")
    p.add_argument("--list", action="store_true", help="only count files and total size")
    args = p.parse_args()

    os.umask(0o007)  # new files readable/writable by owner + group only
    media_url = f"{MEDIA_ROOT}/{args.database}/{args.corpus_path.strip('/')}/"

    timeout = aiohttp.ClientTimeout(total=None, sock_read=300)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # The media server requires a login for every corpus, including Public ones.
        # The cookie is sent as a raw header, like the original TinyVox script does.
        cookies = {"Cookie": f"talkbank={await login(session)}"}
        print(f"Logged in. Scanning {media_url}")

        files = sorted(set(await crawl(session, cookies, media_url, media_url, set())))
        if not files:
            sys.exit("No audio files found. Check the corpus path (and that your account can access it).")
        print(f"\nFound {len(files)} audio files.")

        sem = asyncio.Semaphore(MAX_CONCURRENT)
        if args.list:
            progress = Progress(len(files))
            sizes = await asyncio.gather(*(file_size(session, cookies, f, sem, progress) for f in files))
            print(f"\nTotal size: {human(sum(sizes))}")
            if 0 in sizes:
                print(f"({sizes.count(0)} files didn't report a size, so the real total may be larger.)")
            return

        out = DOWNLOAD_DIR
        os.makedirs(out, exist_ok=True)
        if not os.access(out, os.W_OK):
            sys.exit(f"Can't write to {out}.")
        if input(f"Download {len(files)} files to {out}? [y/N]: ").strip().lower() != "y":
            sys.exit("Cancelled.")

        progress = Progress(len(files))
        results = await asyncio.gather(*(
            download(session, cookies, f, local_path(f, out, media_url), sem, progress) for f in files
        ))
        print(f"\nDone: {results.count('ok')} downloaded, "
              f"{results.count('skip')} already present, {results.count('fail')} failed.")
        if results.count("fail"):
            print("Re-run the same command to retry failed files.")


if __name__ == "__main__":
    asyncio.run(main())