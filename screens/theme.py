import tkinter as tk
from tkinter import font as tkfont


# 디폴트 프로그램 크기
BASE_WINDOW_WIDTH = 520
BASE_WINDOW_HEIGHT = 500

# 테마 색상
PRIMARY = '#007AFF'
PRIMARY_ACTIVE = '#0051A8'
SECONDARY_BG = '#F2F2F7'
SECONDARY_FG = '#000000'
GHOST_BG = 'white'
DANGER = '#FF3B30'
DANGER_ACTIVE = '#CC2922'
DATE_SELECTED = PRIMARY
GRAY = '#8E8E93'
GRAY_LIGHT = '#C7C7CC'


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


def apply_theme(root):
    """Apply a simple iOS-like theme using ttk styles and default fonts."""

    import tkinter.ttk as ttk

    fonts = create_fonts(root)

    # save fonts for other modules
    root._app_fonts = fonts

    # set default fonts for widgets
    root.option_add("*Font", fonts["body"])
    root.option_add("*Label.Font", fonts["body"])
    root.option_add("*Button.Font", fonts["body"])

    style = ttk.Style(root)

    try:
        style.theme_use('clam')
    except Exception:
        pass

    # Primary button
    style.configure(
        'Primary.TButton',
        background=PRIMARY,
        foreground='white',
        padding=8,
        relief='flat'
    )
    style.map('Primary.TButton', background=[('active', PRIMARY_ACTIVE)])

    # Secondary (filled light) button
    style.configure(
        'Secondary.TButton',
        background=SECONDARY_BG,
        foreground=SECONDARY_FG,
        padding=8,
        relief='flat'
    )

    # Ghost / link style (white background or minimal)
    style.configure(
        'Ghost.TButton',
        # background=GHOST_BG,
        # foreground=PRIMARY,
        padding=6,
        relief='flat',
    )

    # Date buttons (normal / selected)
    style.configure('Date.TButton', padding=6, relief='flat')
    style.configure('DateSelected.TButton', padding=6, relief='flat', background=PRIMARY, foreground='white')
    style.map('DateSelected.TButton', background=[('active', PRIMARY_ACTIVE)])


    # Menu-style full-width button
    style.configure('Menu.TButton', padding=10, relief='flat')

    # Danger button
    style.configure('Danger.TButton', background=DANGER, foreground='white', padding=8, relief='flat')
    style.map('Danger.TButton', background=[('active', DANGER_ACTIVE)])


    # Header label style
    style.configure('Header.TLabel', font=fonts['header_title'])

    # Make default frame/background light
    root.configure(bg='white')


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