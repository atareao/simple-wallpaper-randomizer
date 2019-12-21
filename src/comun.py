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

__author__ = 'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'
__date__ = '$24/09/2011'
__copyright__ = 'Copyright (c) 2012-2015 Lorenzo Carbonell'
__license__ = 'GPLV3'
__url__ = 'http://www.atareao.es'

import os
import locale
import gettext
import sys
import re
import subprocess


def is_package():
    return __file__.find('src') < 0


def is_running(process):
    # From http://www.bloggerpolis.com/2011/05/\
    # how-to-check-if-a-process-is-running-using-python/
    # and http://richarddingwall.name/2009/06/18/\
    # windows-equivalents-of-ps-and-kill-commands/
    try:  # Linux/Unix
        s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    except Exception as e:  # Windows
        print(e)
        s = subprocess.Popen(["tasklist", "/v"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True
    return False


def get_desktop_environment():
    desktop_session = os.environ.get("DESKTOP_SESSION")
    # easier to match if we doesn't have  to deal with caracter cases
    if desktop_session is not None:
        desktop_session = desktop_session.lower()
        if desktop_session in ["gnome", "unity", "cinnamon", "mate",
                               "budgie-desktop", "xfce4", "lxde", "fluxbox",
                               "blackbox", "openbox", "icewm", "jwm",
                               "afterstep", "trinity", "kde"]:
            return desktop_session
        # ## Special cases ##
        # Canonical sets $DESKTOP_SESSION to Lubuntu rather than
        # LXDE if using LXDE.
        # There is no guarantee that they will not do the same with
        # the other desktop environments.
        elif "xfce" in desktop_session or\
                desktop_session.startswith("xubuntu"):
            return "xfce4"
        elif desktop_session.startswith("ubuntu"):
            return "unity"
        elif desktop_session.startswith("lubuntu"):
            return "lxde"
        elif desktop_session.startswith("kubuntu"):
            return "kde"
        elif desktop_session.startswith("razor"):  # e.g. razorkwin
            return "razor-qt"
        elif desktop_session.startswith("wmaker"):  # eg. wmaker-common
            return "windowmaker"
    if os.environ.get('KDE_FULL_SESSION') == 'true':
        return "kde"
    elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
        if "deprecated" not in os.environ.get(
                'GNOME_DESKTOP_SESSION_ID'):
            return "gnome2"
    # From http://ubuntuforums.org/showthread.php?t=652320
    elif is_running("xfce-mcs-manage"):
        return "xfce4"
    elif is_running("ksmserver"):
        return "kde"
    return "unknown"


APP = 'simple-wallpaper-randomizer'
APPNAME = 'Simple Wallpaper Randomizer'
APP_CONF = APP + '.conf'
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config')
CONFIG_APP_DIR = os.path.join(CONFIG_DIR, APP)
CONFIG_FILE = os.path.join(CONFIG_APP_DIR, APP_CONF)
SELECTED_WALLPAPER = os.path.join(CONFIG_APP_DIR, 'wallpaper.jpg')
SELECTED_FILE = os.path.join(CONFIG_APP_DIR, 'selected_file.dat')
PARAMS = {'displayed_files': [],
          'desktop_environment': ''}
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']

if is_package():
    ROOTDIR = '/usr/share/'
    LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
    APPDIR = os.path.join(ROOTDIR, APP)
    SAMPLES_DIR = os.path.join(APPDIR, 'samples')
    CHANGELOG = os.path.join(APPDIR, 'changelog')
else:
    ROOTDIR = os.path.dirname(__file__)
    LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../template1'))
    APPDIR = ROOTDIR
    SAMPLES_DIR = os.path.normpath(os.path.join(ROOTDIR, '../data/samples'))
    DATADIR = os.path.normpath(os.path.join(ROOTDIR, '../data'))
    ICONDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons'))
    SOCIALDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/social'))
    DEBIANDIR = os.path.normpath(os.path.join(ROOTDIR, '../debian'))
    CHANGELOG = os.path.join(DEBIANDIR, 'changelog')

f = open(CHANGELOG, 'r')
line = f.readline()
f.close()
pos = line.find('(')
posf = line.find(')', pos)
VERSION = line[pos + 1:posf].strip()
if not is_package():
    VERSION = VERSION + '-src'
try:
    current_locale, encoding = locale.getdefaultlocale()
    language = gettext.translation(APP, LANGDIR, [current_locale])
    language.install()
    print(language)
    if sys.version_info[0] == 3:
        _ = language.gettext
    else:
        _ = language.ugettext
except Exception as e:
    # print(e)
    _ = str

APPNAME = _(APPNAME)
