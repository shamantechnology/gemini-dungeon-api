# Gemini Dungeon API

## Setup

Create a data folder in the root folder and save your purchased copy of the 5E players handbook and dungeon masters guide in text format into that folder

## Environment

You should create a virtualenv with the required dependencies by running
```
make virtualenv
```

When a new requirement is needed you should add it to `unpinned_requirements.txt` and run
```
make update-requirements-txt
make virtualenv
```
this ensures that all requirements are pinned and work together for ensuring reproducibility
