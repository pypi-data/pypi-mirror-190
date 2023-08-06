# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import tempfile

from .log import get_logger
from .. import APP_DEV

RUNTIME_DIR = [
    '/var/run/es7s',
    '/tmp/es7s',
]


def get_socket_path(topic: str):
    filename = f"{topic}.socket"
    path = os.path.join(_get_runtime_dir(), filename)
    if APP_DEV:
        path += ".dev"
    return path


def get_daemon_lockfile_path():
    return os.path.join(_get_runtime_dir(), "es7s-daemon.lock")


def _get_runtime_dir() -> str:
    e = Exception("No runtime dirs provided")
    for runtime_dir in RUNTIME_DIR:
        try:
            os.makedirs(runtime_dir, exist_ok=True)
            testfile = tempfile.TemporaryFile(dir=runtime_dir)
            testfile.close()
        except Exception as e:
            get_logger(False).warning(f'Runtime dir is not writeable: "{runtime_dir}"')
            continue
        return runtime_dir
    raise OSError("Could not find suitable runtime directory") from e
