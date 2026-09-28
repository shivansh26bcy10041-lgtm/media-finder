"""
Media Finder
------------
Type in a book, movie, show or song and get quick links to places that might
have it - free ones on one side, paid ones on the other. There's also a rough
"how likely is it to be free?" guess based on a few simple rules of thumb.

It's a guess, not a promise. Always check the site itself.
"""

import json
import re
import tkinter as tk
import urllib.parse
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk

HISTORY_FILE = Path("search_history.json")
MAX_HISTORY = 25
STARTER_HISTORY = ["Pride and Prejudice", "Metropolis 1927", "Beethoven Symphony No. 5", "Severance"]

# {q} gets swapped for the URL-encoded search text
SOURCES = {
    "books": {
        "free": {
            "Project Gutenberg": "https://www.gutenberg.org/ebooks/search/?query={q}",
            "Internet Archive (Books)": "https://archive.org/search.php?query={q}&and[]=mediatype%3Atexts",
            "Open Library": "https://openlibrary.org/search?q={q}",
            "Standard Ebooks": "https://standardebooks.org/ebooks?query={q}",
            "LibriVox (free audiobooks)": "https://librivox.org/search?q={q}&search_form=advanced",
        },
        "paid": {
            "Amazon Kindle": "https://www.amazon.com/s?k={q}&i=digital-text",
            "Audible": "https://www.audible.com/search?keywords={q}",
            "Google Play Books": "https://play.google.com/store/search?q={q}&c=books",
            "Kobo": "https://www.kobo.com/us/en/search?query={q}",
        },
    },
    "movies": {
        "free": {
            "Tubi": "https://tubitv.com/search/{q}",
            "YouTube (full movies)": "https://www.youtube.com/results?search_query={q}+full+movie",
            "Internet Archive (Movies)": "https://archive.org/search.php?query={q}&and[]=mediatype%3Amovies",
            "JustWatch (free filter)": "https://www.justwatch.com/us/search?q={q}&monetization_types=ads,free",
            "Pluto TV": "https://pluto.tv/us/search/details/{q}",
        },
        "paid": {
            "Netflix": "https://www.netflix.com/search?q={q}",
            "Prime Video": "https://www.amazon.com/s?k={q}&i=instant-video",
            "Disney+": "https://www.disneyplus.com/search?q={q}",
            "Apple TV": "https://tv.apple.com/search?term={q}",
            "Google TV / Play": "https://play.google.com/store/search?q={q}&c=movies",
        },
    },
    "shows": {
        "free": {
            "Tubi": "https://tubitv.com/search/{q}",
            "YouTube (episodes)": "https://www.youtube.com/results?search_query={q}+full+episodes",
            "JustWatch (free filter)": "https://www.justwatch.com/us/search?q={q}&monetization_types=ads,free",
            "Pluto TV": "https://pluto.tv/us/search/details/{q}",
        },
        "paid": {
            "Netflix": "https://www.netflix.com/search?q={q}",
            "Prime Video": "https://www.amazon.com/s?k={q}&i=instant-video",
            "Max": "https://www.max.com/search?q={q}",
            "Hulu": "https://www.hulu.com/search?q={q}",
        },
    },
    "music": {
        "free": {
            "SoundCloud": "https://soundcloud.com/search?q={q}",
            "Bandcamp": "https://bandcamp.com/search?q={q}",
            "Internet Archive (Audio)": "https://archive.org/search.php?query={q}&and[]=mediatype%3Aaudio",
            "Jamendo": "https://www.jamendo.com/search?q={q}",
            "Free Music Archive": "https://freemusicarchive.org/search?quicksearch={q}",
        },
        "paid": {
            "Spotify": "https://open.spotify.com/search/{q}",
            "Apple Music": "https://music.apple.com/us/search?term={q}",
            "YouTube Music": "https://music.youtube.com/search?q={q}",
            "Tidal": "https://listen.tidal.com/search?q={q}",
        },
    },
}


# ---------------------------------------------------------------------------
# The "guessing" part
# ---------------------------------------------------------------------------

CLASSICAL_COMPOSERS = {"mozart", "beethoven", "bach", "chopin", "vivaldi", "tchaikovsky"}
CLASSIC_AUTHORS = {"shakespeare", "dickens", "austen", "twain", "poe", "doyle", "tolstoy", "homer"}
ARCHIVE_WORDS = ("classic", "noir", "silent", "documentary")
EPISODE_WORDS = ("season", "episode", "s0", "e0")
LIVE_MUSIC_WORDS = ("remix", "bootleg", "live", "instrumental")


def mentions_any(text, words):
    """True if any of the words shows up anywhere in the text."""
    return any(w in text for w in words)


