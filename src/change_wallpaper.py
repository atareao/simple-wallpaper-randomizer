#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of Simple Wallpaper Randomizer
#
# Copyright (c) 2019 Lorenzo Carbonell Cerezo <atareao@atareao.es>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
