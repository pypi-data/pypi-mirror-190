# Utilities for managing bitmaps
#
# Copyright 2010,2020 David Vrabel
#

import wx

from orpg.config import Paths


def create_from_file(filename):
    return wx.Bitmap(Paths.image(filename))

class ColorIcon:
    """Generate bitmaps color picker icons from a template image."""

    key_color = wx.Colour(255, 0, 255) # Magenta

    def __init__(self, template_filename: str):
        template_path = Paths.image(template_filename)
        self.image = wx.Image(template_path, type=wx.BITMAP_TYPE_PNG)

    def bitmap(self, color: wx.Colour):
        """Return a new bitmap for 'color', using the template."""
        colored_image = self.image.Copy()
        colored_image.Replace(
            self.key_color.Red(), self.key_color.Green(), self.key_color.Blue(),
            color.Red(), color.Green(), color.Blue())
        return colored_image.ConvertToBitmap()