def guess_availability(category, query):
    """
    Very rough rules of thumb for whether something is likely free or paid.
    Returns the reasons we came up with plus a 10-95 score for each side.
    """
    text = query.lower().strip()
    reasons = []
    free, paid = 40, 60  # starting point before any clues

    # A year in the title is a big clue. Anything before 1928 is likely public
    # domain in the US; very recent stuff is almost always paid.
    match = re.search(r"\b(18\d{2}|19\d{2}|20[0-2]\d)\b", query)
    if match:
        year = int(match.group(1))
        reasons.append(f"Spotted the year {year}")
        if year < 1928:
            reasons.append("Older than 1928, so it may be public domain")
            free += 45
            paid -= 20
        elif year > 2018:
            reasons.append("Fairly recent, so it's probably paid-only")
            free -= 25
            paid += 30

    if category == "books":
        if mentions_any(text, CLASSIC_AUTHORS):
            reasons.append("Sounds like a classic author")
            free = max(free, 85)
        if mentions_any(text, ("audiobook", "narrated")):
            reasons.append("Looks like you want an audiobook - LibriVox is worth a look")

    elif category in ("movies", "shows"):
        if mentions_any(text, ARCHIVE_WORDS):
            reasons.append("Sounds like an archival or niche title")
            free += 25
        if mentions_any(text, EPISODE_WORDS):
            reasons.append("Looks like an episode-specific search")

    elif category == "music":
        if mentions_any(text, CLASSICAL_COMPOSERS):
            reasons.append("Classical music - lots of it is freely available")
            free += 35
        if mentions_any(text, LIVE_MUSIC_WORDS):
            reasons.append("Remix / live / bootleg material tends to live on free sites")
            free += 20

    if not reasons:
        reasons.append("Nothing in particular stood out. Adding a year or creator might sharpen the guess.")

    # keep the bars from looking too certain either way
    free = max(10, min(95, free))
    paid = max(10, min(95, paid))

    return {"reasons": reasons, "free": free, "paid": paid}


# ---------------------------------------------------------------------------
# The window
# ---------------------------------------------------------------------------

