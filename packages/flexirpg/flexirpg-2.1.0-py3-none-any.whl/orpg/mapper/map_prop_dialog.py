# Copyright (C) 2000-2001 The OpenRPG Project
#
#    openrpg-dev@lists.sourceforge.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from orpg.config import Settings
from orpg.mapper.background import *
from orpg.mapper.grid import *
from orpg.mapper.whiteboard import *
import orpg.lib.ui as ui
from orpg.main import image_library
from .units import *

##-----------------------------
## map prop dialog
##-----------------------------

CTRL_BG_COLOR_VALUE = wx.NewId()
CTRL_IMAGE = wx.NewId()
CTRL_IMAGE_SELECT = wx.NewId()
CTRL_GRID = wx.NewId()
CTRL_GRID_SNAP = wx.NewId()
CTRL_GRID_COLOR = wx.NewId()
CTRL_GRID_MODE_RECT = wx.NewId()
CTRL_GRID_MODE_HEX = wx.NewId()
CTRL_GRID_SHOW_LINES = wx.NewId()
CTRL_RULER_SCALE = wx.NewId()
CTRL_RULER_UNITS = wx.NewId()
CTRL_RULER_METHOD = wx.NewId()

class general_map_prop_dialog(wx.Dialog):

    last_directory = Settings.define("map.background.last_directory", "")

    def __init__(self, parent, layers):
        wx.Dialog.__init__(self,parent,-1,"General Map Properties",wx.DefaultPosition)
        self.layers = layers
        self.image = self.layers["bg"].image

        #build controls
        self.ctrls = {  CTRL_BG_COLOR_VALUE : ui.ColorSelectorButton(self, tooltip="Background Color"),
                        CTRL_IMAGE : wx.CheckBox(self, CTRL_IMAGE, "Image", style=wx.ALIGN_RIGHT),
                        CTRL_IMAGE_SELECT : wx.Button(self, CTRL_IMAGE_SELECT, "Select"),
                        CTRL_GRID : wx.TextCtrl(self, CTRL_GRID),
                        CTRL_GRID_SNAP : wx.CheckBox(self, CTRL_GRID_SNAP, " Snap to grid"),
                        CTRL_GRID_COLOR : ui.ColorSelectorButton(self, tooltip="Grid Color"),
                        CTRL_GRID_MODE_RECT : wx.RadioButton(self, CTRL_GRID_MODE_RECT, "Rectangular", style=wx.RB_GROUP),
                        CTRL_GRID_MODE_HEX : wx.RadioButton(self, CTRL_GRID_MODE_HEX, "Hexagonal"),
                        CTRL_GRID_SHOW_LINES : wx.CheckBox(self, CTRL_GRID_SHOW_LINES, "Show Lines"),
                        CTRL_RULER_SCALE : wx.TextCtrl(self, CTRL_RULER_SCALE),
                        CTRL_RULER_UNITS : wx.Choice(self, CTRL_RULER_UNITS,
                                                    choices=[f"{str(u)} ({u.symbol})" for u in Units]),
                        CTRL_RULER_METHOD : wx.Choice(self, CTRL_RULER_METHOD,
                                                    choices=[f"{str(m)}" for m in MeasurementMethod]),
                     }

        # Set background layer control values
        self.ctrls[CTRL_BG_COLOR_VALUE].color = layers["bg"].bg_color
        self.ctrls[CTRL_IMAGE].SetValue(self.image != None)
        self.ctrls[CTRL_IMAGE_SELECT].Enabled = self.ctrls[CTRL_IMAGE].IsChecked()

        # set grid layer control values
        self.ctrls[CTRL_GRID].SetValue(str(layers["grid"].unit_size))
        self.ctrls[CTRL_GRID_SNAP].SetValue(layers["grid"].snap)
        self.ctrls[CTRL_GRID_COLOR].color = layers["grid"].color
        self.ctrls[CTRL_GRID_MODE_RECT].SetValue(layers["grid"].mode == GRID_RECTANGLE)
        self.ctrls[CTRL_GRID_MODE_HEX].SetValue(layers["grid"].mode == GRID_HEXAGON)
        self.ctrls[CTRL_GRID_SHOW_LINES].SetValue(layers["grid"].line != LINE_NONE)
        self.ctrls[CTRL_RULER_SCALE].SetValue(str(layers["ruler"].scale * layers["grid"].unit_size))
        self.ctrls[CTRL_RULER_UNITS].SetSelection(layers["ruler"].units.value)
        self.ctrls[CTRL_RULER_METHOD].SetSelection(layers["ruler"].method.value)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Background
        vbox.Add(ui.StaticTextHeader(self, label="Background"))
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((12, 0))

        hbox.Add(self.ctrls[CTRL_BG_COLOR_VALUE])
        hbox.Add((12, 0))
        hbox.Add(self.ctrls[CTRL_IMAGE], 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add((6, 0))
        hbox.Add(self.ctrls[CTRL_IMAGE_SELECT], 0, wx.ALIGN_CENTER_VERTICAL)

        vbox.Add(hbox, 0, wx.EXPAND)
        vbox.Add((0, 12))

        # Grid
        vbox.Add(ui.StaticTextHeader(self, label="Grid"))
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((12, 0))
        sizer = wx.FlexGridSizer(0, 3, 10, 10)
        sizer.AddGrowableCol(0, 1)
        sizer.AddGrowableCol(1, 1)
        sizer.AddGrowableCol(2, 1)
        sizer.AddMany([(wx.StaticText(self, -1, "Pixels per Square"), 0, wx.ALIGN_CENTER_VERTICAL),
                       (self.ctrls[CTRL_GRID], 0, wx.ALIGN_CENTER_VERTICAL),
                       (0, 0),
                       (self.ctrls[CTRL_GRID_SNAP]),
                       (self.ctrls[CTRL_GRID_MODE_RECT]),
                       (self.ctrls[CTRL_GRID_MODE_HEX]),
                       (self.ctrls[CTRL_GRID_SHOW_LINES], 0, wx.ALIGN_CENTER_VERTICAL),
                       (self.ctrls[CTRL_GRID_COLOR]),
                       (0, 0),
                   ])
        hbox.Add(sizer, 1, wx.EXPAND)
        vbox.Add(hbox, 0, wx.EXPAND)
        vbox.Add((0, 12))

        # Ruler
        vbox.Add(ui.StaticTextHeader(self, label="Measurements"))
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((12, 0))
        sizer = wx.FlexGridSizer(0, 3, 10, 10)
        sizer.AddGrowableCol(0, 1)
        sizer.AddGrowableCol(1, 1)
        sizer.AddGrowableCol(2, 1)
        sizer.AddMany([(wx.StaticText(self, -1, "Scale"), 0, wx.ALIGN_CENTER_VERTICAL),
                       (self.ctrls[CTRL_RULER_SCALE], 1, wx.EXPAND),
                       (self.ctrls[CTRL_RULER_UNITS]),
                       (wx.StaticText(self, -1, "Method"), 0, wx.ALIGN_CENTER_VERTICAL),
                       (self.ctrls[CTRL_RULER_METHOD]),
                       (0, 0),
                   ])
        hbox.Add(sizer, 1, wx.EXPAND)
        vbox.Add(hbox, 0, wx.EXPAND)
        vbox.Add((0, 12))

        bbox = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        vbox.Add(bbox, 0, wx.EXPAND)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(vbox, 1, wx.EXPAND | wx.ALL, border = 12)

        self.SetSizer(box)
        box.Layout()
        box.Fit(self)

        #event handlers
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=self.GetAffirmativeId())
        self.Bind(wx.EVT_CHECKBOX, self.on_image_checkbox, id=CTRL_IMAGE)
        self.Bind(wx.EVT_BUTTON, self.on_image_select, id=CTRL_IMAGE_SELECT)

    def on_image_checkbox(self, evt):
        self.ctrls[CTRL_IMAGE_SELECT].Enabled = self.ctrls[CTRL_IMAGE].IsChecked()
        if not self.ctrls[CTRL_IMAGE].IsChecked():
            self.image = None

    def on_image_select(self, evt):
        d = wx.FileDialog(self.GetParent(), "Select Background Image",
                          self.last_directory.value, "",
                          "Images (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg",
                          wx.FD_OPEN)
        if d.ShowModal() == wx.ID_OK:
            self.last_directory.value = d.GetDirectory()
            self.image = image_library.get_from_file(d.GetPath())
        d.Destroy()


    def on_ok(self,evt):
        # Background
        self.layers["bg"].clear()
        self.layers["bg"].set_color(self.ctrls[CTRL_BG_COLOR_VALUE].color)
        if self.image:
            self.layers["bg"].set_image(self.image)

        # Grid
        grid_size = int(self.ctrls[CTRL_GRID].GetValue())
        if self.ctrls[CTRL_GRID_MODE_RECT].GetValue() == True:
            grid_mode = GRID_RECTANGLE
        else:
            grid_mode = GRID_HEXAGON
        if self.ctrls[CTRL_GRID_SHOW_LINES].GetValue():
            grid_line = LINE_SOLID
        else:
            grid_line = LINE_NONE
        self.layers["grid"].set_grid(grid_size,
                                 self.ctrls[CTRL_GRID_SNAP].GetValue(),
                                 self.ctrls[CTRL_GRID_COLOR].color,
                                 grid_mode,
                                 grid_line)
        self.layers["fog"].set_pixel_size(grid_size)

        # Ruler
        try:
            scale = float(self.ctrls[CTRL_RULER_SCALE].GetValue()) / grid_size
        except ValueError:
            scale = self.layers["ruler"].scale
        units = Units(self.ctrls[CTRL_RULER_UNITS].GetSelection())
        method = MeasurementMethod(self.ctrls[CTRL_RULER_METHOD].GetSelection())
        self.layers["ruler"].set_scale(scale, units, method)

        self.EndModal(wx.ID_OK)
