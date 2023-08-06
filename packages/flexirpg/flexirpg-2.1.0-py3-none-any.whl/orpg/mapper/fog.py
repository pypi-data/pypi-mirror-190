# Fog map layer
#
# Copyright (C) 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from ctypes import *
from itertools import product
from math import ceil, floor

import wx

from orpg.mapper.base import *
from orpg.mapper.fog_msg import fog_msg
from orpg.networking.roles import *
from .gc import *

class fog_tile:
    def __init__(self, fog, x, y):
        self.x = x
        self.y = y
        self._tile_size = fog.fog.tile_size
        self._pixel_size = fog.fog.pixel_size
        self._visible_size = fog.fog.tile_visible_size
        self.texels = None

    def set(self, p, hide):
        if bool(self._texels[p]) != hide:
            self._texels[p] = 0xff if hide else 0
            self._update_rectangles()
            return True
        else:
            return False

    @property
    def texels(self):
        return self._texels

    @texels.setter
    def texels(self, texels):
        if texels is None:
            self._texels = bytearray(b"\xff" * (self._tile_size ** 2))
            self._rectangles = [wx.Rect(0, 0, self._tile_size, self._tile_size)]
        else:
            self._texels[:] = texels
            self._update_rectangles()

    def draw(self, gc):
        path = gc.CreatePath()
        for r in self._rectangles:
            path.AddRectangle(self.x * self._visible_size + r.X * self._pixel_size,
                              self.y * self._visible_size + r.Y * self._pixel_size,
                              r.Width * self._pixel_size,
                              r.Height * self._pixel_size)
        gc.FillPath(path)

    def _update_rectangles(self):
        self._rectangles = []
        for y in range(self._tile_size):
            prev_v = 0
            for x in range(self._tile_size):
                v = self._texels[x + y * self._tile_size]
                if v == prev_v:
                    continue
                if v:
                    self._push_start(x, y)
                else:
                    self._push_end(x, y)
                prev_v = v
            if prev_v:
                self._push_end(x + 1, y)

    def _push_start(self, x, y):
        self._rectangles.append(wx.Rect(x, y, 1, 1))

    def _push_end(self, x, y):
        self._rectangles[-1].Width = x - self._rectangles[-1].X

class fog_layer(layer_base):
    def __init__(self, canvas):
        layer_base.__init__(self)
        self.canvas = canvas
        self.fog = fog_msg(reset_hook=self._reset_hook, updated_hook=self._updated_hook)
        self._tiles = {} # indexed by (x, y) of corner

    def clear(self):
        self.fog.enable = False

    @property
    def enable(self):
        return self.fog.enable

    @enable.setter
    def enable(self, state):
        self.fog.enable = state
        self.send_updates()

    def set_pixel_size(self, psize):
        self.fog.pixel_size = psize
        self.send_updates()

    def add(self, pos):
        self._set_pixel(pos, True)

    def remove(self, pos):
        self._set_pixel(pos, False)

    def tile(self, x, y):
        try:
            tile = self._tiles[x, y]
        except KeyError:
            tile = fog_tile(self, x, y)
            self._tiles[x, y] = tile
        return tile

    def layerDraw(self, gc):
        if not self.fog.enable:
            return

        session = self.canvas.frame.session
        if session.allowed(ROLE_GM):
            opacity = 0.5
        else:
            opacity = 1.0
        gc.BeginLayer(opacity)
        gc.SetBrush(wx.Brush(wx.BLACK))

        with AntialiasMode(gc, wx.ANTIALIAS_NONE):
            for tile in self.visible_tiles():
                tile.draw(gc)

        gc.EndLayer()

    def layerToXML(self, action="update"):
        if action == "update":
            s = self.fog.get_changed_xml(action)
        else:
            s = self.fog.get_all_xml(action)
        return s

    def layerTakeDOM(self, xml_dom):
        self.fog.set_from_dom(xml_dom)

    def _reset_hook(self):
        self._tiles.clear()

    def _updated_hook(self, x, y, texels):
        self.tile(x, y).texels = texels

    def _set_pixel(self, pos, hide):
        pos_x = floor(pos.x / self.fog.pixel_size)
        pos_y = floor(pos.y / self.fog.pixel_size)
        tsize = self.fog.tile_size
        tpos_x = pos_x // tsize
        tpos_y = pos_y // tsize
        ppos_x = pos_x % tsize
        ppos_y = pos_y % tsize

        tile = self.tile(tpos_x, tpos_y)
        if tile.set(ppos_x + ppos_y * tsize, hide):
            self.fog.set_bitmap(tpos_x, tpos_y, tile.texels)
            self.send_updates()

    def visible_tiles(self):
        """Iterate over all fog tiles that are visible in the current viewport."""
        size = self.fog.tile_visible_size
        def tile_range(d1, d2):
            return range(floor(d1 / size), ceil(d2 / size))
        p1, p2 = self.canvas.get_visible_area()
        for x, y in product(tile_range(p1.x, p2.x), tile_range(p1.y, p2.y)):
            yield self.tile(x, y)
