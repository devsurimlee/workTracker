import tkinter as tk
import os
import pygame
from tkinter import ttk

from database import (
    get_setting,
    set_setting
)

from screens.header import create_screen_header
from screens.widgets import IosToggleButton, IosStepper 
from screens import theme


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
            right_command=self._on_back_click
        )

        # [수정 포인트] 중앙 정렬 함수 대신, 상단 정렬되는 일반 프레임을 생성하여 가로를 채웁니다.
        content = tk.Frame(self)
        content.pack(fill="x", expand=False) # expand=False로 위쪽으로 밀착시킵니다.

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

        # [이 코드 추가] DB에서 알림 소리 파일명 로드 (기본값: levelup.mp3)
        self.alarm_sound_var = tk.StringVar(
            value=get_setting(
                "break_alarm_sound",
                "levelup.mp3"
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
            text="휴식알림 시간(분)",
            font=(
                "맑은 고딕",
                11
            )
        ).pack(
            side="left",
            anchor="w"
        )

        # 커스텀 Stepper 위젯 배치
        spinbox = IosStepper(
            section2,
            from_=1,
            to=300,
            step=1,
            textvariable=self.minutes_var
        )

        spinbox.pack(
            side="right",
            anchor="e"
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
            anchor="w",
            pady=(0, 10)
        )

        # iOS 리스트 뷰 효과를 내기 위한 캡슐 컨테이너 프레임
        options_container = tk.Frame(
            section3,
            bg="#E9E9EA", 
            padx=2,
            pady=2
        )
        options_container.pack(fill="x")

        # 인스턴스 변수로 관리하여 추후 업데이트 가능하게 조율
        self.option_rows = {}

        # 옵션 리스트 정의 (DB에 세팅될 값 : 화면에 뿌려줄 텍스트)
        alarm_options = [
            ("windows", "Windows 알림"),
            ("sound", "소리 알림")
        ]

        for index, (val, text) in enumerate(alarm_options):
            # 각 행 카드 생성 (클릭 가능한 프레임)
            row_card = tk.Frame(
                options_container,
                bg="#FFFFFF", 
                height=45,
                cursor="hand2"
            )
            row_card.pack(fill="x", pady=1 if index > 0 else 0) 
            row_card.pack_propagate(False)

            # 레이블 배치
            lbl = tk.Label(
                row_card,
                text=text,
                font=("맑은 고딕", 11),
                bg="#FFFFFF",
                fg="#000000"
            )
            lbl.pack(side="left", padx=15)

            # 우측 체크마크 기호 영역
            check_lbl = tk.Label(
                row_card,
                text="✓" if self.alarm_type_var.get() == val else "",
                font=("맑은 고딕", 12, "bold"),
                bg="#FFFFFF",
                fg=theme.PRIMARY 
            )
            check_lbl.pack(side="right", padx=15)

            # 메모리에 컴포넌트 주소 바인딩 저장
            self.option_rows[val] = (row_card, lbl, check_lbl)

            # 카드 영역 아무데나 클릭해도 값이 바뀌도록 바인딩 처리
            row_card.bind("<Button-1>", lambda e, v=val: self._on_select_alarm_type(v))
            lbl.bind("<Button-1>", lambda e, v=val: self._on_select_alarm_type(v))
            check_lbl.bind("<Button-1>", lambda e, v=val: self._on_select_alarm_type(v))

        ## for문 끝난 지점

        # 알림 소리 동적 탐색 및 리스트 뷰 영역
        section4 = tk.Frame(content)
        section4.pack(fill="x", padx=15, pady=15)

        tk.Label(section4, text="알림 소리", font=("맑은 고딕", 11)).pack(anchor="w", pady=(0, 10))

        sound_container = tk.Frame(section4, bg="#E9E9EA", padx=2, pady=2)
        sound_container.pack(fill="x")

        self.sound_rows = {}
        
        # sounds/ 폴더에서 실제 mp3 파일 목록 동적 호출
        sound_dir = "sounds"
        if not os.path.exists(sound_dir):
            os.makedirs(sound_dir)
        mp3_files = [f for f in os.listdir(sound_dir) if f.endswith(".mp3")]

        if not mp3_files:
            no_sound_card = tk.Frame(sound_container, bg="#FFFFFF", height=45)
            no_sound_card.pack(fill="x")
            no_sound_card.pack_propagate(False)
            tk.Label(no_sound_card, text="sounds/ 폴더에 mp3 파일이 없습니다.", font=("맑은 고딕", 10), bg="#FFFFFF", fg="gray").pack(side="left", padx=15)
        else:
            for index, filename in enumerate(mp3_files):
                # [수정] 파일명에서 확장자(.mp3)를 제외한 순수 이름만 추출합니다.
                display_name = os.path.splitext(filename)[0]

                row_card = tk.Frame(sound_container, bg="#FFFFFF", height=45, cursor="hand2")
                row_card.pack(fill="x", pady=1 if index > 0 else 0) 
                row_card.pack_propagate(False)

                # [수정] text 속성에 filename 대신 display_name을 대입합니다.
                lbl = tk.Label(row_card, text=display_name, font=("맑은 고딕", 11), bg="#FFFFFF", fg="#000000")
                lbl.pack(side="left", padx=15)

                check_lbl = tk.Label(row_card, text="✓" if self.alarm_sound_var.get() == filename else "", font=("맑은 고딕", 12, "bold"), bg="#FFFFFF", fg=theme.PRIMARY)
                check_lbl.pack(side="right", padx=15)

                # 딕셔너리 키값과 바인딩 함수에는 실제 파일명(filename)을 그대로 유지해야 DB 저장 시 문제가 없습니다.
                self.sound_rows[filename] = (row_card, lbl, check_lbl)

                row_card.bind("<Button-1>", lambda e, f=filename: self._on_select_sound(f))
                lbl.bind("<Button-1>", lambda e, f=filename: self._on_select_sound(f))
                check_lbl.bind("<Button-1>", lambda e, f=filename: self._on_select_sound(f))



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

        # 새로 선택한 알람 소리 파일명을 DB에 일괄 저장
        set_setting(
            "break_alarm_sound",
            self.alarm_sound_var.get()
        )

    def _on_toggle(self, is_on):
        self.enabled_var.set(bool(is_on))

    def _on_back_click(self):
        self.save_settings()
        self.controller.show_frame("SettingsScreen")


    def _on_select_alarm_type(self, selected_val):
        """항목 클릭 시 라디오 변수 값을 업데이트하고 체크마크 위치를 토글하는 함수"""
        self.alarm_type_var.set(selected_val)
        
        # UI 새로고침
        for val, (row, lbl, check_lbl) in self.option_rows.items():
            if val == selected_val:
                check_lbl.config(text="✓")
            else:
                check_lbl.config(text="")

    def _on_select_sound(self, selected_sound):
        """소리 항목 클릭 시 변수를 교체하고, 체크마크 전환 및 소리 미리듣기를 실행하는 함수"""
        self.alarm_sound_var.set(selected_sound)
        for filename, (row, lbl, check_lbl) in self.sound_rows.items():
            if filename == selected_sound:
                check_lbl.config(text="✓")
            else:
                check_lbl.config(text="")

        # [여기서부터 미리듣기 로직 추가]
        import os
        import pygame

        sound_path = os.path.join("sounds", selected_sound)

        try:
            # 1. 기존에 재생 중이던 소리가 있다면 멈춥니다.
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            # 2. 선택한 mp3 파일을 로드하여 1회 재생합니다.
            if os.path.exists(sound_path):
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
        except Exception as e:
            print(f"소리 재생 실패: {e}")
