"""Pathfinder specific rule support for the map."""

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

__copyright__ = "Copyright 2023 David Vrabel"

from collections import namedtuple
import math


Square = namedtuple("Square", ["x", "y"])

class PathfinderPath:
   def __init__(self, points, grid_size):
      self._grid_size = grid_size
      self._squares = []
      self._prev_square = None
      self._distance = 0
      self._diagonals = 0
      self._lines_to_squares(points)
      self._unique_squares = set(self._squares)

   @property
   def distance(self):
      return self._distance

   def unique_squares(self):
      for square in self._unique_squares:
         yield square

   def _lines_to_squares(self, points):
      for i in range(1, len(points)):
         p0 = points[i-1]
         p1 = points[i]

         x0 = math.floor(p0.x / self._grid_size)
         y0 = math.floor(p0.y / self._grid_size)
         x1 = math.floor(p1.x / self._grid_size)
         y1 = math.floor(p1.y / self._grid_size)

         self._line(x0, y0, x1, y1)

   def _line(self, x0, y0, x1, y1):
      if abs(y1 - y0) < abs(x1 - x0):
         return self._line_low(x0, y0, x1, y1)
      else:
         return self._line_high(x0, y0, x1, y1)

   def _line_low(self, x0, y0, x1, y1):
      dx = abs(x1 - x0)
      dy = abs(y1 - y0)
      xi = 1 if x0 < x1 else -1
      yi = 1 if y0 < y1 else -1
      D = 2*dy - dx
      y = y0

      for x in range(x0, x1 + xi, xi):
         self._add_square(Square(x, y))
         if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
         else:
            D = D + 2*dy

   def _line_high(self, x0, y0, x1, y1):
      dx = abs(x1 - x0)
      dy = abs(y1 - y0)
      xi = 1 if x0 < x1 else -1
      yi = 1 if y0 < y1 else -1
      D = (2 * dx) - dy

      x = x0
      for y in range(y0, y1 + yi, yi):
         self._add_square(Square(x, y))
         if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
         else:
            D = D + 2*dx

   def _add_square(self, square):
      if square == self._prev_square:
         return
      if self._prev_square:
         self._distance += 1
         if square.x != self._prev_square.x and square.y != self._prev_square.y:
            self._distance += self._diagonals & 1
            self._diagonals += 1
      self._squares.append(square)
      self._prev_square = square
