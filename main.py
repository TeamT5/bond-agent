from libs.service import Service

from libs.service.utility.bond_argparse import Args
from libs.config import config


Args().debug_controller()


def bond_program() -> None:
    """
    Create bond program.
    """

    app = Service(
        title=config.SERVERTITLE,
        description=config.DESCRIPTION,
        version=config.VERSION,
    )
    app.uvicorn_runner(host=config.UVICORN_HOST, port=config.UVICORN_PORT)


def main() -> None:
    """
    Run bond program.
    """

    if config.OS_VERSION == config.System.WINDOWS:
        from pyuac import main_requires_admin
        from libs.service.windows_stray import Stray

        @main_requires_admin
        def create_stray():
            stray = Stray(bond_program)
            stray.hide_console_window()
            stray.stray()

        create_stray()
    else:
        bond_program()


if __name__ == "__main__":
    main()
