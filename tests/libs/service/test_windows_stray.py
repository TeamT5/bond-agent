from libs.config import config


if config.OS_NAME == config.System_Name.WINDOWS:
    from unittest import TestCase
    from unittest import mock
    from libs.service.windows_stray import Stray

    class TestStray(TestCase):
        def setUp(self) -> None:
            self.title = "Stray"
            self.message = "Test Message"

        @mock.patch("multiprocessing.Process")
        def test_bond_process(self, mock_mock_multiprocessing) -> None:
            stray = Stray(None)
            stray.bond_process()

            mock_mock_multiprocessing.assert_called_once_with(
                name="Bond-Agent", target=stray.program
            )
            mock_mock_multiprocessing.return_value.start.assert_called_once()

        @mock.patch("ctypes.WinDLL")
        @mock.patch("win32gui.ShowWindow")
        def test_hide_console_window(self, mock_ShowWindow, mock_kernel32) -> None:
            mock_console_window = (
                mock_kernel32.return_value.GetConsoleWindow.return_value
            )

            stray = Stray(None)
            stray.hide_console_window()
            mock_ShowWindow.assert_called_once_with(mock_console_window, 0)

        @mock.patch("pystray.Icon")
        def test_notify(self, mock_icon) -> None:
            stray = Stray(None)
            stray.notify(mock_icon.return_value, self.title, self.message)

            mock_icon.return_value.notify.assert_called_once_with(
                self.message, self.title
            )

        @mock.patch("ctypes.WinDLL")
        @mock.patch("pystray.Icon")
        @mock.patch("win32gui.IsWindowVisible")
        @mock.patch("win32gui.ShowWindow")
        def test_toggle_console_visible(
            self, mock_ShowWindow, mock_IsWindowVisible, mock_icon, mock_kernel32
        ) -> None:
            mock_console_window = (
                mock_kernel32.return_value.GetConsoleWindow.return_value
            )
            mock_IsWindowVisible.return_value = True

            stray = Stray(None)
            stray.toggle_console(mock_icon)

            mock_ShowWindow.assert_called_once_with(mock_console_window, 0)

            stray.notify(mock_icon.return_value, self.title, self.message)

        @mock.patch("ctypes.WinDLL")
        @mock.patch("pystray.Icon")
        @mock.patch("win32gui.IsWindowVisible")
        @mock.patch("win32gui.ShowWindow")
        def test_toggle_console_hidden(
            self, mock_ShowWindow, mock_IsWindowVisible, mock_icon, mock_kernel32
        ) -> None:
            mock_console_window = (
                mock_kernel32.return_value.GetConsoleWindow.return_value
            ) = 1
            mock_IsWindowVisible.return_value = False

            stray = Stray(None)
            stray.toggle_console(mock_icon)

            mock_ShowWindow.assert_called_once_with(mock_console_window, 1)

            stray.notify(mock_icon.return_value, self.title, self.message)

        @mock.patch("os._exit")
        @mock.patch("pystray.Icon")
        @mock.patch("multiprocessing.Process")
        def test_exit_program(
            self, mock_multiprocessing, mock_icon, mock_os_exit
        ) -> None:
            stray = Stray(None)
            mock_process = mock_multiprocessing.return_value

            stray.bond_process()
            stray.exit_program(mock_icon)
            stray.notify(mock_icon.return_value, self.title, self.message)

            mock_process.terminate.assert_called_once()
            mock_process.join.assert_called_once()
            mock_icon.stop.assert_called_once()
            mock_os_exit.assert_called_once_with(0)

        @mock.patch("pystray.Icon")
        @mock.patch("pystray.MenuItem")
        @mock.patch("PIL.Image.open")
        def test_stray(self, mock_Image, mock_menu, mock_icon) -> None:
            stray = Stray(None)

            stray.bond_process()
            stray.stray()

            mock_icon.assert_called_once_with(
                "name",
                mock_Image.return_value,
                "Bond",
                (
                    mock_menu.return_value,
                    mock_menu.return_value,
                ),
            )
            mock_icon.return_value.run.assert_called_once()
