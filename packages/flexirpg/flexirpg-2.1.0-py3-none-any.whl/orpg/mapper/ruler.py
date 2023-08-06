"""Ruler (measurement) layer."""

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

__copyright__ = "Copyright 2023 David Vrabel"

import math

from orpg.config import Settings
from orpg.lib.xmlutil import float_attrib, int_attrib, str_attrib
from .base import *
from .map_utils import distance_between
from .pathfinder import PathfinderPath
from .units import *

class Ruler:
    line_color = Settings.define("map.ruler.line_color", wx.Colour(0, 0, 64, 255))
    square_color = Settings.define("map.ruler.square_color", wx.Colour(0, 0, 192, 64))
    font = Settings.define("map.ruler.font", "")
    font_size = Settings.define("map.ruler.font_size", 10)

    def __init__(self, layer, start_pos):
        self.layer = layer
        start_pos = self._snap(start_pos)
        self.points = [start_pos, start_pos]

        self.panel_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK)
        self.border_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK).ChangeLightness(75)
        self.text_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOTEXT)
        self.font = wx.Font(self.font_size.value, wx.FONTFAMILY_DEFAULT,
                            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False,
                            self.font.value)

    @property
    def geometric_distance(self):
        d = 0.0
        for i in range(1, len(self.points)):
            a = self.points[i-1]
            b = self.points[i]
            d += distance_between(a.x, a.y, b.x, b.y)
        return d

    def add_point(self, pos):
        self.points.append(self._snap(pos))

    def move_point(self, pos):
        self.points[-1] = self._snap(pos)

    def draw(self, gc):
        gc.SetPen(wx.Pen(self.line_color.value, 1, wx.SOLID))
        gc.StrokeLines(self.points)

        if self.layer.method == MeasurementMethod.PATHFINDER:
            squares = PathfinderPath(self.points, self.layer.grid_size)
            path = gc.CreatePath()
            for square in squares.unique_squares():
                path.AddRectangle(square.x * self.layer.grid_size, square.y * self.layer.grid_size,
                                  self.layer.grid_size, self.layer.grid_size)
            gc.SetBrush(wx.Brush(self.square_color.value))
            gc.FillPath(path)
            distance = squares.distance * self.layer.grid_size
        else:
            distance = self.geometric_distance

        self._draw_distance_panel(gc, distance * self.layer.scale)

    def _draw_distance_panel(self, gc, distance):
        gc.SetBrush(wx.Brush(self.panel_color))
        gc.SetPen(wx.Pen(self.border_color, 1, wx.SOLID))
        gc.SetFont(self.font, self.text_color)

        pos = self.points[-1]
        text = f"{distance:.1f} {self.layer.units.symbol}"
        width, height = gc.GetTextExtent(text)

        if self.layer.method == MeasurementMethod.PATHFINDER:
            offset = self.layer.grid_size // 2 + 1
        else:
            offset = 2

        gc.DrawRectangle(pos.x + offset, pos.y + offset, width + 4, height + 4)
        gc.DrawText(text, pos.x + offset + 2, pos.y + offset + 2)

    def _snap(self, point):
        if self.layer.method == MeasurementMethod.PATHFINDER:
            s = self.layer.grid_size
            return wx.Point2D((math.floor(point.x / s) + 0.5) * s,
                              (math.floor(point.y / s) + 0.5) * s)
        return point


class ruler_layer(layer_base):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

        self.scale = 0.25 # per pixel
        self.units = Units.FEET
        self.method = MeasurementMethod.PATHFINDER
        self.isUpdated = True

        self.active_ruler = None

    def set_scale(self, scale, units, method):
        self.scale = scale
        self.units = units
        self.method = method
        self.isUpdated = True

    @property
    def grid_size(self):
        return self.canvas.layers["grid"].unit_size

    def layerDraw(self, gc):
        if self.active_ruler:
            self.active_ruler.draw(gc)

    def layerToXML(self, action="update"):
        if action == "update" and not self.isUpdated:
            return ""

        xml_str = f"<ruler scale='{self.scale}' units='{self.units.value}' method='{self.method.value}'>"
        xml_str += "</ruler>"

        return xml_str

    def layerTakeDOM(self, xml_dom):
        self.scale = float_attrib(xml_dom, "scale", self.scale)
        self.units = Units(int_attrib(xml_dom, "units", self.units))
        self.method = MeasurementMethod(int_attrib(xml_dom, "method", self.method))

    def add_ruler_point(self, pos):
        if self.active_ruler:
            self.active_ruler.add_point(pos)
        else:
            ruler = Ruler(self, pos)
            self.active_ruler = ruler
        self.canvas.Refresh()

    def move_ruler_point(self, pos):
        if self.active_ruler:
            self.active_ruler.move_point(pos)
            self.canvas.Refresh()

    def cancel_ruler(self):
        if self.active_ruler:
            self.active_ruler = None
            self.canvas.Refresh()
            return True
        return False
