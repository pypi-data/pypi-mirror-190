# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import typing as t
from configparser import ConfigParser as BaseConfigParser
from os import makedirs, path
from os.path import isfile, dirname

import click
import pkg_resources
import pytermor as pt
import yaml

from .log import get_logger
from .. import APP_NAME

_config: ConfigParser | None = None


class ConfigParser(BaseConfigParser):
    def get(self, section: str, option: str, *args, **kwargs) -> t.Any:
        log_msg = f'Getting config value: {section}.{option}'
        result = None
        try:
            result = super().get(section, option, *args, **kwargs)
        except Exception:
            raise
        finally:
            get_logger().info(log_msg + f' = "{result}"')
        return result

    def get_theme_color(self) -> pt.IColor:
        conf_val = self.get('general', 'theme-color')
        try:
            return pt.resolve_color(conf_val)
        except LookupError:
            return pt.cv.RED


def _get_app_config_filepath(name: str) -> str:
    return pkg_resources.resource_filename(APP_NAME, f'data/{name}')

def _get_app_config_raw(name: str) -> t.AnyStr:
    return pkg_resources.resource_stream(APP_NAME, f'data/{name}').read()

def _get_default_config_filepath() -> str:
    return _get_app_config_filepath("es7s.conf.d")

def _get_default_config_raw() -> t.AnyStr:
    return _get_app_config_raw("es7s.conf.d")


def get_app_config_yaml(name: str) -> dict|list:
    return yaml.safe_load(_get_app_config_raw(name + ".yml"))

def get_user_config_filepath() -> str:
    app_dir = click.get_app_dir(APP_NAME)
    return path.join(app_dir, f"{APP_NAME}.conf")


def get_config(require=True) -> ConfigParser | None:
    if not _config:
        if require:
            raise RuntimeError("Config is uninitialized")
        return None
    return _config

def get_default_config() -> ConfigParser:
    default_config = ConfigParser(interpolation=None)
    default_config.read(_get_default_config_raw())
    return default_config


def init_config():
    global _config
    _config = ConfigParser(interpolation=None)  # @todo decorate and log gets/sets

    default_config_filepath = _get_default_config_filepath()
    user_config_filepath = get_user_config_filepath()

    if not isfile(user_config_filepath):
        reset_config()

    config_filepaths = [
        default_config_filepath,
        user_config_filepath,
    ]
    logger = get_logger(False)
    logger.info("Reading configs from: " + ", ".join(f'"{fp}"' for fp in config_filepaths))
    read_ok = _config.read(config_filepaths)
    if not len(read_ok) == len(config_filepaths):
        read_failed = set(config_filepaths) - set(read_ok)
        logger.warning("Failed to read config(s): " + ", ".join(read_failed))


def reset_config():
    default_config_filepath = _get_default_config_filepath()
    user_config_filepath = get_user_config_filepath()
    makedirs(dirname(user_config_filepath), exist_ok=True)

    get_logger().debug(f'Making default config in: "{user_config_filepath}"')
    with open(user_config_filepath, "wt") as user_cfg:
        with open(default_config_filepath, "rt") as default_cfg:
            for idx, line in enumerate(default_cfg.readlines()):
                user_cfg.write(line)
                get_logger().trace(line.strip(), f"{idx+1}| ")


def save_config():
    user_config_filepath = get_user_config_filepath()

    get_logger().debug(f'Writing config to: "{user_config_filepath}"')
    with open(user_config_filepath, "wt") as user_cfg:
        _config.write(user_cfg)
