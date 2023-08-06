"""Ruler (measurement) protocol."""

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

__copyright__ = "Copyright 2023 David Vrabel"

from orpg.mapper.base_msg import *

class ruler_msg(map_element_msg_base):
    def __init__(self, parent):
        super().__init__("ruler", parent)
