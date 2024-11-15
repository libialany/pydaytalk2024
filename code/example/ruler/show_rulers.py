# Copyright 2007 Mitchell N. Charity
# Copyright 2009 Walter Bender
# Copyright 2013 Aneesh Dogra <lionaneesh@gmail.com>
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

from gettext import gettext as _

import cairo

from util import mm, dimensions_mm, set_background_color, write, get_hardware


class ScreenOfRulers():
    def __init__(self, font, font_bold, w, h):
        self.font = font
        self.font_bold = font_bold
        self.w = w
        self.h = h
        self.custom_unit_in_mm = 24.5 # precise upto 2 decimal places
        self.hw = get_hardware()
        self.offset_of_xo_side_from_screen = 0
        self.dpi = 0
        self.c = None

    def draw(self, c, dpi):
        self.c = c
        self.dpi = dpi
        set_background_color(c, self.w, self.h)

        nw, nh = dimensions_mm(dpi, self.w, self.h)
        c.set_antialias(cairo.ANTIALIAS_GRAY)

        self.draw_ruler_pair(c, dpi, mm(dpi, 20))

        # Only calculate offsets if on an OLPC XO-1, 1.5, 1.75
        # Not applicable to XO 3.0
        if self.hw[0:2] == 'xo' and dpi in [200, 201]:
            self.offset_of_xo_side_from_screen = mm(dpi, -38.5)
            c.move_to(self.offset_of_xo_side_from_screen,  mm(dpi, 65))
            self.draw_cm_ruler(c, dpi, 180)
            
            c.save()
            c.move_to(mm(dpi, 20), mm(dpi, 75))
            write(c, _('Use this ruler from the outside edge of the computer.'),
                  self.font, mm(dpi, 4))
            c.restore()

            offset_of_molding_from_screen = mm(dpi, -0.4)
            c.move_to(offset_of_molding_from_screen,  mm(dpi, 95))
            self.draw_cm_ruler(c, dpi, 150)
            self.draw_custom_ruler(self.custom_unit_in_mm, int(nw / 10 * 10))

        else:
            self.offset_of_xo_side_from_screen = mm(dpi, int(nw / 20))
            c.move_to(self.offset_of_xo_side_from_screen,  mm(dpi, 65))
            self.draw_cm_ruler(c, dpi, int(nw / 11 * 10))
            self.draw_custom_ruler(self.custom_unit_in_mm, int(nw / 11 * 10))
            
    def draw_ruler_pair(self, c, dpi, y):
        c.move_to(mm(dpi, 10), y)
        self.connect_rulers(c, dpi)

        c.move_to(mm(dpi, 10), y)
        self.draw_cm_ruler(c, dpi)

        c.move_to(mm(dpi, 10), y+mm(dpi, 10))
        self.draw_mm_ruler(c, dpi)
        
    def connect_rulers(self, c, dpi):
        c.save()
        c.set_line_cap(cairo.LINE_CAP_SQUARE)
        c.translate(*c.get_current_point())

        c.set_line_width(1)
        for xm in range(0, 130+1, 10):
            c.move_to(mm(dpi, xm), 0)
            c.rel_line_to(0, mm(dpi, 10))
        c.stroke()

        c.set_line_width(2)
        c.move_to(0, 0)
        c.rel_line_to(0, mm(dpi, 10))
        c.stroke()

        c.restore()

    # units_per_mm is precise upto 2 decimal places
    def draw_custom_ruler(self, units_per_mm, width=130):
        if not self.c:
            return

        self.c.set_source_rgb(255, 255, 255)
        self.c.rectangle(0, mm(self.dpi, 85),
                    width, mm(self.dpi, 85) + 10)
        self.c.fill()
        self.c.set_source_rgb(0, 0, 0)

        self.c.move_to(self.offset_of_xo_side_from_screen,  mm(self.dpi, 85))
        self.c.save()
        self.c.set_line_cap(cairo.LINE_CAP_SQUARE)
        self.c.translate(*self.c.get_current_point())

        self.c.set_line_width(5)
        self.c.move_to(0, 0)
        self.c.line_to(mm(self.dpi, width), 0)
        for x in [mm(self.dpi, xm / 100.) for xm in range(
                0, (width + 1) * 100, int(units_per_mm * 100))]:
            self.c.move_to(x, 0)
            self.c.rel_line_to(0, mm(self.dpi, -3))
        self.c.stroke()
        pt_list = [x / int(units_per_mm * 100) for x in \
                   range(0, (width + 1) * 100, int(units_per_mm * 100))]
        coord_list = [mm(self.dpi, xm / 100) for xm in range(
                0, (width + 1) * 100, int(units_per_mm * 100))]

        if units_per_mm > 7:  # Avoid overlapping labels
            for a in range(0, len(coord_list)):
                xm = pt_list[a]
                x = coord_list[a]
                n = xm
                self.c.move_to(x, mm(self.dpi, -4))
                write(self.c, "%d" % n, self.font_bold, mm(self.dpi, 2.5),
                      centered=True)

        self.c.restore()


    def draw_cm_ruler(self, c, dpi, width=130):
        c.save()
        c.set_line_cap(cairo.LINE_CAP_SQUARE)
        c.translate(*c.get_current_point())

        c.set_line_width(5)
        c.move_to(0, 0)
        c.line_to(mm(dpi, width), 0)
        for x in [mm(dpi, xm) for xm in range(0, width+1, 10)]:
            c.move_to(x, 0)
            c.rel_line_to(0, mm(dpi, -3))
        c.stroke()

        for x, xm in [(mm(dpi, xm), xm) for xm in range(0, width+1, 10)]:
            n = xm/10
            c.move_to(x, mm(dpi, -4))
            write(c, "%d" % n, self.font_bold, mm(dpi, 2.5), centered=True)
            
        c.move_to(mm(dpi, 1.5), mm(dpi, -4))
        write(c, "cm", self.font_bold, mm(dpi, 2))

        c.restore()

    def draw_mm_ruler(self, c, dpi, width=130):
        c.save()
        c.set_line_cap(cairo.LINE_CAP_SQUARE)
        c.translate(*c.get_current_point())

        c.move_to(0, 0)
        c.set_line_width(4)
        c.line_to(mm(dpi, width), 0)
        for x in [mm(dpi, xm) for xm in range(0, width+1, 10)]:
            c.move_to(x, 0)
            c.rel_line_to(0, mm(dpi, 3))
        c.stroke()

        c.set_line_width(3)
        for x in [mm(dpi, xm) for xm in range(0, width, 5)]:
            c.move_to(x, 0)
            c.rel_line_to(0, mm(dpi, 2.2))
        for x in [mm(dpi, xm) for xm in range(0, width, 1)]:
            c.move_to(x, 0)
            c.rel_line_to(0, mm(dpi, 2))
        c.stroke()

        base = mm(dpi, 7)
        for x, xm in [(mm(dpi, xm), xm) for xm in range(0, width+1, 10)]:
            c.move_to(x, base)
            write(c, "%d" % xm, self.font, mm(dpi, 2), centered=True)
            
        c.move_to(mm(dpi, 1.2), base)
        write(c, "mm", self.font, mm(dpi, 1.5))

        c.restore()

