import tkinter as tk

from tkinter import ttk
from tkinter import messagebox

import time
import pygame
from winotify import Notification

from datetime import (
    datetime,
    timedelta
)

from database import (
    get_connection,
    get_setting
)

from screens.header import create_screen_header
from screens.layout import create_centered_content


class MainScreen(tk.Frame):

    def __init__(
        self,
        parent,
        controller
    ):
        super().__init__(parent)

        self.controller = controller

        self.state = "IDLE"

        self.session_start_datetime = None

        self.work_start_time = None
        self.break_start_time = None

        self.total_work_seconds = 0
        self.total_break_seconds = 0

        # 휴식 알림
        self.next_alarm_seconds = 0
        self.notification_app_id = "WorkTracker"
        
        pygame.mixer.init()
        
        header, _, _ = create_screen_header(
            self,
            "작업시간 관리",
            right_text="설정",
            right_command=lambda:
                controller.show_frame(
                    "SettingsScreen"
                )
        )

        content = create_centered_content(self)

        self.status_label = tk.Label(
            content,
            text="🔵 대기중",
            font=("맑은 고딕", 16)
        )

        self.status_label.pack(
            pady=5
        )

        self.timer_label = tk.Label(
            content,
            text="00:00:00",
            font=("맑은 고딕", 32)
        )

        self.timer_label.pack(
            pady=10
        )

        self.today_label = tk.Label(
            content,
            text="오늘 누적: 0시간 0분"
        )

        self.today_label.pack(
            pady=5
        )

        self.button_frame = tk.Frame(content)

        self.button_frame.pack(
            pady=10
        )

        self.start_btn = tk.Button(
            self.button_frame,
            text="작업 시작",
            width=15,
            command=self.start_work
        )

        self.pause_btn = tk.Button(
            self.button_frame,
            text="휴식 시작",
            width=15,
            command=self.start_break
        )

        self.resume_btn = tk.Button(
            self.button_frame,
            text="작업 재시작",
            width=15,
            command=self.resume_work
        )

        self.stop_btn = tk.Button(
            self.button_frame,
            text="작업 종료",
            width=15,
            command=self.stop_work
        )
        
        # 개발용 알림
        test_alarm_btn = tk.Button(
            content,
            text="알림 테스트",
            command=self.test_break_alarm
        )

        test_alarm_btn.pack(
            pady=5
        )



        self.update_buttons()
        self.update_today_time()
        self.update_timer()

    def update_buttons(self):

        self.start_btn.grid_remove()
        self.pause_btn.grid_remove()
        self.resume_btn.grid_remove()
        self.stop_btn.grid_remove()

        if self.state == "IDLE":

            self.start_btn.grid(
                row=0,
                column=0,
                padx=5
            )

        elif self.state == "WORKING":

            self.pause_btn.grid(
                row=0,
                column=0,
                padx=5
            )

            self.stop_btn.grid(
                row=0,
                column=1,
                padx=5
            )

        elif self.state == "BREAK":

            self.resume_btn.grid(
                row=0,
                column=0,
                padx=5
            )

            self.stop_btn.grid(
                row=0,
                column=1,
                padx=5
            )


    def start_work(self):

        self.state = "WORKING"

        self.session_start_datetime = datetime.now()

        self.work_start_time = time.time()

        self.total_work_seconds = 0
        self.total_break_seconds = 0

        target_minutes = int(
            get_setting(
                "break_alarm_minutes",
                "90"
            )
        )

        self.next_alarm_seconds = (
            target_minutes * 60
        )

        self.status_label.config(
            text="🟢 작업중"
        )

        self.update_buttons()


    def start_break(self):

        elapsed = int(
            time.time()
            - self.work_start_time
        )

        self.total_work_seconds += elapsed

        self.break_start_time = time.time()

        self.state = "BREAK"

        self.status_label.config(
            text="☕ 휴식중"
        )

        self.update_buttons()

    def resume_work(self):

        elapsed = int(
            time.time()
            - self.break_start_time
        )

        self.total_break_seconds += elapsed

        self.work_start_time = time.time()

        self.state = "WORKING"

        self.status_label.config(
            text="🟢 작업중"
        )

        self.update_buttons()

    def stop_work(self):

        if self.state not in (
            "WORKING",
            "BREAK"
        ):
            return

        result = messagebox.askyesno(
            "확인",
            "작업을 종료하시겠습니까?"
        )

        if not result:
            return

        if self.state == "WORKING":

            elapsed = int(
                time.time()
                - self.work_start_time
            )

            self.total_work_seconds += elapsed

        elif self.state == "BREAK":

            elapsed = int(
                time.time()
                - self.break_start_time
            )

            self.total_break_seconds += elapsed

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO sessions (
            start_time,
            end_time,
            duration_seconds,
            break_seconds
        )
        VALUES (?, ?, ?, ?)
        """, (
            self.session_start_datetime.isoformat(),
            datetime.now().isoformat(),
            self.total_work_seconds,
            self.total_break_seconds
        ))

        conn.commit()
        conn.close()

        self.state = "IDLE"

        self.session_start_datetime = None
        self.work_start_time = None
        self.break_start_time = None

        self.total_work_seconds = 0
        self.total_break_seconds = 0

        self.next_alarm_seconds = 0

        self.status_label.config(
            text="🔵 대기중"
        )

        self.timer_label.config(
            text="00:00:00"
        )

        self.update_buttons()
        self.update_today_time()

    def get_display_seconds(self):

        if self.state == "WORKING":

            return (
                self.total_work_seconds
                + int(
                    time.time()
                    - self.work_start_time
                )
            )

        elif self.state == "BREAK":

            return self.total_work_seconds

        return 0

    
    def check_break_alarm(self):

        if self.state != "WORKING":
            return

        enabled = (
            get_setting(
                "break_alarm_enabled",
                "0"
            ) == "1"
        )

        if not enabled:
            return

        target_minutes = int(
            get_setting(
                "break_alarm_minutes",
                "90"
            )
        )

        alarm_type = get_setting(
            "break_alarm_type",
            "windows"
        )

        current_seconds = (
            self.total_work_seconds
            + int(
                time.time()
                - self.work_start_time
            )
        )

        if current_seconds < self.next_alarm_seconds:
            return

        #
        # 소리 알림
        #

        if alarm_type == "sound":

            try:

                pygame.mixer.music.load(
                    "sounds/break_alarm.mp3"
                )

                pygame.mixer.music.play()

            except Exception as e:

                print(e)

        #
        # Windows 알림
        #

        else:

            try:

                pygame.mixer.music.load(
                    "sounds/break_alarm.mp3"
                )

                pygame.mixer.music.play()

                toast = Notification(
                    app_id=self.notification_app_id,
                    title="휴식 권장",
                    msg=(
                        f"{target_minutes}분 이상 "
                        "작업 중입니다.\n"
                        "잠시 휴식을 권장합니다."
                    ),
                    duration="long"
                )

                toast.show()

            except Exception as e:

                print(e)

        #
        # 다음 알림 시점 계산
        #

        self.next_alarm_seconds += (
            target_minutes * 60
        )


    def update_timer(self):

        seconds = self.get_display_seconds()

        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        self.timer_label.config(
            text=f"{h:02}:{m:02}:{s:02}"
        )

        self.check_break_alarm()

        self.after(
            1000,
            self.update_timer
        )

    def update_today_time(self):

        today = datetime.now().date().isoformat()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            COALESCE(
                SUM(duration_seconds),
                0
            )
        FROM sessions
        WHERE date(start_time)=?
        """, (today,))

        total = cursor.fetchone()[0]

        conn.close()

        self.today_label.config(
            text=f"오늘 누적: {total // 3600}시간 {(total % 3600) // 60}분"
        )


    def test_break_alarm(self):

        alarm_type = get_setting(
            "break_alarm_type",
            "windows"
        )

        #
        # 소리 알림 모드
        #

        if alarm_type == "sound":

            try:

                pygame.mixer.music.load(
                    "sounds/break_alarm.mp3"
                )

                pygame.mixer.music.play()

            except Exception as e:

                print(e)

            return

        #
        # Windows 알림 모드
        #

        try:

            pygame.mixer.music.load(
                "sounds/break_alarm.mp3"
            )

            pygame.mixer.music.play()

            toast = Notification(
                app_id=self.notification_app_id,
                title="휴식 권장",
                msg=(
                    "테스트 알림입니다.\n"
                    "휴식알림이 정상 동작합니다."
                ),
                duration="long"
            )

            toast.show()

        except Exception as e:

            print(e)