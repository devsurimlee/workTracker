import tkinter as tk

from database import initialize_database

from screens.main_screen import MainScreen
from screens.settings_screen import SettingsScreen
from screens.break_alarm_screen import BreakAlarmScreen
from screens.statistics_screen import StatisticsScreen


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("근무시간 관리")
        self.geometry("800x700")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for FrameClass in (
            MainScreen,
            SettingsScreen,
            BreakAlarmScreen,
            StatisticsScreen
        ):

            frame = FrameClass(
                container,
                self
            )

            self.frames[
                FrameClass.__name__
            ] = frame

            frame.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

        self.show_frame(
            "MainScreen"
        )

    def show_frame(
        self,
        frame_name
    ):

        self.frames[
            frame_name
        ].tkraise()


if __name__ == "__main__":

    initialize_database()

    app = App()

    app.mainloop()