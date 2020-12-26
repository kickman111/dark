import importlib
import os
import sys
from logging import getLogger

BOT_TOKEN = '1457675734:AAG6gVaX536-WmOrGA-gDe6wVUSFbNlaljw'
admin_id = 353171710
API_URL = 'https://telegg.ru/orig/bot'

logger = getLogger(__name__)


def load_config():
    conf_name = os.environ.get("TG_CONF")
    if conf_name is None:
        conf_name = "development"
    try:
        r = importlib.import_module("settings.{}".format(conf_name))
        logger.debug("Loaded config \"{}\" - OK".format(conf_name))
        return r
    except (TypeError, ValueError, ImportError):
        logger.error("Invalid config \"{}\"".format(conf_name))
        sys.exit(1)

