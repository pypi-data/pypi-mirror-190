# Copyright 2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from orpg.mapper.base_msg import *

class grid_msg(map_element_msg_base):
    def __init__(self, parent):
        super().__init__("grid", parent)
