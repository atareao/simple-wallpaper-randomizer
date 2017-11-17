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


from crontab import CronTab
import gi
try:
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk, Gio
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

WALLPAPERS = ['chrome-os-wallpapers',
              'chrome-os-wallpapers-2015',
              'chromecast-wallpapers-2015',
              'saucy-salamander-wallpaper-contest',
              'trusty-tahr-wallpaper-contest',
              'vivid-vervet-wallpaper-contest',
              'wily-werewolf-wallpaper-contest',
              'xenial-xerus-wallpaper-contest',
              'yakkety-yak-wallpaper-contest',
              'zesty-zapus-wallpaper-contest']


class SimpleWallpaperRandomizerDialog(Gtk.Dialog):
    def __init__(self):
        self.cron = CronTab(user=True)
        # self.cron = CronTab()
        Gtk.Dialog.__init__(self,
                            _('Simple Wallpaper Randomizer'),
                            None,
                            Gtk.DialogFlags.MODAL |
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,
                             Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_title(comun.APPNAME)
        self.set_icon_from_file(comun.ICON)
        self.set_default_size(350, 250)

        self.autostart = Autostart()

        vbox = Gtk.VBox(spacing=5)
        self.get_content_area().add(vbox)

        notebook = Gtk.Notebook.new()
        vbox.pack_start(notebook, True, True, 0)

        vbox0 = Gtk.VBox(spacing=5)
        notebook.append_page_menu(vbox0, Gtk.Label(_('Preferences')))
        frame0 = Gtk.Frame()
        vbox0.pack_start(frame0, True, True, 0)
        vbox1 = Gtk.VBox(spacing=5)
        frame0.add(vbox1)
        #
        frame1 = Gtk.Frame()
        vbox1.pack_start(frame1, True, True, 0)
        #
        table1 = Gtk.Table(rows=1, columns=3, homogeneous=True)
        table1.set_border_width(5)
        table1.set_col_spacings(5)
        table1.set_row_spacings(5)
        frame1.add(table1)
        #
        button1 = Gtk.Button.new_with_label(_('Change it now?'))
        button1.connect('clicked', self.on_button1_clicked)
        table1.attach(button1, 1, 2, 0, 1,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        #
        frame2 = Gtk.Frame()
        vbox1.pack_start(frame2, True, True, 0)
        #
        table2 = Gtk.Table(rows=4, columns=2, homogeneous=False)
        table2.set_border_width(5)
        table2.set_col_spacings(5)
        table2.set_row_spacings(5)
        frame2.add(table2)
        #
        label11 = Gtk.Label(_('Switch on time?') + ':')
        label11.set_alignment(0, .5)
        table2.attach(label11, 0, 1, 0, 1,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        self.switch11 = Gtk.Switch()
        table2.attach(self.switch11, 1, 2, 0, 1,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        label21 = Gtk.Label(_('Minutes between changes') + ':')
        label21.set_alignment(0, .5)
        table2.attach(label21, 0, 1, 1, 2,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        adjustment21 = Gtk.Adjustment(1, 1, 59, 1, 10, 0)
        self.spinbutton21 = Gtk.SpinButton()
        self.spinbutton21.set_adjustment(adjustment21)
        table2.attach(self.spinbutton21, 1, 2, 1, 2,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        label22 = Gtk.Label(_('Hours between changes') + ':')
        label22.set_alignment(0, .5)
        table2.attach(label22, 0, 1, 2, 3,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        adjustment22 = Gtk.Adjustment(0, 0, 24, 1, 10, 0)
        self.spinbutton22 = Gtk.SpinButton()
        self.spinbutton22.set_adjustment(adjustment22)
        table2.attach(self.spinbutton22, 1, 2, 2, 3,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        label23 = Gtk.Label(_('Days between changes') + ':')
        label23.set_alignment(0, .5)
        table2.attach(label23, 0, 1, 3, 4,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        adjustment23 = Gtk.Adjustment(0, 0, 365, 1, 10, 0)
        self.spinbutton23 = Gtk.SpinButton()
        self.spinbutton23.set_adjustment(adjustment23)
        table2.attach(self.spinbutton23, 1, 2, 3, 4,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        #
        frame3 = Gtk.Frame()
        vbox1.pack_start(frame3, True, True, 0)
        #
        table3 = Gtk.Table(rows=1, columns=2, homogeneous=False)
        table3.set_border_width(5)
        table3.set_col_spacings(5)
        table3.set_row_spacings(5)
        frame3.add(table3)
        #
        #
        label31 = Gtk.Label(_('Switch on boot?') + ':')
        label31.set_alignment(0, .5)
        table3.attach(label31, 0, 1, 0, 1,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        self.switch31 = Gtk.Switch()
        table3.attach(self.switch31, 1, 2, 0, 1,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.SHRINK)
        #
        vbox2 = Gtk.VBox(spacing=5)
        notebook.append_page_menu(vbox2, Gtk.Label(_('Install wallpapers')))
        frame4 = Gtk.Frame()
        vbox2.pack_start(frame4, True, True, 0)
        vbox5 = Gtk.VBox(spacing=5)
        frame4.add(vbox5)
        #
        frame5 = Gtk.Frame()
        vbox5.pack_start(frame5, True, True, 0)
        #
        vbox6 = Gtk.VBox(spacing=5)
        frame5.add(vbox6)
        for wallpaperset in WALLPAPERS:
            button = Gtk.Button(wallpaperset)
            button.connect('clicked',
                           self.on_button_clicked,
                           wallpaperset)
            vbox2.pack_start(button, True, True, 0)

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

    def get_the_job_on_reboot(self):
        iter = self.cron.find_comment('cron_change_wallpaper_on_reboot')
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
        wallpaper = random.choice(get_not_displayed_files())
        settings = Gio.Settings.new('org.gnome.desktop.background')
        settings.set_string('picture-options', 'wallpaper')
        settings.set_string('picture-uri', 'file://%s' % wallpaper)
        add_file_to_displayed_files(wallpaper)

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
                # "file://`cat %s`"'
                GSET_MATE = 'gsettings set org.mate.background \
picture-filename "`%s %s`"'
                params = PARAMS % os.getuid()
                desktop_environmen = get_desktop_environment()
                if desktop_environmen == 'gnome':
                    gset = GSET_GNOME % (EXEC, SCRIPT)
                elif desktop_environmen == 'mate':
                    gset = GSET_MATE % (EXEC, SCRIPT)
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


def get_all_files():
    mypath = '/usr/share/backgrounds'
    return [unquote_plus(join(mypath, f)) for f in listdir(mypath)
            if is_image(join(mypath, f))]


def get_not_displayed_files():
    all_files = get_all_files()
    for displayed_file in get_displayed_files():
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
