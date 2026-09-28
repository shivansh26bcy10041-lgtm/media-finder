"""
Graphical User Interface for the Media Finder application.
"""

import tkinter as tk
import urllib.parse
import webbrowser
from tkinter import messagebox, ttk

from core.heuristics import guess_availability
from core.history import HistoryManager
from core.sources import SOURCES


class MediaFinderApp(tk.Tk):
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

        self.history_mgr = HistoryManager()
        self.history = self.history_mgr.history

        self.apply_styles()
        self.build_ui()
        self.combo.focus_set()

    def apply_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TLabel", background=self.SURFACE, foreground=self.TEXT, font=(self.FONT, 10))
        style.configure("Title.TLabel", font=(self.FONT, 16, "bold"))
        style.configure("Sub.TLabel", font=(self.FONT, 9), foreground=self.MUTED)
        style.configure("Header.TLabel", font=(self.FONT, 11, "bold"))

        style.configure("Action.TButton", font=(self.FONT, 10, "bold"), background=self.BLUE, foreground="#ffffff")
        style.map("Action.TButton", background=[("active", "#3a8eef")])

        for name, colour in (("Free", self.GREEN), ("Paid", self.BLUE)):
            style.configure(f"{name}.Horizontal.TProgressbar",
                            troughcolor=self.INPUT, background=colour,
                            bordercolor=self.BORDER, thickness=12)

        style.configure("TCombobox", fieldbackground=self.INPUT, background=self.INPUT, foreground=self.TEXT)
        style.map("TCombobox", fieldbackground=[("readonly", self.INPUT)])

    def make_card(self, **pack_options):
        card = tk.Frame(self, bg=self.SURFACE, padx=20, pady=14,
                        highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(fill="x", padx=15, **pack_options)
        return card

    def build_ui(self):
        header = self.make_card(pady=(15, 8))
        ttk.Label(header, text="Media Finder", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Search a few free and paid places at once, with a rough guess at which is likelier.",
                  style="Sub.TLabel").pack(anchor="w")

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
        self.combo = ttk.Combobox(search_row, textvariable=self.query, values=self.history, font=(self.FONT, 11))
        self.combo.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=4)
        self.combo.bind("<Return>", lambda event: self.run_search())

        ttk.Button(search_row, text="Search", style="Action.TButton",
                   command=self.run_search).pack(side="right", ipady=3, ipadx=6)

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

        body = tk.Frame(self, bg=self.BG)
        body.pack(fill="both", expand=True, padx=15, pady=(4, 15))

        self.free_frame = self.make_column(body, " Free / public sources ", self.GREEN, "left", (0, 6))
        self.paid_frame = self.make_column(body, " Paid / subscription ", self.BLUE, "right", (6, 0))

    def add_meter(self, parent, label, style_name, gap):
        tk.Label(parent, text=label, bg=self.SURFACE, fg=self.TEXT, font=(self.FONT, 9)).pack(side="left", padx=(0, 6))
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

    def run_search(self):
        text = self.query.get().strip()
        if not text:
            messagebox.showwarning("Nothing to search", "Type something in first - a title, an artist, anything.")
            return

        category = self.category.get()
        self.history = self.history_mgr.remember(text)
        self.combo["values"] = self.history

        result = guess_availability(category, text)
        self.insight_label.config(text="\n".join("• " + r for r in result["reasons"]))
        self.free_bar["value"] = result["free"]
        self.paid_bar["value"] = result["paid"]

        self.show_links(self.free_frame, SOURCES[category]["free"], text, self.GREEN)
        self.show_links(self.paid_frame, SOURCES[category]["paid"], text, self.BLUE)

    def show_links(self, parent, sources, text, colour):
        for child in parent.winfo_children():
            child.destroy()

        encoded = urllib.parse.quote_plus(text)
        for name, template in sources.items():
            url = template.format(q=encoded)
            row = tk.Frame(parent, bg=self.SURFACE, pady=4)
            row.pack(fill="x")
            tk.Label(row, text="•  " + name, font=(self.FONT, 10), fg=self.TEXT, bg=self.SURFACE).pack(side="left")
            tk.Button(row, text="Open ↗", font=(self.FONT, 9, "bold"),
                      fg="#ffffff", bg=colour,
                      activebackground=self.BORDER, activeforeground="#ffffff",
                      relief="flat", bd=0, padx=10, pady=2, cursor="hand2",
                      command=lambda link=url: webbrowser.open(link)).pack(side="right")