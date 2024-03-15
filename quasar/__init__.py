# -*- coding: utf-8 -*-

"""
quasar
==========

A infinite chess engine.

:copyright:     (c) 2024 Tymon Becella
:license:       MIT
"""

__title__ = 'quasar'
__author__ = 'Tymon Becella'
__license__ = 'MIT'
__copyright__ = 'Copyright 2024 Tymon Becella'
__version__ = '0.0.1'

import os

from logger import logger, clear_logs
from .chess import *
from .engine import *
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from .gui import *
