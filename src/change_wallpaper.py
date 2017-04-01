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
import subprocess
import os
from gi.repository import Gio
try:
    from simplewallpaperrandomizer import get_not_displayed_files
    from simplewallpaperrandomizer import add_file_to_displayed_files
    from configurator import Configuration
except Exception as e:
    print(e)
    sys.path.insert(
        1, '/opt/extras.ubuntu.com/simple-wallpaper-randomizer/share/\
simple-wallpaper-randomizer')
    from simplewallpaperrandomizer import get_not_displayed_files
    from simplewallpaperrandomizer import add_file_to_displayed_files
    from configurator import Configuration


def execute(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, err = p.communicate()
    return output.decode()


if __name__ == '__main__':
    configuration = Configuration()
    desktop_environment = configuration.get('desktop_environment')
    print(desktop_environment)
    wallpaper = random.choice(get_not_displayed_files())
    cmd = 'grep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -n %s-session)\
/environ|cut -d= -f2-;' % (desktop_environment)
    dsba = execute(cmd)[:-2]
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = dsba
    selected = Gio.File.new_for_path(wallpaper)
    settings = Gio.Settings.new('org.gnome.desktop.background')
    settings.set_string('picture-options', 'wallpaper')
    settings.set_string('picture-uri', selected.get_uri())
    add_file_to_displayed_files(wallpaper)
