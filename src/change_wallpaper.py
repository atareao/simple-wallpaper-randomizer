#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of Simple Wallpaper Randomizer
#
# Copyright (C) 2016 Lorenzo Carbonell
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
import os
import sys
import subprocess
import datetime
import time
from gi.repository import Gio

try:
    if __file__.startswith(
            '/opt/extras.ubuntu.com/simple-wallpaper-randomizer') or\
        os.getcwd().startswith(
            '/opt/extras.ubuntu.com/simple-wallpaper-randomizer'):
        sys.path.insert(
            1,
            '/opt/extras.ubuntu.com/simple-wallpaper-randomizer/\
share/simple-wallpaper-randomizer')
    else:
        sys.path.insert(1,
                        os.path.normpath(os.path.join(os.getcwd(), '../src')))
except Exception as e:
    print(e)
'''
sys.path.insert(
    1,
    '/opt/extras.ubuntu.com/simple-wallpaper-randomizer/\
share/simple-wallpaper-randomizer')
'''
from swr.simplewallpaperrandomizer import get_not_displayed_files,\
                                      add_file_to_displayed_files
from swr.utils import set_background


if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) > 1 and sys.argv[1] == 'boot':
        time.sleep(5)
    if len(sys.argv) > 2:
        config_file = sys.argv[2]
    else:
        config_file = None
    print(config_file)
    files = get_not_displayed_files(config_file)
    print(files)
    wallpaper = random.choice(files)
    set_background(wallpaper)
    add_file_to_displayed_files(wallpaper)
