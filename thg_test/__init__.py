#
# coding=utf-8
"""Description of thg base plugin

An overview of what myplugin does.
"""

from pkg_resources import get_distribution, DistributionNotFound

from .myplugin import empty_decorator, darkcode

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'thg_base'
