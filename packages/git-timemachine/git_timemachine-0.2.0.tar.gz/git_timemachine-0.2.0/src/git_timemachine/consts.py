from pathlib import Path

CONFIG_DIR = Path(
    Path.home(),
    '.git-timemachine'
)

CONFIG_FILE_NAME = Path(
    CONFIG_DIR,
    'config'
)
