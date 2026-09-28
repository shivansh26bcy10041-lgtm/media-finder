"""
Media source endpoints for Books, Movies, Shows, and Music.
"""

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