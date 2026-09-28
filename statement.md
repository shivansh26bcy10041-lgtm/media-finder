# Project Statement

Here's the thing that kicked this off. I'd want to watch some old movie, or find a book I half remembered, and I'd end up with five tabs open, all searching the same words. Half the time I'd finally find it and it was behind a paywall I didn't want. Other times it was sitting on some free site the whole time and I'd just never thought to check there. It's a dumb little problem, but it happened often enough that I decided to fix it for myself.

So `main.py` is the fix. You type a title once, pick books, movies, shows or music, and hit Search. You get two columns. The left one is places that are free or public, the right one is places you'd pay for. Every site has a button, and it opens the search for your title in your browser. That's basically the whole app.

The part I had the most fun with is the little guess at the top, the two bars saying how likely it is that your thing is free. I want to be upfront that it isn't smart. `guess_availability()` is a bunch of hunches turned into if-statements. Old year in the title, like anything before 1928? Probably public domain, so free goes up. Recent year? Probably paid. Austen or Dickens in a book search? Free, almost certainly. Bach or Beethoven? Same. I keep the numbers between 10 and 95 because 100% would just be me pretending to know more than I do.

The code itself is one file, and I left it that way even though a "proper" project would probably split it up. It goes in the order you'd think of it. The `SOURCES` dictionary is at the top, which is just the list of sites, and adding a new one is a single line with `{q}` where the search text goes. Then the guessing function. Then the `MediaFinderApp` class at the bottom, which is the Tkinter window, the buttons, and the history that gets saved to `search_history.json`. I only used what comes with Python, so there's nothing to install. If you've got Python you can run it.

I made a couple of choices on purpose. The app never actually loads any of these sites. It builds a search link and hands it to your browser, which means it's quick, it doesn't break when a site changes its layout, and I'm not scraping anybody. And it never says "this is available on Tubi", because it can't know that. Only the site does. The guess just tells you where to look first.

It has plenty of limits and I'd rather say so. It doesn't know what country you're in, so most links go to the US versions of the sites. The rules will be wrong for lots of titles. And it has no opinion on whether something is legal for you to use, so that's on you.

If I keep working on it, I'd like a country picker, a way to add your own sites from inside the app instead of editing the dictionary, and real availability data instead of guessing. That last one is the big one, and it's probably the difference between a fun little tool and an actually useful one.

To run it, `python main.py`. The `README.md` has the setup details.
