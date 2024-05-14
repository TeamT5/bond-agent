import os
import sys
import tempfile
import functools
import subprocess
from loguru import logger


def _temp_dir_decorator(func: callable):
    """
    Create a temporary directory and pass it to the decorated function.

    :param func: [callable] The function to be decorated.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with tempfile.TemporaryDirectory() as temp_dir:
            logger.info(f"Temp Path: {temp_dir}")
            return func(temp_dir, *args, **kwargs)

    return wrapper


class PythonRunner:
    @classmethod
    def _ensure_pip_installed(cls, venv_python: str) -> None:
        """
        Check if pip needs to be updated and update it if necessary.

        :param venv_python: [str] The path to the python executable in the virtual environment.
        """
        logger.info("Attempting to update pip...")
        try:
            update_pip = subprocess.run(
                [venv_python, "-m", "pip", "install", "--upgrade", "pip"],
                capture_output=True,
                text=True,
            )
            if update_pip.returncode == 0:
                logger.info("Pip successfully updated.")
                logger.info(update_pip.stdout)
            else:
                logger.error("Pip update failed.")
                logger.error(update_pip.stdout)
                logger.error(update_pip.stderr)
        except subprocess.CalledProcessError as e:
            logger.error(f"Subprocess failed: {str(e)}")
            logger.error(e.stdout)
            logger.error(e.stderr)

    @classmethod
    def _create_virtualenv(cls, temp_dir: str) -> str:
        """
        Create a virtual environment in the provided directory.

        :param temp_dir: [str] The path to the temporary directory.
        """
        venv_dir = os.path.join(temp_dir, ".venv")
        subprocess.check_call([sys.executable, "-m", "virtualenv", venv_dir])
        logger.info(f"Virtual environment created at {venv_dir}")
        return venv_dir

    @classmethod
    def _get_module_names_from_script(cls, script_path: str) -> set:
        """
        Get the names of the modules that are imported in the script.

        :param script_path: [str] The path to the script.
        :return: [set] The set of module names.
        """
        with open(script_path, "r") as file:
            lines = file.readlines()
        imports = [
            line.strip()
            for line in lines
            if line.strip().startswith(("import", "from"))
        ]
        logger.info(f"Found import lines: {imports}")
        packages = set()
        for line in imports:
            parts = line.split()
            module_name = parts[1].split(".")[0]
            if (
                module_name not in sys.builtin_module_names
                and module_name not in sys.stdlib_module_names
            ):
                packages.add(module_name)
        return packages

    @classmethod
    def _get_venv_paths(cls, venv_dir: str) -> tuple[str, str]:
        """
        Get the paths to the python and pip executables in the virtual environment.

        :param venv_dir: [str] The path to the virtual environment directory.
        :return: [tuple] The paths to the python and pip executables.
        """

        bin_folder = "Scripts" if sys.platform == "win32" else "bin"
        venv_bin = os.path.join(venv_dir, bin_folder)
        venv_python = os.path.join(venv_bin, "python")
        venv_pip = os.path.join(venv_bin, "pip")
        return venv_python, venv_pip

    @classmethod
    def _install_packages(cls, venv_pip: str, packages: list) -> None:
        """
        Install the provided packages in the virtual environment.

        :param venv_pip: [str] The path to the pip executable in the virtual environment.
        :param packages: [list] The list of package names to install.
        """
        if packages:
            command = [venv_pip, "install"] + packages
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Error installing packages: {e}")

    @classmethod
    def _check_and_install_virtualenv(cls) -> None:
        """
        Check if virtualenv is installed, if not, install it.
        """
        try:
            import virtualenv

            logger.info("virtualenv is already installed.")
        except ImportError:
            logger.info("virtualenv is not installed, installing now...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "virtualenv"]
            )

    @classmethod
    def check_python_file_or_folder(cls, path: str, venv_pip: str) -> str:
        if os.path.isdir(path):
            requirements_path = os.path.join(path, "requirements.txt")
            main_script_path = os.path.join(path, "main.py")
            if os.path.exists(requirements_path):
                with open(requirements_path, "r") as file:
                    packages = file.read().splitlines()
                PythonRunner._install_packages(venv_pip, packages)
                if os.path.exists(main_script_path):
                    return main_script_path
                else:
                    logger.error(f"main.py not found in the directory {path}")
            else:
                logger.error(f"No requirements.txt found in the directory {path}")
        elif os.path.isfile(path):
            packages = PythonRunner._get_module_names_from_script(path)
            PythonRunner._install_packages(venv_pip, list(packages))
            if os.path.exists(path):
                return path
        else:
            logger.error("The provided path is neither a file nor a directory.")

    @staticmethod
    def create_venv_and_do_something(func: callable):
        """
        Create a temporary directory and pass it to the decorated function.

        :param func: [callable] The function to be decorated.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            PythonRunner._check_and_install_virtualenv()
            with tempfile.TemporaryDirectory() as temp_dir:
                logger.info(f"Temp Path: {temp_dir}")
                venv_dir = PythonRunner._create_virtualenv(temp_dir)
                venv_python, venv_pip = PythonRunner._get_venv_paths(venv_dir)
                kwargs["venv_python"] = venv_python
                kwargs["venv_pip"] = venv_pip
                PythonRunner._ensure_pip_installed(venv_python)

                return func(*args, **kwargs)

        return wrapper
