# Copyright 2007 Mitchell N. Charity
# Copyright 2009 Walter Bender
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

import cairo

from util import mm, dimensions_mm, set_background_color


class ScreenOfCircles():

    def __init__(self, font, font_bold, w, h):
        self.font = font
        self.font_bold = font_bold
        self.w = w
        self.h = h

    def draw(self, c, dpi):

        set_background_color(c, self.w, self.h)
        c.set_antialias(cairo.ANTIALIAS_GRAY)

        nw, nh = dimensions_mm(dpi, self.w, self.h)

        def sq(x, y):
            c.rectangle(x, y, mm(dpi, 10), mm(dpi, 10))
            c.fill()
        
        w=nw
        h=nh
        for xm in range(0, w, 20):
            for ym in range(0, h, 20):
                sq(mm(dpi, xm), mm(dpi, ym))
        for xm in range(10, w, 20):
            for ym in range(10, h, 20):
                sq(mm(dpi, xm), mm(dpi, ym))

        c.set_line_width(1)
        c.move_to(mm(dpi, 100), 0)
        c.rel_line_to(0, mm(dpi, 100))
        c.rel_line_to(mm(dpi, -100), 0)
        c.stroke()

        c.set_line_width(3)
        v = 0.5
        c.set_source_rgb(v, v, v)
        c.move_to(mm(dpi, 50), 0)
        c.rel_line_to(0, mm(dpi, 100))
        c.move_to(0, mm(dpi, 50))
        c.rel_line_to(mm(dpi, 100), 0)
        c.stroke()
