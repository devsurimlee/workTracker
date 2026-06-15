import tkinter as tk


def create_screen_header(
    parent,
    title,
    right_text=None,
    right_command=None,
    right_width=8,
):

    header = tk.Frame(
        parent,
        height=84,
        # bg="white"
    )

    header.pack(
        fill="x",
        padx=10,
        pady=4
    )

    header.pack_propagate(False)

    header.grid_columnconfigure(
        0,
        weight=1
    )

    header.grid_columnconfigure(
        1,
        weight=0
    )

    header.grid_columnconfigure(
        2,
        weight=1
    )

    title_label = tk.Label(
        header,
        text=title,
        # bg="white",
        font=(
            "맑은 고딕",
            20,
            "bold"
        )
    )

    title_label.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    right_button = None

    if right_text and right_command:

        try:
            import tkinter.ttk as ttk

            right_button = ttk.Button(
                header,
                text=right_text,
                width=right_width,
                command=right_command
            )
        except Exception:
            right_button = tk.Button(
                header,
                text=right_text,
                width=right_width,
                command=right_command
            )

        right_button.grid(
            row=0,
            column=2,
            sticky="e",
            padx=10
        )

    return header, title_label, right_button