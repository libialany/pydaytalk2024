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

from math import pi, sin, cos

import cairo

from util import mm, dimensions_mm, set_background_color, set_color, \
    get_hardware


def d2r(d):
    """ degrees to radians """
    return d / 180.0 * pi


class Angles90():

    def __init__(self, font, font_bold, w, h):
        self.font = font
        self.font_bold = font_bold
        self.w = w
        self.h = h
        self.hw = get_hardware()

    def draw(self, c, dpi):
        set_background_color(c, self.w, self.h)
        c.set_antialias(cairo.ANTIALIAS_GRAY)

        nw, nh = dimensions_mm(dpi, self.w, self.h)
        if self.hw[0:2] == 'xo':
            scale = 1.
        else:
            scale = 200./nh

        ox = mm(dpi, 0)
        oy = mm(dpi, 99 * scale)
        d = mm(dpi, 90 * scale)

        def xy(angle, m=d):
            return cos(-angle) * m + ox, sin(-angle) * m + oy

        def ray(angle, r0=0, r1=d):
            c.move_to(*xy(angle, r0))
            c.line_to(*xy(angle, r1))

        lw = 6
        c.set_line_width(lw)
        c.move_to(ox, oy + lw / 2)
        c.line_to(*xy(pi / 2))
        ray(0)
        c.stroke()

        c.save()
        c.set_line_width(3)
        c.set_dash([mm(dpi, 5)])
        ray(pi / 4)
        c.stroke()
        c.restore()

        c.set_line_width(4)
        for a in range(10, 81, 10):
            ray(d2r(a), mm(dpi, 10 * scale), mm(dpi, 85 * scale))
        c.stroke()
        c.set_line_width(2)
        for a in range(10, 81, 10):
            ray(d2r(a), mm(dpi, 3 * scale), mm(dpi, 20 * scale))
        c.stroke()

        c.set_line_width(2)
        for a in range(1, 90, 1):
            ray(d2r(a), mm(dpi, 70 * scale), mm(dpi, 80 * scale))
        c.stroke()
        c.set_line_width(2)
        for a in range(0, 90, 5):
            ray(d2r(a), mm(dpi, 20 * scale), mm(dpi, 81 * scale))
        c.stroke()


class Angles360():

    def __init__(self, font, font_bold, w, h):
        self.font = font
        self.font_bold = font_bold
        self.w = w
        self.h = h
        self.hw = get_hardware()

    def draw(self, c, dpi):
        set_background_color(c, self.w, self.h)
        c.set_antialias(cairo.ANTIALIAS_GRAY)

        nw, nh = dimensions_mm(dpi, self.w, self.h)
        if self.hw[0:2] == 'xo':
            scale = 1.
        else:
            scale = 200./nh

        ox = mm(dpi, nw / 2)
        oy = mm(dpi, nh / 2)
        d = mm(dpi, 44 * scale)

        def xy(angle, m=d):
            return cos(-angle) * m + ox, sin(-angle) * m + oy

        def ray(angle, r0=0, r1=d):
            c.move_to(*xy(angle, r0))
            c.line_to(*xy(angle, r1))

        def annulus(a0, a1, r0, r1):
            c.move_to(*xy(a0, r0))
            c.arc_to(ox, oy, r0, a0, a1)
            c.rel_line_to(*xy(a1, r1))
            c.arc_to(ox, oy, r1, a1, a0)
            c.close_path()

        def rays(step, r0=0, r1=d, w=1):
            c.save()
            c.set_line_width(w)
            for a in range(0, 360, step):
                ray(d2r(a), r0, r1)
            c.stroke()
            c.restore()

        rays(1, mm(dpi, 35 * scale), w=2, r1=mm(dpi, 43 * scale))
        rays(5, mm(dpi, 10 * scale), w=2)
        rays(10, mm(dpi, 10 * scale), w=4)
#        rays(10, mm(dpi, 3), mm(dpi, 20), w=2)
        c.save()
        #c.set_dash([mm(dpi, 5)])
        set_color(c, 'dark gray')
        rays(45, 0, mm(dpi, 45 * scale), w=6)
        c.restore()
        rays(90, 0, mm(dpi, 45 * scale), w=6)
