# system modules
import logging
import warnings
import os
import pkg_resources

# internal modules
from thunar_plugins.log import console, Notify

# GObject Introspection
import gi

gi.require_version("Thunarx", "3.0")
gi.require_version("Gtk", "3.0")

# internal modules
import thunar_plugins.version
import thunar_plugins.l10n
import thunar_plugins.log
import thunar_plugins.menus
import thunar_plugins.config


THUNAR_PLUGIN_ENTRY_POINT_NAME = "thunar_plugin"

logger = logging.getLogger(__name__)


def get_available_plugins(also_blacklisted=True):
    available_plugins = {}
    if not also_blacklisted:
        config = thunar_plugins.config.Configuration()
        config.load()
    for entry_point in filter(
        (lambda x: True)
        if also_blacklisted
        else lambda e: not config.plugin_is_blacklisted(e),
        pkg_resources.iter_entry_points(THUNAR_PLUGIN_ENTRY_POINT_NAME),
    ):
        try:
            entry_point_obj = entry_point.load()
        except BaseException as e:
            logger.exception(
                "Couldn't load {} entry-point {} from {}: {}".format(
                    repr(THUNAR_PLUGIN_ENTRY_POINT_NAME),
                    repr(entry_point.name),
                    repr(entry_point.dist or "unknown distribution"),
                    e,
                )
            )
            continue
        logger.info(
            "Found {} entry-point {} ({}) from {}".format(
                repr(THUNAR_PLUGIN_ENTRY_POINT_NAME),
                repr(entry_point.name),
                repr(entry_point_obj),
                repr(entry_point.dist or "unknown distribution"),
            )
        )
        available_plugins[entry_point] = entry_point_obj
    return available_plugins
