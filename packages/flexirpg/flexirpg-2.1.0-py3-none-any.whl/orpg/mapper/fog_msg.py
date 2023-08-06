# Map fog.
#
# Copyright 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# <fog enable='1' tsize='64', psize='20'>
#   <tile id='x,y' bitmap="..."/>
# </fog>

import base64
import string
import xml.dom.minidom

from orpg.mapper.base_msg import *
from orpg.mapper.region import *
from orpg.lib.xmlutil import bool_attrib, int_attrib, str_attrib

DEFAULT_TILE_SIZE = 64
DEFAULT_PIXEL_SIZE = 20

class fog_tile_msg(map_element_msg_base):
    def __init__(self, parent, id):
        super().__init__("tile", parent)

        self.set_prop("id", id)

class fog_msg(map_element_msg_base):
    def __init__(self, parent=None, reset_hook=None, updated_hook=None):
        super().__init__("fog", parent)

        self._reset_hook = reset_hook
        self._updated_hook = updated_hook

        self._enable = False
        self._tile_size = DEFAULT_TILE_SIZE
        self._pixel_size = DEFAULT_PIXEL_SIZE

        self.init_props({"enable": f"{int(self._enable)}",
                         "tsize": f"{self._tile_size}",
                         "psize": f"{self._pixel_size}"})

    @property
    def enable(self):
        return self._enable

    @enable.setter
    def enable(self, state):
        if state != self._enable:
            self._enable = state
            self.set_prop("enable", f"{int(self._enable)}")
            self._reset()

    @property
    def tile_size(self):
        return self._tile_size

    @property
    def tile_visible_size(self):
        return self._tile_size * self.pixel_size

    @property
    def pixel_size(self):
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, psize):
        if psize != self._pixel_size:
            self._pixel_size = psize
            self.set_prop("psize", f"{psize}")
            self._reset()

    def set_bitmap(self, x, y, texels):
        id = f"{x},{y}"
        bitmap = base64.b64encode(texels).decode("ascii")
        if id not in self.children:
            self.children[id] = fog_tile_msg(self, id)
        self.children[id].set_prop("bitmap", bitmap)

    def init_from_dom(self, xml_dom):
        with self.p_lock:
            self._init_from_dom(xml_dom)

    def set_from_dom(self, xml_dom):
        with self.p_lock:
            self._init_from_dom(xml_dom)

    def _init_from_dom(self, xml_dom):
        if xml_dom.tagName != self.tagname:
            return

        for a in range(xml_dom.attributes.length):
            attr = xml_dom.attributes.item(a)
            self.init_prop(attr.nodeName, attr.nodeValue)

        en = bool_attrib(xml_dom, "enable", self.enable)
        tsize = int_attrib(xml_dom, "tsize", self.tile_size)
        psize = int_attrib(xml_dom, "psize", self.pixel_size)
        if en != self.enable or tsize != self.tile_size or psize != self.pixel_size:
            self.children.clear()
            self._enable = en
            self._tile_size = tsize
            self._pixel_size = psize
            self._reset()

        for tile_node in xml_dom.childNodes:
            if tile_node.tagName != "tile":
                continue

            id = str_attrib(tile_node, "id", None)
            if id is None:
                continue

            x, y = [int(v) for v in id.split(",")]
            bitmap = str_attrib(tile_node, "bitmap", None)

            if not bitmap:
                del self.children[id]
            else:
                if id in self.children:
                    self.children[id].set_from_dom(tile_node)
                else:
                    self.children[id] = fog_tile_msg(self, id)
                    self.children[id].set_prop("bitmap", bitmap)
            self._updated(x, y, bitmap)

    def _reset(self):
        if self._reset_hook:
            self._reset_hook()

    def _updated(self, x, y, bitmap):
        if self._updated_hook:
            if bitmap:
                texels = bytearray(base64.b64decode(bitmap))
            else:
                texels = None
            self._updated_hook(x, y, texels)
