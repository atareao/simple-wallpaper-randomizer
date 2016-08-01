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

import os
import sys
import subprocess
from gi.repository import Gio

xfce_displays = ["/backdrop/screen0/monitor0/image-path",
                 "/backdrop/screen0/monitor0/workspace0/last-image"]


def set_settings(schema, key, value):
    settings = Gio.Settings.new(schema)
    if type(value) == bool:
        settings.set_boolean(key, value)
    elif type(value) == float:
        settings.set_double(key, value)
    elif type(value) == int:
        settings.set_int(key, value)
    else:
        settings.set_string(key, value)
    settings.apply()


def set_background(file_path):
    de = get_desktop_environment()

    if de in ["gnome", "unity", "cinnamon", "pantheon", "gnome-classic"]:
        # Because of a bug and stupid design of gsettings,
        # see http://askubuntu.com/a/418521/388226
        if de == "unity":
            set_settings("org.gnome.desktop.background",
                         "draw-background",
                         False)
        set_settings("org.gnome.desktop.background",
                     "picture-uri",
                     "file://" + file_path)
        set_settings("org.gnome.desktop.background",
                     "picture-options",
                     "scaled")
        set_settings("org.gnome.desktop.background",
                     "primary-color",
                     "FFFFFF")
    elif de == "mate":
        set_settings("org.mate.background",
                     "picture-filename",
                     file_path)
    elif de == 'i3':
        subprocess.call(['feh',
                         '--bg-fill',
                         file_path])
    elif de == "xfce4":
        for display in xfce_displays:
            subprocess.call(["xfconf-query",
                             "--channel",
                             "xfce4-desktop",
                             "--property",
                             display,
                             "--set",
                             file_path])
    elif de == "lxde":
        subprocess.call(["pcmanfm",
                         "--set-wallpaper",
                         file_path,
                         "--wallpaper-mode=fit", ])
    elif de == "mac":
        subprocess.call(["osascript",
                         "-e",
                         'tell application "System Events"\n'
                         'set theDesktops to a reference to every desktop\n'
                         'repeat with aDesktop in theDesktops\n'
                         'set the picture of aDesktop to \"' +
                         file_path + '"\nend repeat\nend tell'])
        subprocess.call(["killall", "Dock"])
    elif has_program("feh"):
        print("\nCouldn't detect your desktop environment ('{}'), but you have"
              "'feh' installed so we will use it.".format(de))
        os.environ['DISPLAY'] = ':0'
        subprocess.call(["feh", "--bg-max", file_path])
    elif has_program("nitrogen"):
        print("\nCouldn't detect your desktop environment ('{}'), but you have"
              "'nitrogen' installed so we will use it.".format(de))
        os.environ["DISPLAY"] = ':0'
        subprocess.call(["nitrogen", "--restore"])
    else:
        return False
    return True


# http://stackoverflow.com/a/21213358/4466589
def get_desktop_environment():
    # From http://stackoverflow.com/questions/2035657/
    # what-is-my-current-desktop-environment
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=1139057
    if sys.platform in ["win32", "cygwin"]:
        return "windows"
    elif sys.platform == "darwin":
        return "mac"
    else:  # Most likely either a POSIX system or something not much common
        desktop_session = os.environ.get("DESKTOP_SESSION")
        # Easier to match if we don't have to deal with caracter cases
        if desktop_session is not None:
            desktop_session = desktop_session.lower()
            if desktop_session in ["gnome", "unity", "cinnamon", "mate",
                                   "xfce4", "lxde", "fluxbox",
                                   "blackbox", "openbox", "icewm", "jwm",
                                   "afterstep", "trinity", "kde", "pantheon",
                                   "gnome-classic", "i3"]:
                return desktop_session
            # Special cases ##
            # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if
            # using LXDE.
            # There is no guarantee that they will not do the same with the
            # other desktop environments.
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
            elif desktop_session.startswith("wmaker"):  # e.g. wmaker-common
                return "windowmaker"
        if os.environ.get('KDE_FULL_SESSION') == 'true':
            return "kde"
        elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            if "deprecated" not in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                return "gnome2"
        # From http://ubuntuforums.org/showthread.php?t=652320
        elif is_running("xfce-mcs-manage"):
            return "xfce4"
        elif is_running("ksmserver"):
            return "kde"
    # We couldn't detect it so far, so let's try one last time
    current_desktop = os.environ.get("XDG_CURRENT_DESKTOP")
    if current_desktop:
        current_desktop = current_desktop.lower()
        if current_desktop in ["gnome", "unity", "kde", "gnome-classic",
                               "mate"]:
            return current_desktop
        # Special Cases
        elif current_desktop == "xfce":
            return "xfce4"
        elif current_desktop == "x-cinnamon":
            return "cinnamon"
    return "unknown"


def has_program(program):
    try:
        subprocess.check_output(["which", "--", program])
        return True
    except subprocess.CalledProcessError:
        return False


def is_running(process):
    try:
        subprocess.check_output(["pidof", "--", process])
        return True
    except subprocess.CalledProcessError:
        return False

if __name__ == '__main__':
    print(get_desktop_environment())
    set_background('/home/lorenzo/Escritorio/sample01.jpg')
