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
import comun
from comun import get_desktop_environment
from simplewallpaperrandomizer import get_not_displayed_files
from simplewallpaperrandomizer import add_file_to_displayed_files
import shutil


def change_gesettings(filename):
    shutil.copyfile(filename, comun.SELECTED_WALLPAPER)
    PARAMS = 'export DISPLAY=:0;\
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%s/bus;\
export GSETTINGS_BACKEND=dconf'
    GSET_GNOME = 'gsettings set org.gnome.desktop.background picture-uri \
"file://%s"'
    GSET_MATE = 'gsettings set org.mate.background picture-filename "%s"'
    GSET_CINNAMON = 'gsettings set org.cinnamon.desktop.background picture-uri \
"file://%s"'
    GSET_XFCE = 'xfconf-query -c xfce4-desktop -p \
/backdrop/screen0/monitorDisplayPort-1/workspace0/last-image --set "%s"'
    if os.path.exists(comun.SELECTED_WALLPAPER):
        params = PARAMS % os.getuid()
        desktop_environment = get_desktop_environment()
        if desktop_environment == 'gnome' or \
                desktop_environment == 'unity' or \
                desktop_environment == 'budgie-desktop':
            gset = GSET_GNOME % comun.SELECTED_WALLPAPER
        elif desktop_environment == 'mate':
            gset = GSET_MATE % comun.SELECTED_WALLPAPER
        elif desktop_environment == 'cinnamon':
            gset = GSET_CINNAMON % comun.SELECTED_WALLPAPER
        elif desktop_environment == 'xfce4':
            gset = GSET_XFCE % comun.SELECTED_WALLPAPER
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
        shutil.copyfile(filename, comun.SELECTED_WALLPAPER)
        print(comun.SELECTED_WALLPAPER)
