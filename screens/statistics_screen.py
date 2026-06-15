import tkinter as tk


class StatisticsScreen(tk.Frame):

    def __init__(
        self,
        parent,
        controller
    ):
        super().__init__(parent)
        
        header = tk.Frame(
            self,
            height=60
        )

        header.pack(
            fill="x",
            padx=10,
            pady=10
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="통계",
            font=(
                "맑은 고딕",
                20
            )
        )

        title.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        back_btn = tk.Button(
            header,
            text="뒤로가기",
            command=lambda:
                controller.show_frame(
                    "SettingsScreen"
                )
        )

        back_btn.pack(
            side="right"
        )

        body = tk.Frame(
            self
        )

        body.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            body,
            text="통계",
            font=(
                "맑은 고딕",
                16
            )
        ).pack(
            pady=50
        )