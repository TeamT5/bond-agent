import os
import ctypes
import pystray
import win32gui
import webbrowser
import multiprocessing
from PIL import Image

from libs.config import config


class Stray:
    def __init__(self, program: object):
        self.kernel32 = ctypes.WinDLL("kernel32")
        self.program = program

    def bond_process(self) -> None:
        """
        Create bond process.
        """

        self.process = multiprocessing.Process(name="Bond-Agent", target=self.program)
        self.process.start()

    def hide_console_window(self) -> None:
        """
        Hide bond-agent process console window.
        """

        console_window = self.kernel32.GetConsoleWindow()
        if console_window != 0:
            win32gui.ShowWindow(console_window, 0)

    def notify(self, icon: pystray.Icon, title: str, message: str) -> None:
        """
        Create notification with icon.

        :param icon: [pystray.Icon] icon object
        :param title: [str] notification title
        :param message: [str] notification message
        """

        icon.notify(message, title)

    def toggle_console(self, icon: pystray.Icon) -> None:
        """
        Control console window show or hide.

        :param icon: [pystray.Icon] icon object
        """

        console_window = self.kernel32.GetConsoleWindow()
        if console_window != 0:
            if win32gui.IsWindowVisible(console_window):
                win32gui.ShowWindow(console_window, 0)
                text = "已隱藏主控台"
            else:
                win32gui.ShowWindow(console_window, 1)
                text = "已打開主控台"
            self.notify(icon, "主控台控制", text)

    def exit_program(self, icon: pystray.Icon) -> None:
        """
        Create function to close bond-agent process.

        :param icon: [pystray.Icon] icon object
        """

        self.notify(icon, "關閉程式", "您已關閉程式")
        self.process.terminate()
        self.process.join()
        icon.stop()
        os._exit(0)

    def open_bond_index(self, icon: pystray.Icon) -> None:
        """
        create function to open bond index page

        :param icon: [pystray.Icon] icon object
        """

        url = f"http://localhost:{config.UVICORN_PORT}"
        webbrowser.open(url)
        self.notify(icon, "前往首頁", "您已打開 Bond 首頁")

    def stray(self) -> None:
        """
        This is stray main function,it will create a stray object.
        """

        menu = (
            pystray.MenuItem("前往 bond 首頁", self.open_bond_index, default=True),
            pystray.MenuItem("打開/隱藏主控台", self.toggle_console),
            pystray.MenuItem("退出", self.exit_program),
        )
        self.bond_process()
        image = Image.open("./static/img/Bond-Agent.png")

        icon = pystray.Icon("name", image, "Bond", menu)
        icon.run_detached()
