import tkinter as tk

from screens.header import create_screen_header
from screens.layout import create_centered_content


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
        
        create_screen_header(
            self,
            "설정",
            right_text="메인",
            right_command=lambda:
                controller.show_frame(
                    "MainScreen"
                )
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

        content = create_centered_content(self)

        menu_column = tk.Frame(content)

        menu_column.pack(
            fill="x",
            expand=True,
        )

        self.create_menu_item(
            menu_column,
            "휴식알림",
            lambda:
                controller.show_frame(
                    "BreakAlarmScreen"
                )
        )

        self.create_menu_item(
            menu_column,
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
            height=50,
            # bg="red",
        )

        row.pack(
            fill="x",
            expand=True,
        )

        from tkinter import ttk

        btn = ttk.Button(
            row,
            text=text,
            command=command,
            style='Menu.TButton',
        )

        btn.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        divider = tk.Frame(parent, height=1, bg="#DDDDDD")

        divider.pack(
            fill="x"
        )