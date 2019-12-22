#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of Simple Wallpaper Randomizer

# Copyright (C) 2012-2017 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from crontab import CronTab
import gi
try:
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
import os
from os import listdir
from os.path import isfile, join
from urllib.parse import unquote_plus
from comun import _
from comun import get_desktop_environment
from configurator import Configuration
from autostart import Autostart
import random
import getpass
import comun
import shutil


WALLPAPERS = ['christmas-wallpapers',
              'chromecast-wallpapers',
              'chrome-os-wallpapers',
              'halloween-wallpapers',
              'ubuntu-contest-wallpapers',
              'wallpapers-by-linux-pictures',
              'wallpapers-by-sylvia-ritter',
              'wallpapers-by-vincent-van-gogh',
              'winter-wallpapers']


def marginize(widget, margin=5):
    widget.set_margin_top(margin)
    widget.set_margin_bottom(margin)
    widget.set_margin_start(margin)
    widget.set_margin_end(margin)


class SimpleWallpaperRandomizerDialog(Gtk.Dialog):
    def __init__(self):
        self.cron = CronTab(user=True)
        Gtk.Dialog.__init__(self,
                            _('Simple Wallpaper Randomizer'),
                            None)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        '''
        self.set_wmclass('Simple Wallpaper Randomizer',
                         'SimpleWallpaperRandomizerDialog')
        '''
        self.set_title(comun.APPNAME)
        self. set_icon_name(comun.APP)
        self.set_default_size(350, 250)

        self.autostart = Autostart()

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        self.get_content_area().add(vbox)

        notebook = Gtk.Notebook.new()
        vbox.pack_start(notebook, True, True, 0)

        vbox_1 = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        notebook.append_page_menu(vbox_1, Gtk.Label.new(_('Preferences')))

        vbox0 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        vbox_1.pack_start(vbox0, True, False, 0)

        frame_1 = Gtk.Frame()
        vbox0.pack_start(frame_1, True, False, 0)

        vbox1 = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        frame_1.add(vbox1)

        frame1 = Gtk.Frame()
        marginize(frame1)
        vbox1.pack_start(frame1, False, True, 0)

        vboxtable1 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        frame1.add(vboxtable1)

        table1 = Gtk.Grid.new()
        table1.set_border_width(5)
        vboxtable1.pack_start(table1, True, False, 0)

        button1 = Gtk.Button.new_with_label(_('Change it now?'))
        marginize(button1)
        button1.connect('clicked', self.on_button1_clicked)
        table1.attach(button1, 0, 0, 1, 1)

        frame2 = Gtk.Frame()
        marginize(frame2)
        vbox1.pack_start(frame2, False, True, 0)

        vboxtable2 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        frame2.add(vboxtable2)

        table2 = Gtk.Grid.new()
        table2.set_border_width(5)
        vboxtable2.pack_start(table2, True, False, 0)

        label11 = Gtk.Label.new(_('Switch on time?') + ':')
        marginize(label11)
        label11.set_xalign(0)
        table2.attach(label11, 0, 0, 1, 1)

        vboxs11 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        table2.attach(vboxs11, 1, 0, 1, 1)
        self.switch11 = Gtk.Switch()
        vboxs11.pack_start(self.switch11, False, False, 0)

        label21 = Gtk.Label.new(_('Minutes between changes') + ':')
        marginize(label21)
        label21.set_xalign(0)
        table2.attach(label21, 0, 1, 1, 1)
        adjustment21 = Gtk.Adjustment.new(1, 1, 59, 1, 10, 0)
        self.spinbutton21 = Gtk.SpinButton()
        marginize(self.spinbutton21)
        self.spinbutton21.set_adjustment(adjustment21)
        table2.attach(self.spinbutton21, 1, 1, 1, 1)
        label22 = Gtk.Label.new(_('Hours between changes') + ':')
        marginize(label22)
        label22.set_xalign(0)
        table2.attach(label22, 0, 2, 1, 1)
        adjustment22 = Gtk.Adjustment.new(0, 0, 24, 1, 10, 0)
        self.spinbutton22 = Gtk.SpinButton()
        marginize(self.spinbutton22)
        self.spinbutton22.set_adjustment(adjustment22)
        table2.attach(self.spinbutton22, 1, 2, 1, 1)
        label23 = Gtk.Label.new(_('Days between changes') + ':')
        marginize(label23)
        label23.set_xalign(0)
        table2.attach(label23, 0, 3, 1, 1)
        adjustment23 = Gtk.Adjustment.new(0, 0, 365, 1, 10, 0)
        self.spinbutton23 = Gtk.SpinButton()
        marginize(self.spinbutton23)
        self.spinbutton23.set_adjustment(adjustment23)
        table2.attach(self.spinbutton23, 1, 3, 1, 1)

        frame3 = Gtk.Frame()
        marginize(frame3)
        vbox1.pack_start(frame3, False, True, 0)

        vboxtable3 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        frame3.add(vboxtable3)

        table3 = Gtk.Grid.new()
        table3.set_border_width(5)
        vboxtable3.pack_start(table3, True, False, 0)

        label31 = Gtk.Label.new(_('Switch on boot?') + ':')
        label31.set_xalign(0)
        table3.attach(label31, 0, 0, 1, 1)

        vboxs31 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        table3.attach(vboxs31, 1, 0, 1, 1)
        self.switch31 = Gtk.Switch()
        marginize(self.switch31)
        vboxs31.pack_start(self.switch31, False, False, 0)

        vbox2 = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        notebook.append_page_menu(vbox2,
                                  Gtk.Label.new(_('Install wallpapers')))
        frame4 = Gtk.Frame()
        vbox2.pack_start(frame4, True, True, 0)
        vbox5 = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        frame4.add(vbox5)

        frame5 = Gtk.Frame()
        vbox5.pack_start(frame5, True, True, 0)

        tablew = Gtk.Grid.new()
        for index, wallpaperset in enumerate(WALLPAPERS):
            vboxt = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
            marginize(vboxt)
            vboxth = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
            marginize(vboxth)
            for i in range(1, 4):
                afile = os.path.join(
                    comun.SAMPLES_DIR,
                    '{}/example-{}.jpg'.format(wallpaperset, i))
                if os.path.exists(afile):
                    image = Gtk.Image.new_from_file(afile)
                    vboxth.pack_start(image, True, True, 0)
            vboxt.pack_start(vboxth, True, True, 0)

            button = Gtk.Button.new_with_label(wallpaperset)
            marginize(button)
            button.connect('clicked',
                           self.on_button_clicked,
                           wallpaperset)
            vboxt.pack_start(button, True, True, 0)
            print(index)
            left = index if index < 5 else index - 5
            top = 0 if index < 5 else 1
            tablew.attach(vboxt, top, left, 1, 1)
        vbox2.pack_start(tablew, True, True, 0)
        marginize(vbox2)

        configuration = Configuration()
        configuration.set('desktop_environment',
                          comun.get_desktop_environment())
        configuration.save()
        self.load_preferences()

        self.show_all()

    def on_button_clicked(self, widget, wallpaper_set):
        os.system('apturl apt:%s &' % (wallpaper_set))

    def on_button1_clicked(self, widget):
        print('clicked')
        self.force_change_wallpaper()

    def get_the_job(self):
        iter = self.cron.find_comment('cron_change_wallpaper')
        jobs = list(iter)
        noj = len(jobs)
        print('Number of jobs: %s' % noj)
        if noj == 0:
            return None
        else:
            for index, ajob in enumerate(jobs):
                if index == 0:
                    thejob = ajob
                else:
                    self.cron.remove(ajob)
                    self.cron.write()
        return thejob

    def load_preferences(self):
        thejob = self.get_the_job()
        if thejob is None:
            minutes = 10
            hours = 0
            days = 0
        else:
            self.switch11.set_active(thejob.is_enabled())
            data = str(thejob).split(" ")
            if thejob.is_enabled():
                minutes = data[0]
                hours = data[1]
                days = data[2]
            else:
                minutes = data[1]
                hours = data[2]
                days = data[3]
            print(minutes, hours, days)
            if minutes != '*' and minutes.find('/'):
                minutes = int(minutes.split('/')[-1])
            else:
                minutes = 1
            if hours != '*' and hours.find('/'):
                hours = int(hours.split('/')[-1]) - 1
            else:
                hours = 0
            if days != '*' and days.find('/'):
                days = int(days.split('/')[-1]) - 1
            else:
                days = 0
        self.spinbutton21.set_value(minutes)
        self.spinbutton22.set_value(hours)
        self.spinbutton23.set_value(days)
        print(minutes, hours, days)
        self.switch31.set_active(self.autostart.get_autostart())

    def force_change_wallpaper(self):
        filename = random.choice(get_not_displayed_files())
        shutil.copyfile(filename, comun.SELECTED_WALLPAPER)
        print(filename)
        PARAMS = 'export DISPLAY=:0;\
export GSETTINGS_BACKEND=dconf'
        GSET_GNOME = 'gsettings set org.gnome.desktop.background picture-uri \
"file://%s"'
        GSET_MATE = 'gsettings set org.mate.background picture-filename "%s"'
        GSET_CINNAMON = 'gsettings set org.cinnamon.desktop.background \
picture-uri "file://%s"'
        GSET_XFCE = 'xfconf-query -c xfce4-desktop -p \
/backdrop/screen0/monitorDisplayPort-1/workspace0/last-image --set "%s"'
        if os.path.exists(comun.SELECTED_WALLPAPER):
            params = PARAMS  # % os.getuid()
            desktop_environment = get_desktop_environment()
            print(desktop_environment)
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

    def save_preferences(self):
        thejob = self.get_the_job()
        if self.switch11.get_active():
            if thejob is None:
                PARAMS = 'export DISPLAY=:0;\
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%s/bus;\
export GSETTINGS_BACKEND=dconf'
                EXEC = '/usr/bin/python3'
                SCRIPT = '/usr/share/simple-wallpaper-randomizer/\
change_wallpaper.py'
                GSET_GNOME = 'gsettings set org.gnome.desktop.background \
picture-uri "file://`%s %s`"'
                # "filcde://`cat %s`"'
                GSET_MATE = 'gsettings set org.mate.background \
picture-filename "`%s %s`"'
                GSET_CINNAMON = 'gsettings set \
org.cinnamon.desktop.background picture-uri "file://`%s %s`"'
                GSET_XFCE = 'xfconf-query -c xfce4-desktop -p \
/backdrop/screen0/monitorDisplayPort-1/workspace0/last-image --set "`%s %s`"'
                params = PARAMS % os.getuid()
                desktop_environment = get_desktop_environment()
                if desktop_environment == 'gnome' or \
                        desktop_environment == 'unity' or \
                        desktop_environment == 'budgie-desktop':
                    gset = GSET_GNOME % (EXEC, SCRIPT)
                elif desktop_environment == 'mate':
                    gset = GSET_MATE % (EXEC, SCRIPT)
                elif desktop_environment == "cinnamon":
                    gset = GSET_CINNAMON % (EXEC, SCRIPT)
                elif desktop_environment == 'xfce4':
                    gset = GSET_XFCE % (EXEC, SCRIPT)
                else:
                    gset = None
                if gset is not None:
                    command = '{0};{1}'.format(params, gset)
                    thejob = self.cron.new(command=command,
                                           user=getpass.getuser())
                    thejob.minute.every(10)
                    thejob.set_comment("cron_change_wallpaper")
                    thejob.enable()
            thejob.enable(self.switch11.get_active())
            thejob.minute.every(self.spinbutton21.get_value())
            thejob.hour.every(self.spinbutton22.get_value() + 1)
            thejob.day.every(self.spinbutton23.get_value() + 1)
            self.cron.write()
        else:
            if thejob is not None:
                self.cron.remove(thejob)
            self.autostart.set_autostart(self.switch31.get_active())
        self.cron.write()


