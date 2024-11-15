# Copyright 2007 Mitchell N. Charity
# Copyright 2009, 2012 Walter Bender
# Copyright 2012 Flavio Danesse
#
# This file is part of Ruler.
#
# Ruler is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ruler is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ruler.  If not, see <http://www.gnu.org/licenses/>

import os

from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import Pango
from gi.repository import PangoCairo

XO1 = 'xo1'
XO15 = 'xo1.5'
XO175 = 'xo1.75'
UNKNOWN = 'unknown'


def get_hardware():
    """ Determine whether we are using XO 1.0, 1.5, or "unknown" hardware """
    product = _get_dmi('product_name')
    if product is None:
        if os.path.exists('/etc/olpc-release') or \
           os.path.exists('/sys/power/olpc-pm'):
            return XO1
        elif os.path.exists('/sys/devices/platform/lis3lv02d/position'):
            return XO175  # FIXME: temporary check for XO 1.75
        else:
            return UNKNOWN
    if product != 'XO':
        return UNKNOWN
    version = _get_dmi('product_version')
    if version == '1':
        return XO1
    elif version == '1.5':
        return XO15
    else:
        return XO175


def _get_dmi(node):
    ''' The desktop management interface should be a reliable source
    for product and version information. '''
    path = os.path.join('/sys/class/dmi/id', node)
    try:
        return open(path).readline().strip()
    except:
        return None


def mm(dpi, n):
    """ Convert n pixels to units mm """
    return n / 25.40 * dpi


def dimensions_mm(dpi, w, h):
    """ Return screen width, height in units mm """
    return int(w * 25.40 / dpi), int(h * 25.40 / dpi)


def calc_dpi():
    xft_dpi = Gtk.Settings.get_default().get_property('gtk-xft-dpi')
    dpi = float(xft_dpi / 1024)
    return dpi, True

#
# Cairo-related utilities
#
def set_background_color(c, w, h):
    c.save()
    c.rectangle(0, 0, w, h)
    Gdk.cairo_set_source_color(c, Gdk.color_parse('white'))
    c.fill()
    c.restore()


def set_color(c, name):
    Gdk.cairo_set_source_color(c, Gdk.color_parse(name))


def write(c, text, name, size, centered=False, at_top=False):

    font = Pango.FontDescription(name)
    font.set_size(int(round(size * Pango.SCALE)))
    lo = PangoCairo.create_layout(c)
    lo.set_font_description(font)
    lo.set_text('X', -1)
    baseline_offset = lo.get_baseline() / Pango.SCALE
    if not at_top:
        c.rel_move_to(0, -baseline_offset)

    lo.set_font_description(font)
    lo.set_text(text, -1)
    if hasattr(lo, 'get_logical_extents'):
        extents = lo.get_logical_extents()
        ex = extents.get_width() / Pango.SCALE
    else:
        ex = size
        ex *= len(text)

    if centered:
        c.rel_move_to(-ex / 2, 0)
    PangoCairo.update_layout(c, lo)
    PangoCairo.show_layout(c, lo)
    c.rel_move_to(ex, 0)

    if not at_top:
        c.rel_move_to(0, -baseline_offset)
