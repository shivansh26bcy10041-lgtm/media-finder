"""
Rule-based heuristic engine for estimating media availability and public domain likelihood.
"""

import re

CLASSICAL_COMPOSERS = {"mozart", "beethoven", "bach", "chopin", "vivaldi", "tchaikovsky"}
CLASSIC_AUTHORS = {"shakespeare", "dickens", "austen", "twain", "poe", "doyle", "tolstoy", "homer"}
ARCHIVE_WORDS = ("classic", "noir", "silent", "documentary")
EPISODE_WORDS = ("season", "episode", "s0", "e0")
LIVE_MUSIC_WORDS = ("remix", "bootleg", "live", "instrumental")


def mentions_any(text, words):
    """Check if any of the target words are present in the text."""
    return any(w in text for w in words)


def guess_availability(category, query):
    """
    Estimates whether a title is likely to be free or paid based on heuristic rules.
    Returns reasons and percentage scores for free vs. paid likelihood.
    """
    text = query.lower().strip()
    reasons = []
    free, paid = 40, 60

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

    free = max(10, min(95, free))
    paid = max(10, min(95, paid))

    return {"reasons": reasons, "free": free, "paid": paid}