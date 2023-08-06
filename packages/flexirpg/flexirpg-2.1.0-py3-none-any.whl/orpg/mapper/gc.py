# Helpers for drawing to graphic contexts.
#
# Copyright 2023 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import contextlib


@contextlib.contextmanager
def AntialiasMode(gc, mode):
    orig_mode = gc.AntialiasMode
    gc.AntialiasMode = mode
    yield
    gc.AntialiasMode = orig_mode

@contextlib.contextmanager
def CompositionMode(gc, mode):
    orig_mode = gc.CompositionMode
    gc.CompositionMode = mode
    yield
    gc.CompositionMode = orig_mode
