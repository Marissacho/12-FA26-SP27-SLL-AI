#
#reuses a lot of code from talkbank_audio_scrapper.py, but downloads the transcripts instead of the audio.
#

import argparse
import asyncio
import os
import sys
import zipfile

import aiohttp

from talkbank_audio_scrapper import DOWNLOAD_DIR, human, login

DATA_ROOT = "https://talkbank.org/data"


def safe_extract(zip_path, dest):
    """Unzip, refusing any entry that would land outside `dest` (e.g. '../../x')."""
    dest = os.path.realpath(dest)
    with zipfile.ZipFile(zip_path) as zf:
        for member in zf.infolist():
            target = os.path.realpath(os.path.join(dest, member.filename))
            if os.path.commonpath([target, dest]) != dest:
                sys.exit(f"Refusing to extract {member.filename!r}: it points outside {dest}.")
        zf.extractall(dest)
        return [m for m in zf.namelist() if not m.endswith("/")]


async def main():
    p = argparse.ArgumentParser(description="Download and unzip one TalkBank corpus's transcripts.")
    p.add_argument("database", choices=["homebank", "childes", "phon"])
    p.add_argument("corpus_path", help="e.g. Password/Cougar (same as the audio script)")
    p.add_argument("--list", action="store_true", help="only show the zip's size")
    p.add_argument("--delete-zip", action="store_true", help="remove the zip after unzipping")
    args = p.parse_args()

    os.umask(0o007)  # new files readable/writable by owner + group only
    corpus = args.corpus_path.strip("/")
    corpus_name = os.path.basename(corpus)
    url = f"{DATA_ROOT}/{args.database}/{corpus}?f=zip"

    out_dir = os.path.join(DOWNLOAD_DIR, corpus_name, "transcripts")
    zip_path = os.path.join(out_dir, f"{corpus_name}.zip")
    part = zip_path + ".part"

    timeout = aiohttp.ClientTimeout(total=None, sock_read=300)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        headers = {"Cookie": f"talkbank={await login(session)}"}
        print(f"Logged in. Transcript zip: {url}")

        if args.list:
            async with session.head(url, headers=headers, allow_redirects=True) as resp:
                ctype = resp.headers.get("Content-Type", "unknown")
                size = int(resp.headers.get("Content-Length", 0) or 0)
            if "text/html" in ctype:
                sys.exit("Got a web page instead of a zip (login not accepted, or wrong corpus path).")
            print(f"Type: {ctype}   Size: {human(size) if size else 'not reported'}")
            return

        if os.path.exists(zip_path) and zipfile.is_zipfile(zip_path):
            print(f"Already downloaded: {zip_path}")
        else:
            os.makedirs(out_dir, exist_ok=True)
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    sys.exit(f"Download failed: HTTP {resp.status}")
                if "text/html" in resp.headers.get("Content-Type", ""):
                    sys.exit("Got a web page instead of a zip (login not accepted, or wrong corpus path).")
                done = 0
                with open(part, "wb") as f:
                    async for chunk in resp.content.iter_chunked(1 << 20):
                        f.write(chunk)
                        done += len(chunk)
                        print(f"\r  downloaded {human(done)}   ", end="", flush=True)
            print()
            if not zipfile.is_zipfile(part):
                os.remove(part)
                sys.exit("The download isn't a valid zip file. Nothing was saved.")
            os.replace(part, zip_path)
            print(f"Saved {zip_path} ({human(os.path.getsize(zip_path))})")

    files = safe_extract(zip_path, out_dir)
    cha = sum(f.lower().endswith(".cha") for f in files)
    its = sum(f.lower().endswith(".its") for f in files)
    print(f"Unzipped {len(files)} files into {out_dir} ({cha} .cha, {its} .its)")

    if args.delete_zip:
        os.remove(zip_path)
        print("Deleted the zip.")


if __name__ == "__main__":
    asyncio.run(main())