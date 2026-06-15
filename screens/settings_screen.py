import tkinter as tk


class SettingsScreen(tk.Frame):

    def __init__(
        self,
        parent,
        controller
    ):
        super().__init__(parent)

        self.controller = controller

        #
        # 상단 고정 영역
        #
        
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
            text="설정",
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

        home_btn = tk.Button(
            header,
            text="메인",
            command=lambda:
                controller.show_frame(
                    "MainScreen"
                )
        )

        home_btn.pack(
            side="right"
        )

        divider = tk.Frame(
            self,
            height=1,
            bg="#CCCCCC"
        )

        divider.pack(
            fill="x"
        )

        #
        # 스크롤 영역
        #

        content = tk.Frame(
            self
        )

        content.pack(
            fill="both",
            expand=True
        )

        self.create_menu_item(
            content,
            "휴식알림",
            lambda:
                controller.show_frame(
                    "BreakAlarmScreen"
                )
        )

        self.create_menu_item(
            content,
            "통계",
            lambda:
                controller.show_frame(
                    "StatisticsScreen"
                )
        )

    def create_menu_item(
        self,
        parent,
        text,
        command
    ):

        row = tk.Frame(
            parent,
            height=50
        )

        row.pack(
            fill="x"
        )

        btn = tk.Button(
            row,
            text=text,
            relief="flat",
            anchor="w",
            font=(
                "맑은 고딕",
                12
            ),
            command=command
        )

        btn.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        divider = tk.Frame(
            parent,
            height=1,
            bg="#DDDDDD"
        )

        divider.pack(
            fill="x"
        )