def is_image(afile):
    if isfile(afile):
        fileName, fileExtension = os.path.splitext(unquote_plus(afile))
        if fileExtension.lower() in comun.IMAGE_EXTENSIONS:
            return True
    return False


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(unquote_plus(fullPath))
    return allFiles


def get_all_files():
    mypath = '/usr/share/backgrounds'
    return getListOfFiles(mypath)


def get_not_displayed_files():
    all_files = get_all_files()
    for displayed_file in get_displayed_files():
        if displayed_file in all_files:
            all_files.remove(displayed_file)
    return all_files


def get_displayed_files():
    configuration = Configuration()
    displayed_files = configuration.get('displayed_files')
    all_files = get_all_files()
    # print('%s / %s' % (len(displayed_files), len(all_files)))
    if len(displayed_files) == len(all_files):  # all files were showed
        displayed_files = []
        configuration.set('displayed_files', displayed_files)
        configuration.save()
    return displayed_files


def add_file_to_displayed_files(afile):
    configuration = Configuration()
    displayed_files = configuration.get('displayed_files')
    if afile not in displayed_files:
        displayed_files.append(afile)
    configuration.set('displayed_files', displayed_files)
    configuration.save()


if __name__ == '__main__':
    swrd = SimpleWallpaperRandomizerDialog()
    if swrd.run() == Gtk.ResponseType.ACCEPT:
        swrd.save_preferences()
    swrd.destroy()
    exit(0)
