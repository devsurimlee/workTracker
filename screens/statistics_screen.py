import tkinter as tk

from datetime import (
    datetime,
    timedelta
)

from database import get_daily_totals

from screens.header import create_screen_header
from screens.layout import create_centered_content


class StatisticsScreen(tk.Frame):

    def __init__(
        self,
        parent,
        controller
    ):
        super().__init__(parent)

        self.controller = controller
        self.selected_date_str = ""
        self.date_buttons = {}
        self.date_items = []
        self.visible_button_count = 5
        self.date_window_start = 0
        
        create_screen_header(
            self,
            "통계",
            right_text="뒤로가기",
            right_command=lambda:
                controller.show_frame(
                    "SettingsScreen"
                )
        )

        content = create_centered_content(self)

        body = tk.Frame(
            content
        )

        body.pack(
            fill="both",
            expand=True
        )

        month_header = tk.Frame(body)
        month_header.pack(
            fill="x",
            padx=10,
            pady=(10, 10)
        )

        month_header.grid_columnconfigure(
            0,
            weight=1
        )

        month_header.grid_columnconfigure(
            1,
            weight=0
        )

        month_header.grid_columnconfigure(
            2,
            weight=1
        )

        self.month_label = tk.Label(
            month_header,
            text="",
            font=(
                "맑은 고딕",
                16,
                "bold"
            )
        )

        self.month_label.grid(
            row=0,
            column=1
        )

        today_btn = tk.Button(
            month_header,
            text="Today",
            width=8,
            command=self.go_today
        )

        today_btn.grid(
            row=0,
            column=2,
            sticky="e"
        )

        divider_top = tk.Frame(
            body,
            height=1,
            bg="#DDDDDD"
        )

        divider_top.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        date_nav_row = tk.Frame(body)
        date_nav_row.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        prev_btn = tk.Button(
            date_nav_row,
            text="<",
            width=3,
            command=lambda:
                self.move_date_window(-1)
        )

        prev_btn.pack(
            side="left"
        )

        self.date_buttons_frame = tk.Frame(date_nav_row)
        self.date_buttons_frame.pack(
            side="left",
            expand=True,
            fill="x",
            padx=6
        )

        next_btn = tk.Button(
            date_nav_row,
            text=">",
            width=3,
            command=lambda:
                self.move_date_window(1)
        )

        next_btn.pack(
            side="right"
        )

        self.date_buttons_frame.bind(
            "<MouseWheel>",
            self.on_date_mousewheel
        )

        divider_mid = tk.Frame(
            body,
            height=1,
            bg="#DDDDDD"
        )

        divider_mid.pack(
            fill="x",
            padx=10,
            pady=(0, 15)
        )

        self.work_time_label = tk.Label(
            body,
            text="작업시간: 0시간 0분",
            font=(
                "맑은 고딕",
                12
            )
        )

        self.work_time_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 8)
        )

        self.break_time_label = tk.Label(
            body,
            text="휴식시간: 0시간 0분",
            font=(
                "맑은 고딕",
                12
            )
        )

        self.break_time_label.pack(
            anchor="w",
            padx=15
        )

        divider_bottom = tk.Frame(
            body,
            height=1,
            bg="#DDDDDD"
        )

        divider_bottom.pack(
            fill="x",
            padx=10,
            pady=(15, 0)
        )

    def on_show(self):

        self.build_date_items()

        self.selected_date_str = self.date_items[0]["date_str"]
        self.date_window_start = 0

        self.build_date_buttons()
        self.load_date_summary(
            self.selected_date_str
        )

    def build_date_items(self):

        self.date_items = []

        today = datetime.now().date()

        for day_offset in range(60):

            date_obj = today - timedelta(days=day_offset)

            self.date_items.append({
                "date_obj": date_obj,
                "date_str": date_obj.strftime("%Y-%m-%d"),
                "button_text": date_obj.strftime("%m/%d")
            })

    def build_date_buttons(self):

        for child in self.date_buttons_frame.winfo_children():
            child.destroy()

        self.date_buttons = {}

        visible_items = self.date_items[
            self.date_window_start:
            self.date_window_start + self.visible_button_count
        ]

        for item in visible_items:

            btn = tk.Button(
                self.date_buttons_frame,
                text=item["button_text"],
                width=8,
                command=lambda selected=item["date_str"]:
                    self.on_date_click(selected)
            )

            btn.pack(
                side="left",
                padx=4
            )

            self.date_buttons[item["date_str"]] = btn

        self.update_selected_button_style()

    def move_date_window(
        self,
        step
    ):

        max_start = max(
            0,
            len(self.date_items) - self.visible_button_count
        )

        next_start = min(
            max(
                0,
                self.date_window_start + step
            ),
            max_start
        )

        if next_start == self.date_window_start:
            return

        self.date_window_start = next_start
        self.build_date_buttons()

    def on_date_mousewheel(
        self,
        event
    ):

        if event.delta < 0:
            self.move_date_window(1)
        else:
            self.move_date_window(-1)

    def on_date_click(
        self,
        date_str
    ):

        self.selected_date_str = date_str

        self.update_selected_button_style()
        self.load_date_summary(date_str)

    def update_selected_button_style(self):

        for date_str, btn in self.date_buttons.items():

            if date_str == self.selected_date_str:
                btn.config(
                    bg="#2E7D32",
                    fg="white"
                )
            else:
                btn.config(
                    bg="SystemButtonFace",
                    fg="black"
                )

    def load_date_summary(
        self,
        date_str
    ):

        work_seconds, break_seconds = get_daily_totals(date_str)

        selected_dt = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        )

        self.month_label.config(
            text=selected_dt.strftime("%Y년 %m월")
        )

        self.work_time_label.config(
            text=f"작업시간: {self.seconds_to_hm(work_seconds)}"
        )

        self.break_time_label.config(
            text=f"휴식시간: {self.seconds_to_hm(break_seconds)}"
        )

    def go_today(self):

        if not self.date_items:
            self.build_date_items()

        self.selected_date_str = self.date_items[0]["date_str"]
        self.date_window_start = 0

        self.build_date_buttons()
        self.load_date_summary(
            self.selected_date_str
        )

    @staticmethod
    def seconds_to_hm(total_seconds):

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        return f"{hours}시간 {minutes}분"