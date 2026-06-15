import tkinter as tk

from database import initialize_database

from screens.main_screen import MainScreen
from screens.settings_screen import SettingsScreen
from screens.break_alarm_screen import BreakAlarmScreen
from screens.statistics_screen import StatisticsScreen
from screens.theme import apply_theme
from screens import theme


BASE_WINDOW_WIDTH = theme.BASE_WINDOW_WIDTH
BASE_WINDOW_HEIGHT = theme.BASE_WINDOW_HEIGHT


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("작업시간 관리")
        # apply app-wide theme (fonts, ttk styles)
        apply_theme(self)
        self.geometry(f"{BASE_WINDOW_WIDTH}x{BASE_WINDOW_HEIGHT}")
        self.minsize(BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT)

        self._base_scaling = float(self.tk.call("tk", "scaling"))
        self._current_scale = 1.0

        self.bind(
            "<Configure>",
            self.on_window_configure
        )

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(
            0,
            weight=1
        )
        container.grid_columnconfigure(
            0,
            weight=1
        )

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
        frame = self.frames[
            frame_name
        ]

        frame.tkraise()

        if hasattr(
            frame,
            "on_show"
        ):
            frame.on_show()

    def on_window_configure(
        self,
        event
    ):

        if event.widget is not self:
            return

        width_scale = event.width / BASE_WINDOW_WIDTH
        height_scale = event.height / BASE_WINDOW_HEIGHT

        scale = max(
            1.0,
            min(width_scale, height_scale)
        )

        if abs(scale - self._current_scale) < 0.05:
            return

        self._current_scale = scale

        self.tk.call(
            "tk",
            "scaling",
            self._base_scaling * scale
        )


if __name__ == "__main__":

    initialize_database()

    app = App()

    app.mainloop()