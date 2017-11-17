#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of Simple Wallpaper Randomizer
#
# Copyright (C) 2012-2017 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import random
import sys
import os
from comun import get_desktop_environment
from simplewallpaperrandomizer import get_not_displayed_files
from simplewallpaperrandomizer import add_file_to_displayed_files


def change_gesettings(filename):
    PARAMS = 'export DISPLAY=:0;\
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%s/bus;\
export GSETTINGS_BACKEND=dconf'
    GSET_GNOME = 'gsettings set org.gnome.desktop.background picture-uri \
"file://%s"'
    GSET_MATE = 'gsettings set org.mate.background picture-filename "%s"'
    if os.path.exists(filename):
        params = PARAMS % os.getuid()
        desktop_environmen = get_desktop_environment()
        if desktop_environmen == 'gnome':
            gset = GSET_GNOME % filename
        elif desktop_environmen == 'mate':
            gset = GSET_MATE % filename
        else:
            gset = None
        if gset is not None:
            command = '{0};{1}'.format(params, gset)
            os.system(command)
            add_file_to_displayed_files(filename)


if __name__ == '__main__':
    filename = random.choice(get_not_displayed_files())
    if len(sys.argv) > 1:
        change_gesettings(filename)
    else:
        add_file_to_displayed_files(filename)
        print(filename)
