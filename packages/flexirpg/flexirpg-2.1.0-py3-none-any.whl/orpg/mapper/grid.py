# Copyright (C) 2000-2001 The OpenRPG Project
#
#    openrpg-dev@lists.sourceforge.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# --
#
# File: mapper/gird.py
# Author: OpenRPG Team
# Maintainer:
# Version:
#   $Id: grid.py,v 1.29 2007/12/07 20:39:49 digitalxero Exp $
#
# Description:
#
__version__ = "$Id: grid.py,v 1.29 2007/12/07 20:39:49 digitalxero Exp $"

from orpg.mapper.base import *
from math import floor
from orpg.mapper.map_utils import *

# Grid mode constants
GRID_RECTANGLE = 0
GRID_HEXAGON = 1
LINE_NONE = 0
LINE_SOLID = 2

##-----------------------------
## grid layer
##-----------------------------
class grid_layer(layer_base):

    def __init__(self, canvas):
        layer_base.__init__(self)
        self.canvas = canvas
        self.unit_size = 100
        #unit_widest and unit_offset are for the Hex Grid only. these are mathmatics to figure out the exact center of the hex
        self.unit_widest = 100
        self.unit_offset = 100
        #size_ratio is the size ajustment for Hex to make them more accurate
        self.size_ratio = 1.5

        self.snap = True
        self.color = wx.Colour(wx.BLACK)
        self.mode = GRID_RECTANGLE
        self.line = LINE_NONE
        # Keep logic for different modes in different functions
        self.grid_hit_test = self.grid_hit_test_rect
        self.get_top_corner = self.get_top_corner_rect
        self.layerDraw = self.draw_rect

        self.isUpdated = True

    def get_unit_size(self):
        return self.unit_size

    def get_mode(self):
        return self.mode

    def get_color(self):
        return self.color

    def get_line_type(self):
        return self.line

    def is_snap(self):
        return self.snap

    def clear(self):
        pass

    def _snap_to_corner(self, pos, w, h):
        xl = floor((pos.x + self.unit_size/2)     / self.unit_size) * self.unit_size
        xr = floor((pos.x + self.unit_size/2 + w) / self.unit_size) * self.unit_size - w
        yt = floor((pos.y + self.unit_size/2)     / self.unit_size) * self.unit_size
        yb = floor((pos.y + self.unit_size/2 + h) / self.unit_size) * self.unit_size - h
        if abs(pos.x - xl) < abs(pos.x - xr):
            x = xl
        else:
            x = xr
        if abs(pos.y - yt) < abs(pos.y - yb):
            y = yt
        else:
            y = yb
        return cmpPoint(x, y)

    def get_snapped_to_pos(self, pos, width, height):
        """Return the position required to snap a miniature to the grid.

        pos: The position of the top-left corner of the miniature.
        width: Width of the miniature.
        height: Height of the miniature.

        The centre of the miniature will be snapped to the centre of
        the grid cell. The corners will also snap to the closest
        corner of rectangular grid squares.
        """
        centre = cmpPoint(pos.x + width//2, pos.y + height//2)
        grid_pos = self.grid_hit_test(centre)
        if grid_pos is not None:
            top_left = self.get_top_corner(grid_pos)#  get the top corner for this grid cell
            if self.mode == GRID_HEXAGON:
                x = top_left.x + (self.unit_size/1.75 - width) // 2
                y = top_left.y + (self.unit_size - height) // 2
            else:# GRID_RECTANGLE
                x = top_left.x + (self.unit_size - width) // 2
                y = top_left.y + (self.unit_size - height) //2
                corner = self._snap_to_corner(pos, width, height)
                corner_delta = distance_between(pos.x, pos.y, corner.x, corner.y)
                centre_delta = distance_between(pos.x, pos.y, x, y)
                if corner_delta < centre_delta:
                    return corner
            return cmpPoint(int(x), int(y))
        else:
            return pos

    def set_rect_mode(self):
        "switch grid to rectangular mode"
        self.mode = GRID_RECTANGLE
        self.grid_hit_test = self.grid_hit_test_rect
        self.get_top_corner = self.get_top_corner_rect
        self.layerDraw = self.draw_rect

    def set_hex_mode(self):
        "switch grid to hexagonal mode"
        self.mode = GRID_HEXAGON
        self.grid_hit_test = self.grid_hit_test_hex
        self.get_top_corner = self.get_top_corner_hex
        self.layerDraw = self.draw_hex
        self.unit_offset = sqrt(pow((self.unit_size/self.size_ratio ),2)-pow((self.unit_size/2),2))
        self.unit_widest = (self.unit_offset*2)+(self.unit_size/self.size_ratio )

    def grid_hit_test_rect(self,pos):
        "return grid pos (w,h) on rect map from pos"
        if self.unit_size and self.snap:
            return cmpPoint(floor(pos.x//self.unit_size), floor(pos.y//self.unit_size))
        else:
            return None

    def grid_hit_test_hex(self,pos):
        "return grid pos (w,h) on hex map from pos"
        if self.unit_size and self.snap:
            # rectangualr repeat patern is as follows (unit_size is the height of a hex)
            hex_side = int(self.unit_size/1.75)
            half_height = int(self.unit_size/2)
            height = int(self.unit_size)
            #_____
            #     \       /
            #      \_____/
            #      /     \
            #_____/       \
            col = int(pos.x/(hex_side*1.5))
            row = int(pos.y/height)
            (px, py) = (pos.x-(col*(hex_side*1.5)), pos.y-(row*height))
            # adjust for the odd columns' rows being staggered lower
            if col % 2 == 1:
                if py < half_height:
                    row = row - 1
                    py = py + half_height
                else:
                    py = py - half_height
            # adjust for top right corner
            if (px * height - py * hex_side) > height * hex_side:
                if col % 2 == 0:
                    row = row - 1
                col = col + 1
            # adjust for bottom right corner
            elif (px * height + py * hex_side) > 2 * height * hex_side:
                if col%2==1:
                    row = row + 1
                col = col + 1
            return cmpPoint(col, row)
        else:
            return None

    def get_top_corner_rect(self,grid_pos):
        "return upper left of a rect grid pos"
        if self.unit_size:
            return cmpPoint(grid_pos[0]*self.unit_size,grid_pos[1]*self.unit_size)
        else:
            return None

    def get_top_corner_hex(self,grid_pos):
        "return upper left of a hex grid pos"
        if self.unit_size:
            # We can get our x value directly, y is trickier
            temp_x = (((self.unit_size/1.75)*1.5)*grid_pos[0])
            temp_y = self.unit_size*grid_pos[1]
            # On odd columns we have to slide down slightly
            if grid_pos[0] % 2:
                temp_y += self.unit_size/2
            return cmpPoint(temp_x,temp_y)
        else:
            return None

    def set_grid(self, unit_size, snap, color, mode, line):
        self.unit_size = unit_size
        self.snap = snap
        self.color = color
        self.SetMode(mode)
        self.SetLine(line)
        self.isUpdated = True

    def SetLine(self,line):
        if line == LINE_NONE:
            self.line = LINE_NONE
        else:
            self.line = LINE_SOLID

    def SetMode(self, mode):
        if mode == GRID_RECTANGLE:
            self.set_rect_mode()
        elif mode == GRID_HEXAGON:
            self.set_hex_mode()

    def return_grid(self):
        return self.canvas.size

    def draw_rect(self, gc):
        if not self.unit_size:
            return

        if self.line == LINE_NONE:
            return

        gc.BeginLayer(0.5)

        pen = wx.Pen(self.color, 1, wx.SOLID)
        gc.SetPen(pen)

        s = self.unit_size
        sx, sy, w, h = gc.GetClipBox()
        ex = sx + w
        ey = sy + h

        x = floor(sx / s) * s
        while x < ex:
            gc.StrokeLine(x, sy, x, ey)
            x += s

        y = floor(sy / s) * s
        while y < ey:
            gc.StrokeLine(sx, y, ex, y)
            y += s

        gc.EndLayer()

    def draw_hex(self, gc):
        if self.unit_size == 0:
            return

        if self.line == LINE_NONE:
            return

        if self.line == LINE_SOLID:
            gc.SetPen(wx.Pen(self.color, 1, wx.SOLID))
        else:
            gc.SetPen(wx.Pen(self.color, 1, wx.DOT))

        A = self.unit_size/1.75 #Side Length
        B = self.unit_size #The width between any two sides
        D = self.unit_size/2 #The distance from the top to the middle of the hex
        C = self.unit_size/3.5 #The distance from the point of the hex to the point where the top line starts

        # <---A--><---A+2C----->
        # ___1____
        #         \            /  ^
        #          \2         /6  |
        #           \___4____/    |B=2D
        #           /        \    |
        #          /3         \5  |
        #         /            \  V

        path = gc.CreatePath()

        sx, sy, w, h = gc.GetClipBox()

        startx = floor(sx / (3*A)) * (3*A)
        starty = floor(sy / B) * B
        endx = sx + w
        endy = sy + h

        y = starty
        while y < endy:
            x = startx
            while x < endx:
                # (1)
                path.MoveToPoint(x, y)
                path.AddLineToPoint(x+A, y)
                # (2)
                path.AddLineToPoint(x+A+C, y+D)
                # (3)
                path.AddLineToPoint(x+A, y+B)
                # (4)
                path.MoveToPoint(x+A+C, y+D)
                path.AddLineToPoint(x+A+C+A, y+D)
                # (5)
                path.AddLineToPoint(x+A+C+A+C, y+B)
                # (6)
                path.MoveToPoint(x+A+C+A, y+D)
                path.AddLineToPoint(x+A+C+A+C, y)
                x += 3*A
            y += B
        gc.StrokePath(path)

    def layerToXML(self,action = "update"):
        xml_str = "<grid"

        if self.color != None:
            xml_str += " color='" + self.color.GetAsString(wx.C2S_HTML_SYNTAX) + "'"

        if self.unit_size != None:
            xml_str += " size='" + str(self.unit_size) + "'"

        if self.snap != None:
            if self.snap:
                xml_str += " snap='1'"
            else:
                xml_str += " snap='0'"

        if self.mode != None:
            xml_str+= "  mode='" + str(self.mode) + "'"

        if self.line != None:
            xml_str+= " line='" + str(self.line) + "'"

        xml_str += "/>"

        if (action == "update" and self.isUpdated) or action == "new":
            self.isUpdated = False
            return xml_str
        else:
            return ''


    def layerTakeDOM(self, xml_dom):
        if xml_dom.hasAttribute("color"):
            self.color.Set(xml_dom.getAttribute("color"))

        if xml_dom.hasAttribute("mode"):
            self.SetMode(int(xml_dom.getAttribute("mode")))

        if xml_dom.hasAttribute("size"):
            self.unit_size = int(xml_dom.getAttribute("size"))

        if xml_dom.hasAttribute("snap"):
            if (xml_dom.getAttribute("snap") == 'True') or (xml_dom.getAttribute("snap") == "1"):
                self.snap = True
            else:
                self.snap = False

        if xml_dom.hasAttribute("line"):
            self.SetLine(int(xml_dom.getAttribute("line")))
