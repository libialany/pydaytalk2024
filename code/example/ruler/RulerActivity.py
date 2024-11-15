# Copyright (c) 2007 Mitchell N. Charity
# Copyright (c) 2009-2012 Walter Bender
# Copyright (c) 2012 Flavio Danesse
# Copyright (c) 2013 Aneesh Dogra <lionaneesh@gmail.com>
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
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')

from gi.repository import Gdk
from gi.repository import Gtk
from sugar3.activity import activity
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics import style
from sugar3.graphics.radiotoolbutton import RadioToolButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbarbox import ToolbarButton

GRID_CELL_SIZE = style.GRID_CELL_SIZE

import logging
_logger = logging.getLogger("ruler-activity")

from gettext import gettext as _

from util import calc_dpi
import show_rulers
import show_grids
import show_checkers
import show_angles

MMPERINCH = 25.4


class MyCanvas(Gtk.DrawingArea):
    ''' Create a GTK+ widget on which we will draw using Cairo '''

    def __init__(self):
        
        Gtk.DrawingArea.__init__(self)
        
        self._draw_ruler = False
        self._object = None
        self.connect('draw', self.__draw_cb)
        self._dpi = 96

    def __draw_cb(self, widget, cr):

        if self._draw_ruler:
            self._object.draw(cr, self._dpi)
        
        cr.clip()

    def add_a_ruler(self, r):
        self._draw_ruler = True
        self._object = r
        self.queue_draw()

    def get_dpi(self):
        return self._dpi

    def set_dpi(self, dpi):
        self._dpi = dpi


