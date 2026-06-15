import tkinter as tk
from tkinter import ttk

from database import (
    get_setting,
    set_setting
)

from screens.header import create_screen_header
from screens.layout import create_centered_content
from screens.widgets import IosToggleButton 


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

        create_screen_header(
            self,
            "휴식알림",
            right_text="뒤로가기",
            right_command=lambda:
                controller.show_frame(
                    "SettingsScreen"
                )
        )

        # divider = tk.Frame(
        #     self,
        #     height=1,
        #     bg="#CCCCCC"
        # )

        # divider.pack(
        #     fill="x"
        # )

        content = create_centered_content(self)

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
            content
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
            "연속 작업 시간이 설정값을 넘으면\n"
            "휴식을 권장하는 알림을 표시합니다.\n\n"
            "예)\n"
            "90분 설정 → 90분 마다 알림\n"
        )

        # use custom iOS-style toggle button
        toggle = IosToggleButton(
            section1,
            command=lambda val: self._on_toggle(val)
        )

        # initialize state from stored setting
        toggle.set_state(self.enabled_var.get())

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
            content
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
            content
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

    def _on_toggle(self, is_on):

        # keep BooleanVar in sync and persist change
        self.enabled_var.set(bool(is_on))
        self.save_settings()