class MediaFinderApp(tk.Tk):
    # dark theme colours
    BG = "#121212"
    SURFACE = "#1e1e1e"
    INPUT = "#2a2a2a"
    BORDER = "#333333"
    TEXT = "#e0e0e0"
    MUTED = "#888888"
    BLUE = "#4a9eff"
    GREEN = "#4caf50"

    FONT = "Segoe UI"

    def __init__(self):
        super().__init__()
        self.title("Media Finder")
        self.geometry("900x740")
        self.minsize(800, 650)
        self.configure(bg=self.BG)

        self.history = self.load_history()
        self.apply_styles()
        self.build_ui()
        self.combo.focus_set()

    # -- setup --------------------------------------------------------------

    def apply_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TLabel", background=self.SURFACE, foreground=self.TEXT, font=(self.FONT, 10))
        style.configure("Title.TLabel", font=(self.FONT, 16, "bold"))
        style.configure("Sub.TLabel", font=(self.FONT, 9), foreground=self.MUTED)
        style.configure("Header.TLabel", font=(self.FONT, 11, "bold"))

        style.configure("Action.TButton", font=(self.FONT, 10, "bold"),
                        background=self.BLUE, foreground="#ffffff")
        style.map("Action.TButton", background=[("active", "#3a8eef")])

        for name, colour in (("Free", self.GREEN), ("Paid", self.BLUE)):
            style.configure(f"{name}.Horizontal.TProgressbar",
                            troughcolor=self.INPUT, background=colour,
                            bordercolor=self.BORDER, thickness=12)

        style.configure("TCombobox", fieldbackground=self.INPUT, background=self.INPUT,
                        foreground=self.TEXT)
        style.map("TCombobox", fieldbackground=[("readonly", self.INPUT)])

    def make_card(self, **pack_options):
        """A dark rounded-ish box that all the sections sit in."""
        card = tk.Frame(self, bg=self.SURFACE, padx=20, pady=14,
                        highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(fill="x", padx=15, **pack_options)
        return card

    def build_ui(self):
        # header
        header = self.make_card(pady=(15, 8))
        ttk.Label(header, text="Media Finder", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Search a few free and paid places at once, with a rough guess at which is likelier.",
                  style="Sub.TLabel").pack(anchor="w")

        # search controls
        controls = self.make_card(pady=4)

        category_row = tk.Frame(controls, bg=self.SURFACE)
        category_row.pack(fill="x", pady=2)
        tk.Label(category_row, text="Looking for:", bg=self.SURFACE, fg=self.TEXT,
                 font=(self.FONT, 10, "bold")).pack(side="left", padx=(0, 10))

        self.category = tk.StringVar(value="books")
        for name in SOURCES:
            tk.Radiobutton(category_row, text=name.title(), value=name, variable=self.category,
                           bg=self.SURFACE, fg=self.TEXT,
                           activebackground=self.SURFACE, activeforeground=self.BLUE,
                           selectcolor=self.INPUT, font=(self.FONT, 10)).pack(side="left", padx=8)

        search_row = tk.Frame(controls, bg=self.SURFACE)
        search_row.pack(fill="x", pady=(12, 0))

        self.query = tk.StringVar()
        self.combo = ttk.Combobox(search_row, textvariable=self.query, values=self.history,
                                  font=(self.FONT, 11))
        self.combo.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=4)
        self.combo.bind("<Return>", lambda event: self.run_search())

        ttk.Button(search_row, text="Search", style="Action.TButton",
                   command=self.run_search).pack(side="right", ipady=3, ipadx=6)

        # the guess
        analysis = self.make_card(pady=6)
        ttk.Label(analysis, text="What we think", style="Header.TLabel").pack(anchor="w")

        self.insight_label = tk.Label(
            analysis, text="Type a title, creator or topic above and we'll take a guess.",
            justify="left", anchor="w", bg=self.SURFACE, fg=self.MUTED, font=(self.FONT, 9))
        self.insight_label.pack(fill="x", pady=(4, 8))

        meters = tk.Frame(analysis, bg=self.SURFACE)
        meters.pack(fill="x")
        self.free_bar = self.add_meter(meters, "Chance it's free:", "Free", gap=25)
        self.paid_bar = self.add_meter(meters, "Chance it's paid:", "Paid", gap=0)

        # link columns
        body = tk.Frame(self, bg=self.BG)
        body.pack(fill="both", expand=True, padx=15, pady=(4, 15))

        self.free_frame = self.make_column(body, " Free / public sources ", self.GREEN, "left", (0, 6))
        self.paid_frame = self.make_column(body, " Paid / subscription ", self.BLUE, "right", (6, 0))

    def add_meter(self, parent, label, style_name, gap):
        tk.Label(parent, text=label, bg=self.SURFACE, fg=self.TEXT,
                 font=(self.FONT, 9)).pack(side="left", padx=(0, 6))
        bar = ttk.Progressbar(parent, orient="horizontal", length=140, mode="determinate",
                              style=f"{style_name}.Horizontal.TProgressbar")
        bar.pack(side="left", padx=(0, gap))
        return bar

    def make_column(self, parent, title, colour, side, padx):
        frame = tk.LabelFrame(parent, text=title, bg=self.SURFACE, fg=colour,
                              font=(self.FONT, 10, "bold"), padx=12, pady=10,
                              highlightbackground=self.BORDER)
        frame.pack(side=side, fill="both", expand=True, padx=padx)
        return frame

    # -- actions ------------------------------------------------------------

    def run_search(self):
        text = self.query.get().strip()
        if not text:
            messagebox.showwarning("Nothing to search", "Type something in first - a title, an artist, anything.")
            return

        category = self.category.get()
        self.remember(text)

        result = guess_availability(category, text)
        self.insight_label.config(text="\n".join("• " + r for r in result["reasons"]))
        self.free_bar["value"] = result["free"]
        self.paid_bar["value"] = result["paid"]

        self.show_links(self.free_frame, SOURCES[category]["free"], text, self.GREEN)
        self.show_links(self.paid_frame, SOURCES[category]["paid"], text, self.BLUE)

    def show_links(self, parent, sources, text, colour):
        # wipe whatever was there from the last search
        for child in parent.winfo_children():
            child.destroy()

        encoded = urllib.parse.quote_plus(text)
        for name, template in sources.items():
            url = template.format(q=encoded)

            row = tk.Frame(parent, bg=self.SURFACE, pady=4)
            row.pack(fill="x")
            tk.Label(row, text="•  " + name, font=(self.FONT, 10),
                     fg=self.TEXT, bg=self.SURFACE).pack(side="left")
            tk.Button(row, text="Open ↗", font=(self.FONT, 9, "bold"),
                      fg="#ffffff", bg=colour,
                      activebackground=self.BORDER, activeforeground="#ffffff",
                      relief="flat", bd=0, padx=10, pady=2, cursor="hand2",
                      command=lambda link=url: webbrowser.open(link)).pack(side="right")

    # -- history ------------------------------------------------------------

    def load_history(self):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return [str(item) for item in data][:MAX_HISTORY]
        except (OSError, ValueError):
            pass  # no file yet, or it's broken - just start fresh
        return list(STARTER_HISTORY)

    def remember(self, text):
        # if we've seen it before, move it to the top instead of ignoring it
        if text in self.history:
            self.history.remove(text)
        self.history.insert(0, text)
        self.history = self.history[:MAX_HISTORY]
        self.combo["values"] = self.history

        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2)
        except OSError:
            pass  # not being able to save history isn't worth interrupting anyone


if __name__ == "__main__":
    MediaFinderApp().mainloop()