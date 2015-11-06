#!/usr/bin/env python3

import random, os, sys, subprocess
import datetime
import time
from gi.repository import Gio
if __file__.startswith('/opt/extras.ubuntu.com/simple-wallpaper-randomizer') or os.getcwd().startswith('/opt/extras.ubuntu.com/utext'):
	sys.path.insert(1, '/opt/extras.ubuntu.com/simple-wallpaper-randomizer/share/simple-wallpaper-randomizer')
else:
	sys.path.insert(1,os.path.normpath(os.path.join(os.getcwd(), '../src')))	
from simplewallpaperrandomizer import get_not_displayed_files, add_file_to_displayed_files

if __name__ == '__main__':
	print(len(sys.argv))
	if len(sys.argv)>1 and sys.argv[1]=='boot':
		time.sleep(5)	
	wallpaper = random.choice(get_not_displayed_files())
	cmd = "export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep gnome-session)/environ|cut -d= -f2-);"
	cmd = cmd + "gsettings set org.gnome.desktop.background picture-uri " + "file://" + wallpaper
	subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	add_file_to_displayed_files(wallpaper)
