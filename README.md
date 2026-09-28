# Media Finder

A cross-platform desktop application to find out where digital books, movies, shows and music is available. Queries get distributed across relevant free/public-domain and commercial subscription repositories, while a rule-based heuristic engine estimates public domain availability.

---

## Overview

A search for digital media often involves muddling through countless websites and different streaming platforms. Media Finder is a graphical utility written in python and tkinter, which aggregates search queries to major open-access repositories and commercial providers while estimating the likelihood of public domain availability using a rule-based heuristic engine.

When a search is made and a media category is picked, Media Finder:

1. Constructs direct search links for each major open-access repository and commercial provider

2. Analyzes the query using a heuristic analyzer to determine the likelihood of being in the public domain

3. Keeps a persistent history of recent searches for easy re-use

---

## Features

### Multi-Category Cross-Media Search

Book search includes:

- Project Gutenberg

- Internet Archive

- Open Library

- Standard Ebooks

- LibriVox

- Amazon Kindle

- Audible

- Google Play Books

- Kobo

Movie search includes:

- Tubi

- YouTube

- Internet Archive

- JustWatch

- Pluto TV

- Netflix

- Prime Video

- Disney+

- Apple TV

- Google TV

TV Show search includes:

- Tubi

- YouTube

- JustWatch

- Pluto TV

- Netflix

- Prime Video

- Max

- Hulu

Music search includes:

- SoundCloud

- Bandcamp

- Internet Archive

- Jamendo

- Free Music Archive

- Spotify

- Apple Music

- YouTube Music

- Tidal

### Intelligent Availability Heuristic Engine

- Uses regex year detection for public domain cutoff years (US copyright law, pre-1928) and modern (post-2018) works

- Heuristics include domain specific patterns for recognizing public domain works by classical authors (Shakespeare, Dickens, Austen, Twain, Poe, Doyle, Tolstoy, Homer) and composers (Mozart, Beethoven, Bach, Chopin, Vivaldi, Tchaikovsky)

- Detects audiobooks, archival content, live performances, remixes and bootlegs

- Two progress bars showing confidence levels for free vs. paid availability

### Two-Sided Source Organization

Sources are divided into two groups: Those that host free/public-domain content, and those that require subscription or payment.

### Native Link Dispatch

The link gets opened in the default browser by encoding the search parameters directly into the query.

### Persistent Search History

The most recent 25 unique search queries are stored in a json file called `search_history.json`, and sorted according to an MRU (Most Recently Used) algorithm.

### Modern Dark UI

Customized ttk themed buttons and widgets to provide a modern, accessible UI with good color contrast.

---

## Technologies

- Python 3.8+

- Tkinter + `ttk`

Some libraries used:

- `urllib.parse`

- `webbrowser`

- `json`

- `re`

- `pathlib`

Testing:

- `unittest`

Hosting:

- Git + GitHub

---

## Installing

### Requirements

- Python 3.8 or higher

- Tkinter (comes bundled with the official python Windows/macOS installers). For Linux (Ubuntu/Debian):

```bash

sudo apt-get install python3-tk