#
# Sugar activity
#
class RulerActivity(activity.Activity):

    def __init__(self, handle):
        super(RulerActivity, self).__init__(handle)

        self.button_dict = {}
        self.callback_dict = {}
        self._ready = False

        font = 'helvetica 12'
        font_bold = 'helvetica bold 12'

        #
        # We need a canvas
        #
        self._canvas = MyCanvas()
        self.set_canvas(self._canvas)
        self._canvas.show()

        screen = Gdk.Screen()
        width = screen.width()
        height = screen.height() - GRID_CELL_SIZE

        dpi, self.known_dpi = calc_dpi()
        self._canvas.set_dpi(dpi)

        # Create instances of our graphics
        self._r = show_rulers.ScreenOfRulers(font, font_bold, width, height)
        self._gcm = show_grids.ScreenGrid_cm(font, font_bold, width, height)
        self._gmm = show_grids.ScreenGrid_mm(font, font_bold, width, height)
        self._a90 = show_angles.Angles90(font, font_bold, width, height)
        self._a360 = show_angles.Angles360(font, font_bold, width, height)
        self._c = show_checkers.ScreenOfCircles(font, font_bold, width, height)

        # start with a ruler
        self._current = self._r
        self._canvas.add_a_ruler(self._current)

        # other settings
        self._grids_mode = "cm"
        self._angles_mode = "90"

        #
        # We need some toolbars
        #
        self.max_participants = 1

        toolbar_box = ToolbarBox()

        # Buttons added to the Activity toolbar
        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        self.rulers = radio_factory('ruler',
                                    toolbar_box.toolbar,
                                    self._rulers_cb,
                                    tooltip=_('Ruler'),
                                    group=None)

        self.grids = radio_factory('grid-a',
                                    toolbar_box.toolbar,
                                    self._grids_cb,
                                    tooltip=_('Grid'),
                                    group=self.rulers)

        self.angles = radio_factory('angles-90',
                                    toolbar_box.toolbar,
                                    self._angles_cb,
                                    tooltip=_('Angles'),
                                    group=self.rulers)

        self.checker = radio_factory('checker',
                                    toolbar_box.toolbar,
                                    self._checker_cb,
                                    tooltip=_('Checker'),
                                    group=self.rulers)

        self.wrapper = Gtk.ToolItem()
        self.wrapper2 = Gtk.ToolItem()
        self.wrapper3 = Gtk.ToolItem()
        self.custom_unit_entry = Gtk.Entry()
        self.txt1 = Gtk.Label()
        self.txt1.set_text(_('1 custom unit equals '))
        self.txt2 = Gtk.Label()
        # TRANS: mm is for Milli Meters
        self.txt2.set_text(_(' mm.'))
        self.wrapper.add(self.txt1)
        self.wrapper2.add(self.custom_unit_entry)
        self.wrapper3.add(self.txt2)
        self.wrapper.show_all()
        self.wrapper2.show_all()
        self.wrapper3.show_all()
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_expand(False)
        separator.show()
        toolbar_box.toolbar.insert(separator, -1)
        custom_units_toolbox = ToolbarBox()
        custom_units_toolbox.toolbar.insert(self.wrapper, -1)
        custom_units_toolbox.toolbar.insert(self.wrapper2, -1)
        custom_units_toolbox.toolbar.insert(self.wrapper3, -1)
        custom_units_toolbox.show()
        self.custom_units_button = ToolbarButton(icon_name='view-source',
                                                 page=custom_units_toolbox)
        toolbar_box.toolbar.insert(self.custom_units_button, -1)
        self.custom_unit_entry.connect('changed', self.custom_unit_change_cb)
        self.custom_units_button.show()

        if not self.known_dpi:
            separator = Gtk.SeparatorToolItem()
            separator.show()
            toolbar_box.toolbar.insert(separator, -1)
            dpi = self._canvas.get_dpi()
            self._dpi_spin_adj = Gtk.Adjustment(dpi, 72, 200, 2, 32, 0)
            self._dpi_spin = Gtk.SpinButton(self._dpi_spin_adj, 0, 0)
            self._dpi_spin_id = self._dpi_spin.connect('value-changed',
                                                       self._dpi_spin_cb)
            self._dpi_spin.set_numeric(True)
            self._dpi_spin.show()
            self.tool_item_dpi = Gtk.ToolItem()
            self.tool_item_dpi.add(self._dpi_spin)
            toolbar_box.toolbar.insert(self.tool_item_dpi, -1)
            self.tool_item_dpi.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        separator.show()
        toolbar_box.toolbar.insert(separator, -1)

        # The ever-present Stop Button
        stop_button = StopButton(self)
        stop_button.props.accelerator = '<Ctrl>Q'
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        self.show_all()

        # Restore state if previously saved
        self._ready = True
        if 'ruler' in self.metadata and \
           self.metadata['ruler'] in self.button_dict:
            _logger.debug('restoring %s', self.metadata['ruler'])
            self.button_dict[self.metadata['ruler']].set_active(True)
            self.callback_dict[self.metadata['ruler']]
        else:
            self._rulers_cb()
            self.rulers.set_active(True)

        if 'custom_unit' in self.metadata:
            self.custom_unit_entry.set_text(self.metadata['custom_unit'])
        else: # set the default
            self.custom_unit_entry.set_text("25.4")

    #
    # Button callbacks
    #
    def _rulers_cb(self, button=None):
        if self._ready:
            self.custom_units_button.set_sensitive(True)
            self._current = self._r
            self._canvas.add_a_ruler(self._current)
            _logger.debug('selecting ruler')
            self.metadata['ruler'] = 'ruler'
        return False

    def custom_unit_change_cb(self, widget):
        try:
            new = float(widget.get_text())
        except ValueError:
            new = MMPERINCH
        new = abs(new)
        if new == 0:
            new = MMPERINCH
            if widget.get_text != '':
                widget.set_text(str(new))
        self._canvas.add_a_ruler(self._r)
        self._r.custom_unit_in_mm = new
        self._r.draw_custom_ruler(self._r.custom_unit_in_mm)
        self.metadata['custom_unit'] = str(new)

    def _grids_cb(self, button=None):
        if self._ready:
            self.custom_units_button.set_sensitive(False)
            self.custom_units_button.set_expanded(False)
            if self._grids_mode == "cm":
                self._current = self._gcm
                if hasattr(self, 'grids'):
                    self.grids.set_icon_name("grid-c")
                self._grids_mode = "mm"
            else:
                self._current = self._gmm
                if hasattr(self, 'grids'):
                    self.grids.set_icon_name("grid-a")
                self._grids_mode = "cm"
            self._canvas.add_a_ruler(self._current)
            _logger.debug('selecting grids')
            self.metadata['ruler'] = 'grids'
        return False

    def _angles_cb(self, button=None):
        if self._ready:
            self.custom_units_button.set_sensitive(False)
            self.custom_units_button.set_expanded(False)
            if self._angles_mode == "90":
                self._current = self._a90
                if hasattr(self, 'angles'):
                    self.angles.set_icon_name("angles-360")
                    self._angles_mode = "360"
            else:
                self._current = self._a360
                if hasattr(self, 'angles'):
                    self.angles.set_icon_name("angles-90")
                    self._angles_mode = "90"
            self._canvas.add_a_ruler(self._current)
            _logger.debug('selecting angles')
            self.metadata['ruler'] = 'angles'
        return False

    def _checker_cb(self, button=None):
        if self._ready:
            self.custom_units_button.set_sensitive(False)
            self.custom_units_button.set_expanded(False)
            self._current = self._c
            self._canvas.add_a_ruler(self._current)
            _logger.debug('selecting checker')
            self.metadata['ruler'] = 'checker'
        return False

    def _dpi_spin_cb(self, button):
        self._canvas.set_dpi(self._dpi_spin.get_value_as_int())
        self._canvas.add_a_ruler(self._current)
        return

    def write_file(self, file_path):
        ''' Write the dpi to the Journal '''
        dpi = self._canvas.get_dpi()
        _logger.debug("Write dpi: " + str(dpi))
        self.metadata['dpi'] = str(dpi)


def radio_factory(icon_name, toolbar, callback, cb_arg=None,
                  tooltip=None, group=None):
    ''' Add a radio button to a toolbar '''
    button = RadioToolButton(group=group)
    button.set_icon_name(icon_name)
    if tooltip is not None:
        button.set_tooltip(tooltip)
    if cb_arg is None:
        button.connect('clicked', callback)
    else:
        button.connect('clicked', callback, cb_arg)
    if hasattr(toolbar, 'insert'):  # the main toolbar
        toolbar.insert(button, -1)
    else:  # or a secondary toolbar
        toolbar.props.page.insert(button, -1)
    button.show()
    return button
