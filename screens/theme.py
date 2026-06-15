import tkinter as tk
from tkinter import font as tkfont


BASE_WINDOW_WIDTH = 480
BASE_WINDOW_HEIGHT = 700

FONT_SPECS = {
    "header_title": {
        "family": "맑은 고딕",
        "size": 20,
    },
    "status": {
        "family": "맑은 고딕",
        "size": 16,
    },
    "timer": {
        "family": "맑은 고딕",
        "size": 32,
    },
    "body": {
        "family": "맑은 고딕",
        "size": 12,
    },
    "menu": {
        "family": "맑은 고딕",
        "size": 12,
    },
    "section": {
        "family": "맑은 고딕",
        "size": 11,
    },
    "month": {
        "family": "맑은 고딕",
        "size": 16,
        "weight": "bold",
    },
}


def create_fonts(root):

    fonts = {}

    for name, spec in FONT_SPECS.items():

        fonts[name] = tkfont.Font(
            root=root,
            family=spec["family"],
            size=spec["size"],
            weight=spec.get("weight", "normal")
        )

    return fonts


def scale_fonts(fonts, scale):

    for name, spec in FONT_SPECS.items():

        fonts[name].configure(
            size=max(1, round(spec["size"] * scale))
        )


def create_centered_body(parent):

    outer = tk.Frame(parent)
    outer.pack(
        fill="both",
        expand=True
    )

    outer.grid_rowconfigure(
        0,
        weight=1
    )

    outer.grid_columnconfigure(
        0,
        weight=1
    )

    panel = tk.Frame(outer)
    panel.grid(
        row=0,
        column=0
    )

    return outer, panel