# Copyright 2007 Mitchell N. Charity
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

from util import mm, dimensions_mm, set_background_color, write


class ScreenGrid_mm():

    def __init__(self, font, font_bold, w, h):
        self.font = font
        self.font_bold = font_bold
        self.w = w
        self.h = h

    def draw(self, c, dpi):
        set_background_color(c, self.w, self.h)
        nw, nh = dimensions_mm(dpi, self.w, self.h)
        draw_numbers(self, c, dpi, nw, nh, 10, "mm")
        draw_grid(c, dpi, 1, 1, nw, nh)
        draw_grid(c, dpi, 10, 2, nw, nh)
        draw_grid(c, dpi, 100, 3.5, nw, nh)


class ScreenGrid_cm():

    def __init__(self, font, font_bold, w, h):
        self.font = font
        self.font_bold = font_bold
        self.w = w
        self.h = h

    def draw(self, c, dpi):
        set_background_color(c, self.w, self.h)
        nw, nh = dimensions_mm(dpi, self.w, self.h)
        c.set_antialias(cairo.ANTIALIAS_GRAY)
        draw_numbers(self, c, dpi, nw, nh)
        draw_grid(c, dpi, 10, 2, nw, nh)
        draw_grid(c, dpi, 100, 3.5, nw, nh)


def draw_numbers(p, c, dpi, nw, nh, m=1, unit="cm"):
    c.save()
    v = 0.7
    c.set_source_rgb(v, v, v)
    for n in range(1, 11):
        c.move_to(mm(dpi, n * 10), mm(dpi, n * 10))
        c.rel_move_to(mm(dpi, 0), mm(dpi, 3))
        write(c, "%d" % (n * m), p.font, mm(dpi, 4), centered=True)
        if n == 1:
            c.rel_move_to(mm(dpi, -0.5), mm(dpi, -0.5))
            write(c, " "+unit, p.font, mm(dpi, 3))
    c.restore()


def draw_grid(c, dpi, step, stroke, nw, nh):

    c.save()
    c.set_line_width(stroke)
    lay_mm_grid(c, dpi, width_mm=nw, height_mm=nh, step_mm=step)
    c.stroke()
    c.restore()


def lay_mm_grid(c, dpi, width_mm=152, height_mm=114, step_mm=1):

    c.save()
    z = mm(dpi, 1)
    c.scale(z, z)
    for x in range(0, width_mm, step_mm):
        c.move_to(x, 0)
        c.rel_line_to(0, height_mm)
    for y in range(0, height_mm, step_mm):
        c.move_to(0, y)
        c.rel_line_to(width_mm, 0)
    c.restore()
