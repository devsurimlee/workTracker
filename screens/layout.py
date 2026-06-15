import tkinter as tk


def create_centered_content(parent):

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

    centered = tk.Frame(outer)

    centered.grid(
        row=0,
        column=0
    )

    return centered