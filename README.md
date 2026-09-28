# Media Finder

A cross-platform desktop application designed to discover where digital books, movies, shows, and music are accessible. The application aggregates search queries across curated free/public-domain repositories and commercial subscription platforms while using a rule-based heuristic engine to estimate public domain availability.

---

## Overview

Finding digital media often requires jumping between disparate websites and streaming platforms. Media Finder streamlines this discovery process with a centralized graphical interface built in Python and Tkinter.

When a query is entered and a media category is selected, the application:
1. Dynamically constructs direct search links for major open-access repositories and commercial providers.
2. Evaluates the search terms through a heuristic analyzer to predict whether the content is likely in the public domain or behind a paywall.
3. Maintains a local, persistent history of recent searches for quick re-execution.

---

## Features

- **Multi-Category Cross-Media Search:**
  - **Books:** Project Gutenberg, Internet Archive, Open Library, Standard Ebooks, LibriVox, Amazon Kindle, Audible, Google Play Books, Kobo.
  - **Movies:** Tubi, YouTube, Internet Archive, JustWatch, Pluto TV, Netflix, Prime Video, Disney+, Apple TV, Google TV.
  - **TV Shows:** Tubi, YouTube, JustWatch, Pluto TV, Netflix, Prime Video, Max, Hulu.
  - **Music:** SoundCloud, Bandcamp, Internet Archive, Jamendo, Free Music Archive, Spotify, Apple Music, YouTube Music, Tidal.

- **Intelligent Availability Heuristic Engine:**
  - Regular expression year detection (identifies US public domain cutoff years prior to 1928 and modern post-2018 titles).
  - Domain-specific pattern matching for classical authors (Shakespeare, Dickens, Austen, Twain, Poe, Doyle, Tolstoy, Homer) and composers (Mozart, Beethoven, Bach, Chopin, Vivaldi, Tchaikovsky).
  - Contextual keyword recognition for audiobooks, archival content, live recordings, remixes, and bootlegs.
  - Dual visual progress meters illustrating confidence scores for free vs. paid likelihood.

- **Dual-Pane Source Organization:** Side-by-side separation between free/public-domain sources and paid/subscription services.

- **One-Click Native Link Dispatch:** Safely encodes query parameters and opens direct search result pages in the user's default web browser.

- **Persistent Search History:** Automatically caches up to 25 unique recent search queries in `search_history.json` using an MRU (Most Recently Used) reordering mechanism.

- **Modern Dark UI:** Custom-styled Tkinter/ttk interface with accessible contrast and clean typography.

---

## Technologies & Tools Used

- **Programming Language:** Python 3.8+
- **GUI Framework:** Tkinter & `ttk` (clam theme)
- **Standard Libraries:** `urllib.parse`, `webbrowser`, `json`, `re`, `pathlib`
- **Data Persistence:** Local JSON storage (`search_history.json`)
- **Testing:** `unittest` framework
- **Version Control:** Git & GitHub

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher installed on your system.
- Tkinter installed (bundled standard with official Python Windows/macOS installers).  
  *On Linux (Ubuntu/Debian), install via:*
  ```bash
  sudo apt-get install python3-tk
