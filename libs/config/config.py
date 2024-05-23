import sys
from libs.config.__version__ import __version__
from fastapi.templating import Jinja2Templates

# *----- Server Setting -----*
DEBUG = False
DOCS_URL = "/Bond-Agent/Swagger_UI"
REDOC_URL = "/Bond-Agent/API_redoc"
SERVERTITLE = "Bond-Agent"
FAVICON_URL = "/static/img/Bond-Agent.ico"
VERSION = __version__
DESCRIPTION = """
[Bond-Agent Index](/)\n

"""

# *----- Templates & static Setting -----*
STATIC_PATH = "static"

TEMPLATES_PATH = "templates"
TEMPLATES = Jinja2Templates(directory=TEMPLATES_PATH)


# *----- uvicorn Setting -----*
UVICORN_HOST = "0.0.0.0"
UVICORN_PORT = 8086

# *----- Server Access Log Setting -----*
ACCESS_LOG_NAME = "uvicorn.access"
ACCESS_LOG_SIZE = 1000  # 單位為 KB
ACCESS_LOG_LEVEL = "DEBUG"
ACCESS_LOG_PATH = "logs"
ACCESS_LOG_FILE_NAME = "BOND_ACCESS_LOG.log"
ACCESS_LOG_BACKUP_COUNT = 5
ACCESS_LOG_MODE = "a"
ACCESS_LOG_ENCODING = "utf-8"

# *----- Download Setting -----*
DOWNLOAD_DIR_NAME = "Downloads"
DOWNLOAD_PATH = "./Downloads"


# *----- OS Setting -----*
class System:
    AIX = "aix"
    LINUX = "linux"
    WINDOWS = "win32"
    WINDOWS_CYGWIN = "cygwin"
    MAC = "darwin"


class System_Name:
    WINDOWS = "Windows"
    LINUX = "Linux"
    MAC = "Mac"
    WINDOWS_CYGWIN = "Cygwin"
    AIX = "AIX"


SYSTEM_CHART = {
    System.AIX: "AIX",
    System.LINUX: "Linux",
    System.WINDOWS: "Windows",
    System.WINDOWS_CYGWIN: "Cygwin",
    System.MAC: "Mac",
}

OS_VERSION = sys.platform
OS_NAME = SYSTEM_CHART[OS_VERSION]
