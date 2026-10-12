# Sprint 1 Report (September 1st to October 11th)

## YouTube link of Sprint * Video (Make this video unlisted)
https://youtu.be/0ZN6XFm5m60?is=nW1GyMijwwuX9n-D 

## What's New (User Facing)
 * Completed initial requirements gathering with the client and identified the main goals and expected functionality of the speaker segmentation system.
 * Created user stories describing how child speech researchers will interact with the system.
 * Developed use cases to describe the expected system behavior and researcher workflows.
 * Created UML diagrams to visualize the system structure and interactions.
 * Researched existing pretrained speaker segmentation models and potential technologies for the project.
 * Identified Python and other frameworks as the primary technologies for development.
 * Established initial plans for audio processing, speaker segmentation, model evaluation, and future fine tuning.
 * Set up the initial project organization and development planning for future implementation.

## Work Summary (Developer Facing)
During Sprint 1, our team focused primarily on requirements gathering, project planning, documentation, and technical research rather than implementing/fine-tuning the system. We communicated with our client, Joe Dumoulin, to better understand the research problem and the limitations of existing speaker segmentation models when processing child speech. We used this information to identify the system's expected functionality and create user stories, use cases, and UML diagrams. We also researched existing pretrained speaker segmentation models he provided to us and analyzed the Python based machine learning that could support the project. One of the main challenges was understanding the differences between existing speaker segmentation approaches and determining which technologies would be realistic for our project. Through research, team discussions, and communication with the client, we established a clearer technical direction and identified the main areas that will need to be implemented and tested during future sprints.

## Unfinished Work
The following issues were not completed during Sprint 1 and have been moved into the appropriate stages of the Kanban board for continued work:

* Design a Fine Tuning Algorithm is in Backlog because the team has not yet finalized the approach for fine tuning the pretrained models.
* Data Cleansing is in Backlog because the data preparation requirements still need to be defined and implemented.
* Data Conversion is in Backlog because the required data format and conversion process still need to be completed.
* Data Ingestion is Ready and assigned to Rylan and Jose. The issue is ready for implementation but has not yet been started.
* PyTorch is Ready and assigned to Marissa and Quan. The issue is ready to be picked up but has not yet been started.
* Get Server Space is currently In Progress and assigned to Rylan. Work is actively being done to obtain the required server resources.

## Completed Issues/User Stories

Here are the issues completed during Sprint 1:

* [Requirement Gathering](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/7)
* [Access to member only corpora](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/2)

Both completed issues were assigned to all four team members.

 ## Incomplete Issues/User Stories

Here are the issues we worked on or prepared but did not complete in this sprint:

* [Get Server Space](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/8)
We are still working on obtaining the server space needed to store and process the project's audio data.
* [PyTorch](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/6)
The issue is ready to be picked up, but the PyTorch development environment has not yet been completed.
* [Data Ingestion](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/1)
The issue is ready to be picked up, but implementation has not yet started.
* [Data Conversion](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/5)
The issue remains in the backlog because the data conversion process has not yet been implemented.
* [Data Cleansing](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/3)
The issue remains in the backlog because the data cleansing process has not yet been implemented.
* [Design a Fine-Tuning Algorithm](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/4)
The issue remains in the backlog while the team determines an appropriate fine tuning approach.

## Code Files for Review
No major production code was completed during Sprint 1. The sprint focused primarily on requirements, data access, project organization, and technical preparation.

The main work completed this sprint is represented by the GitHub issues and Kanban board rather than production source code.
 
## Retrospective Summary
Here's what went well:
* We successfully completed the requirements gathering process with all four team members contributing.
* We obtained access to the member only corpora needed for the project.
* We identified the major technical tasks required for future implementation.
* We organized the technical work into separate GitHub issues.
* We established ownership for issues that are ready to be implemented.
* We created a Kanban workflow to track the progress of project tasks.
 
Here's what we'd like to improve:
* Begin implementation sooner after requirements are established.
* Improve estimates for the amount of time required for infrastructure and data preparation tasks.
* Define clearer acceptance criteria and estimates for upcoming issues.
* Continue improving our understanding of the research dataset before implementing the data pipeline.
* Coordinate dependencies between server setup, PyTorch, data ingestion, conversion, and cleansing.
  
Here are changes we plan to implement in the next sprint:
* Complete the server space setup.
* Set up the PyTorch development environment.
* Begin implementing data ingestion.
* Begin converting the research data into the required format.
* Develop the initial data cleansing process.
* Continue researching and designing the fine tuning algorithm.
* Begin testing the development environment with available research data.
