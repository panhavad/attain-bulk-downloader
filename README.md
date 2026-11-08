# Attain Bulk Downloader

![Language](https://img.shields.io/github/languages/top/panhavad/attain-bulk-downloader) ![Last commit](https://img.shields.io/github/last-commit/panhavad/attain-bulk-downloader) [![Release](https://img.shields.io/github/v/release/panhavad/attain-bulk-downloader?include_prereleases)](https://github.com/panhavad/attain-bulk-downloader/releases/latest)

A Python script to **back up the lessons of a Teachable course you are enrolled in** - lesson videos (Wistia) and PDF handouts - into clean, named folders for offline study. Use it only for content you have access rights to.

![System snapshot](docs/snapshot.svg)

## Features

- Walks through course lectures from a start lesson
- Resolves Wistia video and PDF asset URLs
- Safe file / folder naming
- Uses your own logged-in session cookie

## How it works

```mermaid
flowchart LR
    U["Course id + start lesson"] --> L["Lecture page"]
    L -->|"BeautifulSoup"| A["Find assets"]
    A --> V["Wistia JSON -> video URL"]
    A --> P["PDF URL"]
    V --> D["wget download"]
    P --> D
    D --> N["Next lecture"] --> L
```

## Getting started

```bash
pip install -r requirement.txt
python main.py
```

## Download

Grab the packaged source from the [latest release](https://github.com/panhavad/attain-bulk-downloader/releases/latest).

## Tech stack

- Python
- requests
- BeautifulSoup
- wget

## Project structure

```text
attain-bulk-downloader/
├── docs/
├── .gitignore
├── main.py
├── README.md
└── requirement.txt
```
