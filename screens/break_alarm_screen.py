import tkinter as tk
from tkinter import ttk

from database import (
    get_setting,
    set_setting
)


class ToolTip:

    def __init__(
        self,
        widget,
        text
    ):

        self.widget = widget
        self.text = text

        self.tooltip = None

        widget.bind(
            "<Enter>",
            self.show
        )

        widget.bind(
            "<Leave>",
            self.hide
        )

    def show(
        self,
        event=None
    ):

        if self.tooltip:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(
            self.widget
        )

        self.tooltip.wm_overrideredirect(
            True
        )

        self.tooltip.geometry(
            f"+{x}+{y}"
        )

        label = tk.Label(
            self.tooltip,
            text=self.text,
            justify="left",
            background="#FFFFE0",
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=5
        )

        label.pack()

    def hide(
        self,
        event=None
    ):

        if self.tooltip:

            self.tooltip.destroy()

            self.tooltip = None


class BreakAlarmScreen(tk.Frame):

    def __init__(
        self,
        parent,
        controller
    ):
        super().__init__(parent)

        self.controller = controller

        #
        # 상단 헤더
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

        header.pack_propagate(
            False
        )

        title = tk.Label(
            header,
            text="휴식알림",
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

        divider = tk.Frame(
            self,
            height=1,
            bg="#CCCCCC"
        )

        divider.pack(
            fill="x"
        )

        #
        # 설정 로드
        #

        self.enabled_var = tk.BooleanVar(
            value=get_setting(
                "break_alarm_enabled",
                "0"
            ) == "1"
        )

        self.minutes_var = tk.IntVar(
            value=int(
                get_setting(
                    "break_alarm_minutes",
                    "90"
                )
            )
        )

        self.alarm_type_var = tk.StringVar(
            value=get_setting(
                "break_alarm_type",
                "windows"
            )
        )

        #
        # 휴식알림 사용
        #

        section1 = tk.Frame(
            self
        )

        section1.pack(
            fill="x",
            padx=15,
            pady=15
        )

        left = tk.Frame(
            section1
        )

        left.pack(
            side="left"
        )

        title_row = tk.Frame(
            left
        )

        title_row.pack(
            anchor="w"
        )

        tk.Label(
            title_row,
            text="휴식알림 사용",
            font=(
                "맑은 고딕",
                11
            )
        ).pack(
            side="left"
        )

        help_btn = tk.Label(
            title_row,
            text=" ? ",
            fg="blue",
            cursor="hand2"
        )

        help_btn.pack(
            side="left",
            padx=5
        )

        ToolTip(
            help_btn,
            "연속 근무 시간이 설정값을 넘으면\n"
            "휴식을 권장하는 알림을 표시합니다.\n\n"
            "예)\n"
            "90분 설정\n"
            "↓\n"
            "90분 연속 근무\n"
            "↓\n"
            "설정한 방식으로 알림"
        )

        toggle = ttk.Checkbutton(
            section1,
            variable=self.enabled_var,
            command=self.save_settings
        )

        toggle.pack(
            side="right"
        )

        divider = tk.Frame(
            self,
            height=1,
            bg="#DDDDDD"
        )

        divider.pack(
            fill="x"
        )

        #
        # 휴식알림 시간
        #

        section2 = tk.Frame(
            self
        )

        section2.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            section2,
            text="휴식알림 시간"
        ).pack(
            anchor="w"
        )

        spinbox = ttk.Spinbox(
            section2,
            from_=10,
            to=300,
            width=10,
            textvariable=self.minutes_var
        )

        spinbox.pack(
            anchor="w",
            pady=5
        )

        spinbox.bind(
            "<FocusOut>",
            lambda e:
                self.save_settings()
        )

        divider = tk.Frame(
            self,
            height=1,
            bg="#DDDDDD"
        )

        divider.pack(
            fill="x"
        )

        #
        # 알림 방식
        #

        section3 = tk.Frame(
            self
        )

        section3.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            section3,
            text="알림 방식",
            font=(
                "맑은 고딕",
                11
            )
        ).pack(
            anchor="w"
        )

        tk.Radiobutton(
            section3,
            text="Windows 알림",
            variable=self.alarm_type_var,
            value="windows",
            command=self.save_settings
        ).pack(
            anchor="w"
        )

        tk.Radiobutton(
            section3,
            text="소리 알림",
            variable=self.alarm_type_var,
            value="sound",
            command=self.save_settings
        ).pack(
            anchor="w"
        )

        divider = tk.Frame(
            self,
            height=1,
            bg="#DDDDDD"
        )

        divider.pack(
            fill="x"
        )

    def save_settings(self):

        set_setting(
            "break_alarm_enabled",
            "1" if self.enabled_var.get() else "0"
        )

        set_setting(
            "break_alarm_minutes",
            self.minutes_var.get()
        )

        set_setting(
            "break_alarm_type",
            self.alarm_type_var.get()
        )