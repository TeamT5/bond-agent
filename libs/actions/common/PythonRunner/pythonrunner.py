import os
import re
import sys
import pkgutil
import tempfile
import functools
import subprocess
from loguru import logger


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
    def _ensure_virtualenv_installed(cls) -> None:
        """
        Check if virtualenv is installed, if not, install it.
        """
        try:
            import virtualenv

            logger.info("virtualenv is already installed.")
        except ImportError:
            logger.info("virtualenv is not installed, installing now...")
            subprocess.run([sys.executable, "-m", "pip", "install", "virtualenv"])

    @classmethod
    def _create_virtualenv(cls, temp_dir: str) -> str:
        """
        Create a virtual environment in the provided directory.

        :param temp_dir: [str] The path to the temporary directory.
        :return: [str] The path to the virtual environment directory.
        """
        venv_dir = os.path.join(temp_dir, ".venv")
        subprocess.check_call([sys.executable, "-m", "virtualenv", venv_dir])
        logger.info(f"Virtual environment created at {venv_dir}")
        return venv_dir

    @classmethod
    def _parse_import_line(cls, line: str) -> str:
        """
        Parse a single import line to extract the base module name, handling aliases and multiple imports.

        :param line: [str] The import line.
        :return: [str] The base module name.
        """
        parts = line.split()
        if parts[0] == "import":
            module_name = parts[1].split(",")[0].split(".")[0].split("as")[0]
        else:  # from import
            module_name = parts[1].split(".")[0]
        return module_name

    @classmethod
    def _get_imported_packages(cls, script_path: str) -> set:
        """
        Use regex to extract the imported module names from a Python script.

        :param script_path: [str] The path to the Python script.
        :return: [set] The set of imported module names.
        """
        std_libs = {module.name for module in pkgutil.iter_modules()}

        import_pattern = re.compile(r"^\s*(?:from\s+([\w\.]+)|import\s+([\w\.]+))")
        imported_modules = set()

        with open(script_path, "r", encoding="utf-8") as file:
            for line in file:
                match = import_pattern.match(line)
                if match:
                    module = match.group(1) or match.group(2)
                    module_name = module.split(".")[0]
                    if module_name not in std_libs:
                        imported_modules.add(module_name)

        return imported_modules

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
                subprocess.run(command)
            except subprocess.CalledProcessError as e:
                logger.error(f"Error installing packages: {e}")

    @classmethod
    def _get_requirements_packages(cls, requirements_path: str) -> list:
        """
        Get the list of packages from the requirements file.

        :param requirements_path: [str] The path to the requirements file.
        :return: [list] The list of package names.
        """
        with open(requirements_path, "r") as file:
            packages = file.read().splitlines()
        return packages

    @classmethod
    def _get_processed_file_path(cls, venv_pip: str, path: str) -> str | None:
        """
        Get the path to the main script file and install the required packages.

        :param venv_pip: [str] The path to the pip executable in the virtual environment.
        :param path: [str] The path to the directory containing the main script file.
        :return: [str] The path to the main script file.
        """

        requirements_path = os.path.join(path, "requirements.txt")
        main_script_path = os.path.join(path, "main.py")
        if not os.path.exists(requirements_path):
            logger.error(f"No requirements.txt found in the directory {path}")
            return None
        packages = cls._get_requirements_packages(requirements_path)
        PythonRunner._install_packages(venv_pip, packages)
        if not os.path.exists(main_script_path):
            logger.error(f"main.py not found in the directory {path}")
            return None

        return main_script_path

    @classmethod
    def _get_processed_project_path(cls, venv_pip: str, path: str) -> str | None:
        """
        Get the path to the main script file and install the required packages.

        :param venv_pip: [str] The path to the pip executable in the virtual environment.
        :param path: [str] The path to the Python file.
        :return: [str] The path to the main script file.
        """

        packages = PythonRunner._get_imported_packages(path)
        PythonRunner._install_packages(venv_pip, list(packages))
        if not os.path.exists(path):
            return None

        return path

    @classmethod
    def check_python_file_or_folder(cls, path: str, venv_pip: str) -> str:
        """
        Check if the provided path is a Python file or folder and install the required packages.

        :param path: [str] The path to the Python file or folder.
        :param venv_pip: [str] The path to the pip executable in the virtual environment.
        :return: [str] The path to the main script file.
        """
        if os.path.isdir(path):
            main_script_path = cls._get_processed_file_path(venv_pip, path)
        elif os.path.isfile(path):
            main_script_path = cls._get_processed_project_path(venv_pip, path)
        else:
            logger.error("The provided path is neither a file nor a directory.")
            return None

        if main_script_path is None:
            return None

        return main_script_path

    @staticmethod
    def execute_with_venv(func: callable) -> callable:
        """
        Create a temporary directory and pass it to the decorated function.

        :param func: [callable] The function to be decorated.
        :return: [callable] The decorated function.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            PythonRunner._ensure_virtualenv_installed()
            with tempfile.TemporaryDirectory() as temp_dir:
                logger.info(f"Temp Path: {temp_dir}")
                venv_dir = PythonRunner._create_virtualenv(temp_dir)
                venv_python, venv_pip = PythonRunner._get_venv_paths(venv_dir)
                kwargs["venv_python"] = venv_python
                kwargs["venv_pip"] = venv_pip
                PythonRunner._ensure_pip_installed(venv_python)

                return func(*args, **kwargs)

        return wrapper
