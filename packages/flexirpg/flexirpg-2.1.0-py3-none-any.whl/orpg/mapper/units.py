"""Measurement units."""

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

__copyright__ = "Copyright 2023 David Vrabel"


from enum import Enum

class Units(Enum):
    METRES = 0
    SQUARES = 1
    FEET = 2

    def __str__(self):
        return self.name.lower()

    @property
    def symbol(self):
        _symbols = {
            self.METRES: 'm',
            self.SQUARES: 'sq',
            self.FEET: 'ft',
        }
        return _symbols[self]

class MeasurementMethod(Enum):
    GEOMETRIC = 0
    PATHFINDER = 1

    def __str__(self):
        return self.name.capitalize()
