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

import codecs
import os
import json
import sys
sys.path.append(
    os.path.normpath(
        os.path.join(
            os.path.dirname(
                os.path.realpath(os.path.join(os.getcwd(),
                                 os.path.expanduser(__file__)))),
            '..')))
try:
    from swr.comun import PARAMS
    from swr.comun import CONFIG_FILE
except Exception as e:
    print(e)
    exit(-1)


class Configuration(object):
    def __init__(self, config_file=None):
        self.params = PARAMS
        if config_file is None:
            self.config_file = CONFIG_FILE
        else:
            self.config_file = config_file
        self.read()

    def get(self, key):
        try:
            return self.params[key]
        except KeyError as e:
            print(e)
            self.params[key] = PARAMS[key]
            return self.params[key]

    def set(self, key, value):
        self.params[key] = value

    def reset(self):
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        self.params = PARAMS
        self.save()

    def set_defaults(self):
        self.params = PARAMS
        self.save()

    def read(self):
        try:
            f = codecs.open(self.config_file, 'r', 'utf-8')
        except IOError as e:
            print(e)
            self.save()
            f = codecs.open(self.config_file, 'r', 'utf-8')
        try:
            self.params = json.loads(f.read())
        except ValueError as e:
            print(e)
            self.save()
        f.close()

    def save(self):
        if not os.path.exists(os.path.dirname(self.config_file)):
            os.makedirs(os.path.dirname(self.config_file))
        f = codecs.open(CONFIG_FILE, 'w', 'utf-8')
        f.write(json.dumps(self.params))
        f.close()
