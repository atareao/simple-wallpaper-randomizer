#!/usr/bin/env python3

from crontab import CronTab
from gi.repository import Gtk, Gio
import os
import shutil
from os import listdir
from os.path import isfile, join
from urllib.parse import unquote_plus, unquote
from comun import _
from configurator import Configuration
import random
import getpass
import comun

class SimpleWallpaperRandomizerDialog(Gtk.Dialog):
	def __init__(self):
		self.cron = CronTab(user=True)
		#self.cron = CronTab()
		Gtk.Dialog.__init__(self,_('Simple Wallpaper Randomizer'),None,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL))
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_title(comun.APPNAME)
		self.set_icon_from_file(comun.ICON)
		self.set_default_size(350, 250)
		#
		vbox = Gtk.VBox(spacing = 5)
		self.get_content_area().add(vbox)
		#
		notebook = Gtk.Notebook.new()
		vbox.pack_start(notebook,True,True,0)
		#		
		vbox0 = Gtk.VBox(spacing = 5)
		notebook.append_page_menu(vbox0, Gtk.Label(_('Preferences')))
		frame0 = Gtk.Frame()
		vbox0.pack_start(frame0,True,True,0)
		vbox1 = Gtk.VBox(spacing = 5)
		frame0.add(vbox1)
		#
		frame1 = Gtk.Frame()
		vbox1.pack_start(frame1,True,True,0)
		#
		table1 = Gtk.Table(rows = 1, columns = 3, homogeneous = True)
		table1.set_border_width(5)
		table1.set_col_spacings(5)
		table1.set_row_spacings(5)
		frame1.add(table1)
		#
		button1 = Gtk.Button.new_with_label(_('Change it now?'))
		button1.connect('clicked',self.on_button1_clicked)
		table1.attach(button1,1,2,0,1, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)		
		#
		frame2 = Gtk.Frame()
		vbox1.pack_start(frame2,True,True,0)
		#
		table2 = Gtk.Table(rows = 4, columns = 2, homogeneous = False)
		table2.set_border_width(5)
		table2.set_col_spacings(5)
		table2.set_row_spacings(5)
		frame2.add(table2)
		#
		label11 = Gtk.Label(_('Switch on time?')+':')
		label11.set_alignment(0,.5)		
		table2.attach(label11,0,1,0,1, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)		
		self.switch11 = Gtk.Switch()
		table2.attach(self.switch11,1,2,0,1, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)		
		label21 = Gtk.Label(_('Minutes between changes')+':')
		label21.set_alignment(0,.5)		
		table2.attach(label21,0,1,1,2, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)		
		adjustment21 = Gtk.Adjustment(1, 1, 59, 1, 10, 0)
		self.spinbutton21 = Gtk.SpinButton()
		self.spinbutton21.set_adjustment(adjustment21)
		table2.attach(self.spinbutton21,1,2,1,2, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)				
		label22 = Gtk.Label(_('Hours between changes')+':')
		label22.set_alignment(0,.5)		
		table2.attach(label22,0,1,2,3, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)		
		adjustment22 = Gtk.Adjustment(0, 0, 24, 1, 10, 0)
		self.spinbutton22 = Gtk.SpinButton()
		self.spinbutton22.set_adjustment(adjustment22)
		table2.attach(self.spinbutton22,1,2,2,3, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)				
		label23 = Gtk.Label(_('Days between changes')+':')
		label23.set_alignment(0,.5)		
		table2.attach(label23,0,1,3,4, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)		
		adjustment23 = Gtk.Adjustment(0, 0, 365, 1, 10, 0)
		self.spinbutton23 = Gtk.SpinButton()
		self.spinbutton23.set_adjustment(adjustment23)
		table2.attach(self.spinbutton23,1,2,3,4, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)				
		#
		frame3 = Gtk.Frame()
		vbox1.pack_start(frame3,True,True,0)
		#
		table3 = Gtk.Table(rows = 1, columns = 2, homogeneous = False)
		table3.set_border_width(5)
		table3.set_col_spacings(5)
		table3.set_row_spacings(5)
		frame3.add(table3)
		#
		#
		label31 = Gtk.Label(_('Switch on boot?')+':')
		label31.set_alignment(0,.5)		
		table3.attach(label31,0,1,0,1, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)		
		self.switch31 = Gtk.Switch()
		table3.attach(self.switch31,1,2,0,1, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)		
		#
		vbox2 = Gtk.VBox(spacing = 5)
		notebook.append_page_menu(vbox2, Gtk.Label(_('Wallpapers')))
		frame4 = Gtk.Frame()
		vbox2.pack_start(frame4,True,True,0)
		vbox5 = Gtk.VBox(spacing = 5)
		frame4.add(vbox5)
		#
		frame5 = Gtk.Frame()
		vbox5.pack_start(frame5,True,True,0)
		#
		vbox6 = Gtk.VBox(spacing = 5)
		frame5.add(vbox6)
		button1 =Gtk.Button('chrome-os-wallpapers')
		button1.connect('clicked',self.on_button_clicked,'chrome-os-wallpapers')
		vbox2.pack_start(button1,True,True,0)
		button2 =Gtk.Button(' chrome-os-wallpapers-2015')
		button2.connect('clicked',self.on_button_clicked,'chrome-os-wallpapers-2015')
		vbox2.pack_start(button2,True,True,0)
		button3 =Gtk.Button('saucy-salamander-wallpaper-contest')
		button3.connect('clicked',self.on_button_clicked,'saucy-salamander-wallpaper-contest')
		vbox2.pack_start(button3,True,True,0)
		button4 =Gtk.Button('trusty-tahr-wallpaper-contest')
		button4.connect('clicked',self.on_button_clicked,'trusty-tahr-wallpaper-contest')
		vbox2.pack_start(button4,True,True,0)
		button5 =Gtk.Button('vivid-vervet-wallpaper-contest')
		button5.connect('clicked',self.on_button_clicked,'vivid-vervet-wallpaper-contest')
		vbox2.pack_start(button5,True,True,0)
		button6 =Gtk.Button('wily-werewolf-wallpaper-contest')
		button6.connect('clicked',self.on_button_clicked,'wily-werewolf-wallpaper-contest')
		vbox2.pack_start(button6,True,True,0)
		# Init
		self.load_preferences()
		#		
		self.show_all()
	def on_button_clicked(self,widget,wallpaper_set):
		os.system('apturl apt:%s &'%(wallpaper_set))
	def on_button1_clicked(self,widget):
		print('clicked')
		self.force_change_wallpaper()

	def get_the_job(self):
		iter = self.cron.find_comment('cron_change_wallpaper')
		jobs = list(iter)
		noj = len(jobs)
		print('Number of jobs: %s'%noj)
		if noj == 0:
			return None
		else:
			for index,ajob in enumerate(jobs):
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
			print(minutes,hours,days)		
			if minutes != '*' and minutes.find('/'):
				minutes = int(minutes.split('/')[-1])
			else:
				minutes = 1
			if hours != '*' and hours.find('/'):
				hours = int(hours.split('/')[-1])-1
			else:
				hours = 0
			if days != '*' and days.find('/'):
				days = int(days.split('/')[-1])-1
			else:
				days = 0
		self.spinbutton21.set_value(minutes)
		self.spinbutton22.set_value(hours)
		self.spinbutton23.set_value(days)
		print(minutes,hours,days)
		filestart = os.path.join(os.getenv("HOME"),".config/autostart/",comun.AUTOSTART_FILE)
		self.switch31.set_active(os.path.exists(filestart))

	def force_change_wallpaper(self):
		wallpaper = random.choice(get_not_displayed_files())
		settings = Gio.Settings.new('org.gnome.desktop.background')
		settings.set_string('picture-options', 'wallpaper')
		settings.set_string('picture-uri','file://%s'%wallpaper)
		print(wallpaper)
		add_file_to_displayed_files(wallpaper)

	def save_preferences(self):
		thejob = self.get_the_job()
		if self.switch11.get_active():
			if thejob is None:
				thejob  = self.cron.new(command='export DISPLAY=:0.0 && /usr/bin/python3 /opt/extras.ubuntu.com/simple-wallpaper-randomizer/bin/change_wallpaper.py',user=getpass.getuser())
				thejob.minute.every(10)
				thejob.set_comment("cron_change_wallpaper")
				thejob.enable()			
			thejob.enable(self.switch11.get_active())
			thejob.minute.every(self.spinbutton21.get_value())
			thejob.hour.every(self.spinbutton22.get_value()+1)
			thejob.day.every(self.spinbutton23.get_value()+1)
		else:
			if thejob is not None:
				self.cron.remove(thejob)
		filestart = os.path.join(os.getenv("HOME"),".config/autostart/",comun.AUTOSTART_FILE)				
		if self.switch31.get_active():			
			if not os.path.exists(os.path.dirname(filestart)):
				os.makedirs(os.path.dirname(filestart))
			shutil.copyfile(comun.AUTOSTART,filestart)
		else:		
			if os.path.exists(filestart):
				os.remove(filestart)		
		self.cron.write()
		print(thejob)
		
def is_image(afile):
	if isfile(afile):
		fileName, fileExtension = os.path.splitext(unquote(afile))
		if fileExtension.lower() in comun.IMAGE_EXTENSIONS:
			return True
	return False
	
def get_all_files():
	mypath='/usr/share/backgrounds'
	return [ unquote(join(mypath,f)) for f in listdir(mypath) if is_image(join(mypath,f)) ]

def get_not_displayed_files():
	all_files = get_all_files()
	displayed_files = get_displayed_files()
	for displayed_file in get_displayed_files():
		all_files.remove(displayed_file)
	return all_files
	
def get_displayed_files():
	configuration = Configuration()
	displayed_files = configuration.get('displayed_files')
	all_files = get_all_files()
	print('%s / %s'%(len(displayed_files),len(all_files)))
	if len(displayed_files) == len(all_files):# all files were showed
		displayed_files = []
		configuration.set('displayed_files',displayed_files)
		configuration.save()
	return displayed_files
	
def add_file_to_displayed_files(afile):
	configuration = Configuration()
	displayed_files = configuration.get('displayed_files')
	if afile not in displayed_files:
		displayed_files.append(afile)
	configuration.set('displayed_files',displayed_files)
	configuration.save()
		
	
if __name__ == '__main__':
	'''
	examples=['/usr/share/backgrounds/MOL_1755.jpg', '/usr/share/backgrounds/SutroSunset-rocks-misty.jpg', '/usr/share/backgrounds/IMG_0472.jpg', '/usr/share/backgrounds/the+docs.jpg', '/usr/share/backgrounds/Farewell+San+Francisco.jpg', '/usr/share/backgrounds/_DX_7114-Edit-Recovered.jpg', '/usr/share/backgrounds/7439storm2.jpg', '/usr/share/backgrounds/untitled-5.jpg', '/usr/share/backgrounds/061119-1290-HaenaSurf.jpg', '/usr/share/backgrounds/YosemiteFalls.jpg', '/usr/share/backgrounds/8941Autumn.jpg', '/usr/share/backgrounds/050925-0107-MontereySunrise.jpg', '/usr/share/backgrounds/LandsEnds-le-sunset.jpg', '/usr/share/backgrounds/The+Fickle+Mistress.jpg', '/usr/share/backgrounds/Have+You+Ever+Loved+a+Woman-3.jpg', '/usr/share/backgrounds/20140105-untitled+shoot-2908_HDR_HDR.jpg', '/usr/share/backgrounds/050618-0071-Impact.jpg', '/usr/share/backgrounds/ohau-cliff-hawaii-trey-ratcliff.jpg', '/usr/share/backgrounds/Metal-1.jpg', '/usr/share/backgrounds/TheMomentAfterSheLeft.jpg', '/usr/share/backgrounds/IMG_2705.jpg', '/usr/share/backgrounds/090810-1930-NeedleAndHaystack.jpg', '/usr/share/backgrounds/060518-0190-TamBreeze.jpg', '/usr/share/backgrounds/Pescadero.jpg', '/usr/share/backgrounds/Reflecting%2520Moonlight.jpg', '/usr/share/backgrounds/SunetReflection_16x9-Edit.jpg', '/usr/share/backgrounds/14290309900_0f6d0d94d9_o.jpg', '/usr/share/backgrounds/8280686512_7820f388dc_k.jpg', '/usr/share/backgrounds/21400647301_eb9f4dd4ff_o.jpg', '/usr/share/backgrounds/Evidence.jpg', '/usr/share/backgrounds/Tufa+at+Night.jpg', '/usr/share/backgrounds/Dark+vs+Light.jpg', '/usr/share/backgrounds/The+Edge+of+the+Day+at+Garrapata+Beach.jpg', '/usr/share/backgrounds/IMGP8993.jpg', '/usr/share/backgrounds/071121-3891-MontcitoMorn.jpg', '/usr/share/backgrounds/TunnelViewWinter.jpg', '/usr/share/backgrounds/Seattle.jpg', '/usr/share/backgrounds/DSC_0471-Edit-Edit.jpg', '/usr/share/backgrounds/Dandelion_.jpg', '/usr/share/backgrounds/DSC_5300.jpg', '/usr/share/backgrounds/IMG_2630_HDR.jpg', '/usr/share/backgrounds/stuck_04.jpg', '/usr/share/backgrounds/04_20080526.jpg', '/usr/share/backgrounds/20130724-DSC_6280-Edit.jpg', '/usr/share/backgrounds/_D3_0763-Edit-Edit.jpg', '/usr/share/backgrounds/Wyoming-5.jpg', '/usr/share/backgrounds/Rice+Fields.jpg', '/usr/share/backgrounds/IMGP8440.jpg', '/usr/share/backgrounds/IMG_1182.CR2.jpg', '/usr/share/backgrounds/070211-2329-GarrapataSurf1.jpg', '/usr/share/backgrounds/WahclelaFalls.jpg', '/usr/share/backgrounds/02202012-04.jpg', '/usr/share/backgrounds/IMG_1204.jpg', '/usr/share/backgrounds/070902-3129-BowlingBall1.jpg', '/usr/share/backgrounds/060820-0818-ThePhotogs.jpg', '/usr/share/backgrounds/TufaSunset-1-2.jpg', '/usr/share/backgrounds/C21T0861.jpg', '/usr/share/backgrounds/FI4C6008.jpg', '/usr/share/backgrounds/20100924-IMG_5794-HDR-Edit.jpg', '/usr/share/backgrounds/MWF_6457-2.jpg', '/usr/share/backgrounds/The+Grassy+Roof.jpg', '/usr/share/backgrounds/IMGP0592.jpg', '/usr/share/backgrounds/Chicago.jpg', '/usr/share/backgrounds/090424-0690-CrystCvBreakers.jpg', '/usr/share/backgrounds/IMGP8556-Edit.jpg', '/usr/share/backgrounds/McWay+Milky+Way.jpg', '/usr/share/backgrounds/color_globe.jpg', '/usr/share/backgrounds/1071616194_the+farm+of+eden.jpg', '/usr/share/backgrounds/21255366399_314b13b3c9_o.jpg', '/usr/share/backgrounds/MountainSplendor.jpg', '/usr/share/backgrounds/061012-1109-PigeonPEve.jpg', '/usr/share/backgrounds/4+horses.jpg', '/usr/share/backgrounds/Western+Point,+Acadia.jpg', '/usr/share/backgrounds/Olmsted-Sunset-1.jpg', '/usr/share/backgrounds/4624063643_1a659b8881_o.jpg', '/usr/share/backgrounds/DSCF0155-Edit.jpg', '/usr/share/backgrounds/new-england-4.jpg', '/usr/share/backgrounds/RHeaRy_465.jpg', '/usr/share/backgrounds/Trey+Ratcliff+-+OTW+to+Glen.jpg', '/usr/share/backgrounds/21266094515_066f274d3f_o.jpg', '/usr/share/backgrounds/IMG_8311.jpg', '/usr/share/backgrounds/Euphoria!_by_Tomasino.cz.jpg', '/usr/share/backgrounds/_O9V5569_HDR.jpg', '/usr/share/backgrounds/12262010-01.jpg', '/usr/share/backgrounds/Houston,+5-28-2011-634.jpg', '/usr/share/backgrounds/trey-ratcliff-close-to-tepako-new-zealand.jpg', '/usr/share/backgrounds/Murmurs+of+the+Heart,+Plate+4.jpg', '/usr/share/backgrounds/Trey+Ratcliff+-+China+2011+-+A+Great+Wall+at+Sunset.jpg', '/usr/share/backgrounds/IMG_5433.jpg', '/usr/share/backgrounds/DSC_7222-Edit-2.jpg', '/usr/share/backgrounds/3550Levitate.jpg', '/usr/share/backgrounds/DSC02146+Red+Plant.jpg', '/usr/share/backgrounds/BeanHollow-sunset-surf.jpg', '/usr/share/backgrounds/IMG_0725.jpg', '/usr/share/backgrounds/213125_1600x1200+(3).jpg', '/usr/share/backgrounds/RHeaRy_380.jpg', '/usr/share/backgrounds/by+Russ+Bishop.jpg', '/usr/share/backgrounds/California+State+Fair+2009-395.jpg', '/usr/share/backgrounds/rainier-bridge-07-22-2014.jpg', '/usr/share/backgrounds/IMG_5755.jpg', '/usr/share/backgrounds/MorningGlory.jpg', '/usr/share/backgrounds/Lupines.jpg', '/usr/share/backgrounds/2012.+purple+is+my+favorite+color.jpg', '/usr/share/backgrounds/061122-1421-LtAtEndOfPier.jpg', '/usr/share/backgrounds/IMGP1985_stitch.jpg', '/usr/share/backgrounds/IMGP4685-2_HDRmasked-Edit.jpg', '/usr/share/backgrounds/IMGP1485-Edit.jpg', '/usr/share/backgrounds/IMG_2526-3b.jpg', '/usr/share/backgrounds/5-20-11-sunset-clouds365-kdelay.jpg', '/usr/share/backgrounds/DSC_8703.jpg', '/usr/share/backgrounds/DryLeaf.jpg', '/usr/share/backgrounds/RodeoBeach-firespinning-2.jpg', '/usr/share/backgrounds/Sand+Beach+Texture-4.jpg', '/usr/share/backgrounds/IMG_20130330_120430-Edit.jpg', '/usr/share/backgrounds/3189889363_6357f5f645_o.jpg', '/usr/share/backgrounds/Invitation.jpg', "/usr/share/backgrounds/Hell's+Gate+Bridge-6.jpg", '/usr/share/backgrounds/bubble_junky.jpg', '/usr/share/backgrounds/Tranquil_by_Pat_David.jpg', '/usr/share/backgrounds/_MG_0139.jpg', '/usr/share/backgrounds/_X7A5208-Edit.jpg', '/usr/share/backgrounds/01_MG_3677.jpg', '/usr/share/backgrounds/One+Trick+Pony.jpg', '/usr/share/backgrounds/dsc_4194.jpg', '/usr/share/backgrounds/02212012-08.jpg', '/usr/share/backgrounds/_DX_6908_09_10_11_32bit-Edit.jpg', '/usr/share/backgrounds/DarkSide.jpg', '/usr/share/backgrounds/20130915-7372-34873c91-2048.jpg', '/usr/share/backgrounds/GGB-Wave_mono-square.jpg', '/usr/share/backgrounds/20121030-(08_21_49)-salisbury-plain-ample-bay-5167-Edit.jpg', '/usr/share/backgrounds/IMG_1017.jpg', '/usr/share/backgrounds/Sharpened-version.jpg', '/usr/share/backgrounds/388A3302.jpg', '/usr/share/backgrounds/7995122298_d4743a46ce_k.jpg', '/usr/share/backgrounds/A+View+from+the+Ranch+in+Argentina.jpg', '/usr/share/backgrounds/Fitzgerald+Streaks.jpg', '/usr/share/backgrounds/MOL_2167.jpg', '/usr/share/backgrounds/LandsEnd-sunset-2.jpg', '/usr/share/backgrounds/Tesla_by_Tomasino.cz.jpg', '/usr/share/backgrounds/IMG_1311.jpg', '/usr/share/backgrounds/CC+-+Dry+Tortuga.jpg', '/usr/share/backgrounds/Red+by+Alistair+Nicol.jpg', '/usr/share/backgrounds/_MG_1449.jpg', '/usr/share/backgrounds/KeeSummer-1920.jpg', '/usr/share/backgrounds/tekapo-new-zealand-trey-ratcliff-2.jpg', '/usr/share/backgrounds/Horseshoe+Bend+Sunset.jpg', '/usr/share/backgrounds/RayofHope.jpg', '/usr/share/backgrounds/13109364663_8021e6b91d_o.jpg', '/usr/share/backgrounds/trey-ratcliff-road-to-mountain-forever.jpg', '/usr/share/backgrounds/MagicBallContest.jpg', '/usr/share/backgrounds/Exposed.jpg', '/usr/share/backgrounds/IMG_7006-Edit.jpg', '/usr/share/backgrounds/trey-ratcliff-queenstown-nz-nikon-d800.jpg', '/usr/share/backgrounds/The+Dream+Catcher+-+Palouse,WA.jpg', '/usr/share/backgrounds/4088949046_5d094cb2e2_o.jpg', '/usr/share/backgrounds/Moss_inflorescence_by_carmelo75.jpg', '/usr/share/backgrounds/091220-2536-TheCurl.jpg', '/usr/share/backgrounds/Night+Falls+on+Crater+Lake+-+Crater+Lake,+OR1.jpg', '/usr/share/backgrounds/inverness-to-istanbul-00177.jpg', '/usr/share/backgrounds/frolicking_worker_bee.jpg', '/usr/share/backgrounds/Glacier+Point+Milky+Way+Panorama.jpg', '/usr/share/backgrounds/IMG_0935.jpg', '/usr/share/backgrounds/paoWS.jpg', '/usr/share/backgrounds/DSC03916+Green+Leaf+Texture.jpg', '/usr/share/backgrounds/GrayWhaleCove.jpg', '/usr/share/backgrounds/tempest+(1)-Edit.jpg', '/usr/share/backgrounds/bondi_sml.jpg', '/usr/share/backgrounds/3505475407_d776e4d589_o-1.jpg', '/usr/share/backgrounds/IMG_1109_HDR.jpg', '/usr/share/backgrounds/080229-4653-GraytonStream.jpg', '/usr/share/backgrounds/DSC_4067.jpg', '/usr/share/backgrounds/IMG_3857-Edit-Edit-2.jpg', '/usr/share/backgrounds/090102-0157-BirdRock.jpg', '/usr/share/backgrounds/Rockaway+Sunset+Sky.jpg', '/usr/share/backgrounds/POD+2013-01-13.jpg', '/usr/share/backgrounds/IMG_7939+he.jpg', '/usr/share/backgrounds/Kona-Hawaii-Stormy-Sky.jpg', '/usr/share/backgrounds/Highway+1.jpg', '/usr/share/backgrounds/Another+Rockaway+Sunset.jpg', '/usr/share/backgrounds/20120128-20120128-ENS_3119_20_21_tonemapped-Edit.jpg', '/usr/share/backgrounds/tree+in+the+park.jpg', '/usr/share/backgrounds/Islands.jpg', '/usr/share/backgrounds/The+Night+is+Coming.jpg', '/usr/share/backgrounds/100722-4061-LaupahoehoeCove.jpg', '/usr/share/backgrounds/SealRocks-sunset-beach-rock.jpg', '/usr/share/backgrounds/MOL_2238-Edit.jpg', '/usr/share/backgrounds/GMZzGwX.jpg', '/usr/share/backgrounds/DSC_1557-Edit.jpg', '/usr/share/backgrounds/070319-2657-PathToLight.jpg', '/usr/share/backgrounds/inverness-to-istanbul-00077.jpg', '/usr/share/backgrounds/060408-1938-GarrapataFlow.jpg', '/usr/share/backgrounds/071110-3579-HvnsGate.jpg', '/usr/share/backgrounds/Not+Enough+Wonder+in+the+World.jpg', '/usr/share/backgrounds/HaenaReflections-1920.jpg', '/usr/share/backgrounds/Trey+Ratcliff+-+Queenstown+Aurora+Australis.jpg', '/usr/share/backgrounds/GGB-SlackersRidge-Sunrise-fog-headlights-wide.jpg', '/usr/share/backgrounds/100804-4696-PololuMorn1.jpg', '/usr/share/backgrounds/rose_of_love_and_light.jpg', '/usr/share/backgrounds/071229-4231-SandstNSky1.jpg', '/usr/share/backgrounds/IMG_0242.jpg', '/usr/share/backgrounds/2012-Favorites-3.jpg', '/usr/share/backgrounds/20130307-(12_46_39)-tahoe-5d3-15940.jpg', '/usr/share/backgrounds/Ripples.jpg', '/usr/share/backgrounds/Little+Bit+of+Paradise.jpg', '/usr/share/backgrounds/21158335342_d1c7cf23ef_o.jpg', '/usr/share/backgrounds/06152012-12.jpg', '/usr/share/backgrounds/Mysore+Palace.jpg', '/usr/share/backgrounds/IMG_4701.jpg', '/usr/share/backgrounds/388A3363.jpg', '/usr/share/backgrounds/img_0571.jpg', '/usr/share/backgrounds/IMGP7317_18_19_20_tonemapped.jpg', '/usr/share/backgrounds/Darker+Sort+of+Love.jpg', '/usr/share/backgrounds/IMG_3857-Edit-Edit.jpg', '/usr/share/backgrounds/farm_in_the_prairie.jpg', '/usr/share/backgrounds/reunion.jpg', '/usr/share/backgrounds/4070581709_a1c668a779_o.jpg', '/usr/share/backgrounds/Pole+With+The+View.jpg', '/usr/share/backgrounds/Houston,+5-28-2011-160.jpg', '/usr/share/backgrounds/Hanging+Leaf.jpg', '/usr/share/backgrounds/JFU+POD+2012-05-21.jpg', '/usr/share/backgrounds/RubyBeachSunset.jpg', '/usr/share/backgrounds/IMGP9276.jpg', '/usr/share/backgrounds/Lonely+Rock.jpg', '/usr/share/backgrounds/07_20090416.jpg', '/usr/share/backgrounds/Pier+7.jpg', '/usr/share/backgrounds/G+.jpg', '/usr/share/backgrounds/Bristlecone_Stars.jpg', '/usr/share/backgrounds/IMGP7962.jpg', '/usr/share/backgrounds/New+York+-+NEX7+-+Trey+Ratcliff+(8+of+21).jpg', '/usr/share/backgrounds/Sitting_Here,_Making_Fun_by_Philipp_Haegi.jpg', '/usr/share/backgrounds/091009-2169-LibOfAges3.jpg', '/usr/share/backgrounds/untitled+(101+of+207).jpg', '/usr/share/backgrounds/on_the_road.jpg', '/usr/share/backgrounds/060506-0094-Farscape.jpg', '/usr/share/backgrounds/IMG_3027.jpg', '/usr/share/backgrounds/21455163031_cc9f7247c8_o.jpg', '/usr/share/backgrounds/GoldenFalls-1920b.jpg', '/usr/share/backgrounds/Dare+to+Dream.jpg', '/usr/share/backgrounds/IMG_1531.jpg', '/usr/share/backgrounds/071022-3473-NightScape.jpg', '/usr/share/backgrounds/Christmas_Lights_by_RaDu_GaLaN.jpg', '/usr/share/backgrounds/ENS-+Macro+Snow-.jpg', '/usr/share/backgrounds/Seattle_BrianMatiash.jpg', '/usr/share/backgrounds/IMG_5974.jpg', '/usr/share/backgrounds/Low+Tide+Textures+at+Little+Hunter+Beach.jpg', '/usr/share/backgrounds/TwilightRocks_SanMateoCoast-2.jpg', '/usr/share/backgrounds/After+the+Storm.jpg', '/usr/share/backgrounds/Take+It+or+Leave+It.jpg', '/usr/share/backgrounds/21229839068_d09e2e5039_o.jpg', '/usr/share/backgrounds/20121026-(12_10_32)-cumberland-bay-3122-Edit.jpg', '/usr/share/backgrounds/SonomaCoast-Arch-surf-longexp.jpg', '/usr/share/backgrounds/warty-final-ubuntu.png', '/usr/share/backgrounds/Funston-Sunset.jpg', '/usr/share/backgrounds/3054580997_b9c89c7d9f_o.jpg', '/usr/share/backgrounds/Antelope+Hallway.jpg', '/usr/share/backgrounds/tah+prohm+ruins.jpg', '/usr/share/backgrounds/PatriciaLake.jpg', '/usr/share/backgrounds/oil3.jpg', '/usr/share/backgrounds/20130307-(12_35_23)-tahoe-iq180-16274.jpg', '/usr/share/backgrounds/Stream_xps13_Oct-18-101543-2015_Conflict.jpg', '/usr/share/backgrounds/ToxawayLake.jpg', '/usr/share/backgrounds/20746999743_2545f7e9eb_o.jpg', '/usr/share/backgrounds/MOL_1841.jpg', '/usr/share/backgrounds/A+Deep+Blue.jpg', '/usr/share/backgrounds/Spins+Free-3.jpg', '/usr/share/backgrounds/061120-1380-HanaleiBonfire.jpg', '/usr/share/backgrounds/20100525-IMG_6788-HDR-Edit.jpg', '/usr/share/backgrounds/LandsEnd-Sunset.jpg', '/usr/share/backgrounds/End+Game+.jpg', '/usr/share/backgrounds/Antelope+Weeping+Eye.jpg', '/usr/share/backgrounds/20090411_132734_.jpg', '/usr/share/backgrounds/110121-7113-LightForce.jpg', '/usr/share/backgrounds/IMGP0652_3_4_tonemapped.jpg', '/usr/share/backgrounds/_MSU3203.jpg', '/usr/share/backgrounds/21233025279_56c0225489_o.jpg', '/usr/share/backgrounds/Abstract_Ubuntu_by_Marek_Koteluk.jpg', '/usr/share/backgrounds/David+Morrow-1.jpg', '/usr/share/backgrounds/060518-0179-TamRedwoods.jpg', '/usr/share/backgrounds/Stay+With+Me.jpg', '/usr/share/backgrounds/IMG_7449.jpg', '/usr/share/backgrounds/Lone+Pine+Sunset.jpg', '/usr/share/backgrounds/DSC_6674-Edit-Edit.jpg', '/usr/share/backgrounds/8031438226_5713c1a86c_o.jpg', '/usr/share/backgrounds/DSC_6930-Edit-Edit.jpg', '/usr/share/backgrounds/DSC_4393.jpg', '/usr/share/backgrounds/110627-8240-Myst.jpg', '/usr/share/backgrounds/Portofino2.jpg', '/usr/share/backgrounds/ConvictLake+(2+of+3).jpg', '/usr/share/backgrounds/_dsc9194-edit.jpg', '/usr/share/backgrounds/The+Rocks+of+Iceland.jpg', '/usr/share/backgrounds/Despair.jpg', '/usr/share/backgrounds/IMGP5017.jpg', '/usr/share/backgrounds/2398605326_bf7dde0cf7_o.jpg', '/usr/share/backgrounds/Hotel_by_sarcasmrules2011.jpg', '/usr/share/backgrounds/15092772979_755e42f46d_o.jpg', '/usr/share/backgrounds/1134103121_gateway+to+the+temple+of+heaven.jpg', '/usr/share/backgrounds/David+Morrow-1-28.jpg', '/usr/share/backgrounds/ViewToKilauea-1920.jpg', '/usr/share/backgrounds/Full+Moon+Pull+1.jpg', '/usr/share/backgrounds/Basses2.jpg', '/usr/share/backgrounds/C21T0817.jpg', '/usr/share/backgrounds/13990659923_351ec9aabe_o.jpg', '/usr/share/backgrounds/HerbertLake-2.jpg', '/usr/share/backgrounds/20130805_mit_and_river_00001-2.jpg', '/usr/share/backgrounds/final+copy+Second+Beach.jpg', '/usr/share/backgrounds/20140204_Iceland_0234_5_6_32bit.jpg', '/usr/share/backgrounds/Polka_Dots_and_Moonbeams_by_SirPecanGum.jpg', '/usr/share/backgrounds/Hooded+Lady+of+the+Valley.jpg', '/usr/share/backgrounds/space_needle_scarlet.jpg', '/usr/share/backgrounds/Motion.jpg', '/usr/share/backgrounds/Group+TWO.jpg', '/usr/share/backgrounds/110205-7264-GrayWCoveSurf.jpg', '/usr/share/backgrounds/IMGP7287.jpg', '/usr/share/backgrounds/DSC_6464.jpg', '/usr/share/backgrounds/IMGP9268.jpg', '/usr/share/backgrounds/DunesEdge.jpg', '/usr/share/backgrounds/110521-8046-PacificaLt2.jpg', '/usr/share/backgrounds/by+Joel++Tjintjelaar.jpg', '/usr/share/backgrounds/SealRocks-sunset-reflection.jpg', '/usr/share/backgrounds/050518-2044-KeeEvening.jpg', '/usr/share/backgrounds/IMG_0366.jpg', '/usr/share/backgrounds/Panamint_Dunes.jpg', '/usr/share/backgrounds/061228-2049-UTPScripps1.jpg', '/usr/share/backgrounds/20121024-(08_52_33)-right-whale-beach-1842-Edit.jpg', '/usr/share/backgrounds/Chrysler+Building,+NYC.jpg', '/usr/share/backgrounds/Last+Light+at+Garrapata.jpg', '/usr/share/backgrounds/10-13-12highres.jpg', '/usr/share/backgrounds/SanGregLight1800.jpg', '/usr/share/backgrounds/Blue_by_dariuskws.jpg', '/usr/share/backgrounds/Iceland.jpg', '/usr/share/backgrounds/3K9C4807.jpg', '/usr/share/backgrounds/GGate+Dawn+from+Slacker+Hill.jpg', '/usr/share/backgrounds/The+Cave.jpg', '/usr/share/backgrounds/dsc_0056.jpg', '/usr/share/backgrounds/MOL_1600.jpg', '/usr/share/backgrounds/Tenerife_Roques_de_Anaga_by_Frederik_Schulz.jpg', '/usr/share/backgrounds/MorningBlue-2.jpg', '/usr/share/backgrounds/IMG_7808.jpg', '/usr/share/backgrounds/Seal+Cove.jpg', '/usr/share/backgrounds/388A1845.jpg', '/usr/share/backgrounds/IMGP0430.jpg', '/usr/share/backgrounds/MarshallBeachSunset.jpg', '/usr/share/backgrounds/20111009-(07_08_56)-sierras-5d2-7923And2more-Edit-Edit.jpg', '/usr/share/backgrounds/IMG_2388+e.jpg', '/usr/share/backgrounds/DSC_1556-Edit.jpg', '/usr/share/backgrounds/IMG_1221.jpg', '/usr/share/backgrounds/JFU+POD+2012-07-12.jpg', '/usr/share/backgrounds/100530-3924-Orbs1.jpg', '/usr/share/backgrounds/080820-5209-MakenaLL.jpg', '/usr/share/backgrounds/Startrails_Nov3.jpg', '/usr/share/backgrounds/Chef+at+Sunset.jpg', '/usr/share/backgrounds/12-11-12-original.jpg', '/usr/share/backgrounds/Reef-mono.jpg', '/usr/share/backgrounds/IMG_2617.jpg', '/usr/share/backgrounds/_MSU8463.jpg', '/usr/share/backgrounds/Tramonto_a_Scalea_by_Renatvs88.jpg', '/usr/share/backgrounds/The+Beach.jpg', '/usr/share/backgrounds/cleardrop.jpg', '/usr/share/backgrounds/Suru_Wallpaper_Desktop_4096x2304_Gray.png', '/usr/share/backgrounds/The+Farm+of+Eden.jpg', '/usr/share/backgrounds/Interlocking.jpg', '/usr/share/backgrounds/Blue.jpg', '/usr/share/backgrounds/AtAnchor.jpg', '/usr/share/backgrounds/IMG_2452.jpg', '/usr/share/backgrounds/dock-3.jpg', '/usr/share/backgrounds/Outflow.jpg', '/usr/share/backgrounds/IMGP7962-2.jpg', '/usr/share/backgrounds/MArshallBeach-sky-surf-rocks.jpg', '/usr/share/backgrounds/florida-5.jpg', '/usr/share/backgrounds/IMG_1984.jpg', '/usr/share/backgrounds/DSC_0267_8_9_tonemapped-Edit-1.jpg', '/usr/share/backgrounds/388A3234.jpg', '/usr/share/backgrounds/SecondBeach2.jpg', '/usr/share/backgrounds/GGB-MarshallBeach-lightSky.jpg', '/usr/share/backgrounds/20110710-160024.jpg', '/usr/share/backgrounds/MakingTracksForHome.jpg', '/usr/share/backgrounds/14573905897_be892ac323_o.jpg', '/usr/share/backgrounds/16101646308_14f7b7f9eb_o.jpg', '/usr/share/backgrounds/austin+2.jpg', '/usr/share/backgrounds/DSC_0444_5_6-Edit.jpg', '/usr/share/backgrounds/20859746630_cc74e3fffc_o.jpg', '/usr/share/backgrounds/388A4957.jpg', '/usr/share/backgrounds/DSC01099+Plant.jpg', '/usr/share/backgrounds/tree.jpg', '/usr/share/backgrounds/I+Cover+the+Waterfront+-+Alki+Beach,+WA.jpg', '/usr/share/backgrounds/SutroSunset-surf-burn.jpg', '/usr/share/backgrounds/090227-0384-McCluresPoint.jpg', '/usr/share/backgrounds/061012-1078-PelicanCove.jpg', '/usr/share/backgrounds/the+lonely+grass+house.jpg', '/usr/share/backgrounds/300928932_3bf6d408df_o.jpg', '/usr/share/backgrounds/forest+fog+v2.jpg', '/usr/share/backgrounds/PVK_5178.jpg', '/usr/share/backgrounds/Trey+Ratcliff+-+China+2011+-+The+Egg+at+Sunset.jpg', '/usr/share/backgrounds/TetonShwabacher.jpg', '/usr/share/backgrounds/A+Razor+to+the+Sky.jpg', '/usr/share/backgrounds/Silver+Lake+StarTrails.jpg', '/usr/share/backgrounds/IMGP4090-Edit.jpg', '/usr/share/backgrounds/sky_leaves.jpg', '/usr/share/backgrounds/150305-cinqAA_by_Pierre_Cante.jpg', '/usr/share/backgrounds/final.jpg', '/usr/share/backgrounds/071229-4235-SandstNSky2.jpg', '/usr/share/backgrounds/_MG_4776.CR2.jpg', '/usr/share/backgrounds/red+bridge+in+late+afternoon.jpg', '/usr/share/backgrounds/blue4.jpg', '/usr/share/backgrounds/Sutro+Baths+Sunset.jpg', '/usr/share/backgrounds/T3_IMG_3936.jpg', '/usr/share/backgrounds/IMGP8003.jpg', '/usr/share/backgrounds/3425202839_7a6b829432_o.jpg', '/usr/share/backgrounds/20140328_Hawaii_2209-Edit-Edit.jpg', '/usr/share/backgrounds/9082667654_c7919ec6ed_o.jpg', '/usr/share/backgrounds/ibiza+dock.jpg', '/usr/share/backgrounds/19216651096_52561b8976_o.jpg', '/usr/share/backgrounds/maui-13.jpg', '/usr/share/backgrounds/DSC01070+Mosaic.jpg', '/usr/share/backgrounds/Bonzai+Rock+Sunset.jpg', '/usr/share/backgrounds/IMG_4460.jpg', '/usr/share/backgrounds/GoldenFalls-1920.jpg', '/usr/share/backgrounds/PVK_5085.jpg', '/usr/share/backgrounds/The+Blue+City.jpg', '/usr/share/backgrounds/MSU_1184.jpg', '/usr/share/backgrounds/21103394645_2e59b9e36a_o.jpg', '/usr/share/backgrounds/060607-0405-PillarsPast.jpg', '/usr/share/backgrounds/OceanBeach_sunset_ripples.jpg', '/usr/share/backgrounds/IMGP4467.jpg', '/usr/share/backgrounds/GGB_130628_MCu_1-2.jpg', '/usr/share/backgrounds/MWF_8382-3ps.jpg', '/usr/share/backgrounds/MWF_2155.jpg', '/usr/share/backgrounds/GGB_DarkMorningWindyFog.jpg', '/usr/share/backgrounds/061112-1181-Portal2BigSur.jpg', '/usr/share/backgrounds/FI4C4577.jpg', '/usr/share/backgrounds/_dsc9224-edit.jpg', '/usr/share/backgrounds/Column+of+Light.jpg', '/usr/share/backgrounds/Seal+Rocks-Edit.jpg', '/usr/share/backgrounds/theedge.jpg', '/usr/share/backgrounds/LowerAntelope1.jpg', '/usr/share/backgrounds/14060198835_4bfebc4a48_o.jpg', '/usr/share/backgrounds/21455138181_766da8efd0_o.jpg', '/usr/share/backgrounds/ConvictLakeSunrise.jpg', '/usr/share/backgrounds/Traviny_by_Tomasino.cz.jpg', '/usr/share/backgrounds/_X7A8818-Edit.jpg', '/usr/share/backgrounds/Lines.jpg', '/usr/share/backgrounds/David+Morrow-22.jpg', '/usr/share/backgrounds/The+Infinity+of+Tokyo.jpg', '/usr/share/backgrounds/21265991816_ba8e4925e9_o.jpg', '/usr/share/backgrounds/DSC_3091-Edit.jpg', '/usr/share/backgrounds/DSC_0300.jpg', '/usr/share/backgrounds/20101103_TorresDelPaine_Cuernos_Horns_6215_blended-Edit-Edit-Edit.jpg', '/usr/share/backgrounds/IMGP0184.jpg', '/usr/share/backgrounds/The+Solar+Flower.jpg', '/usr/share/backgrounds/Reflection.jpg', '/usr/share/backgrounds/DSC_2857.jpg', '/usr/share/backgrounds/Patience.jpg', '/usr/share/backgrounds/32+Hours+&+Counting.jpg', '/usr/share/backgrounds/David+Morrow-11.jpg', '/usr/share/backgrounds/path_of_leaves.jpg', '/usr/share/backgrounds/20828743919_7735946fbc_o.jpg', '/usr/share/backgrounds/388A1865_HDR.jpg', '/usr/share/backgrounds/DSC_6436.jpg', '/usr/share/backgrounds/Bryce+Canyon.jpg', '/usr/share/backgrounds/061125-1635-Maelstrom3.jpg', '/usr/share/backgrounds/David+Morrow-1-53.jpg', '/usr/share/backgrounds/100409-3657-PinnacleRock3.jpg', '/usr/share/backgrounds/1171692863_the+eiffel+from+beneath.jpg', '/usr/share/backgrounds/Thamserku.jpg', '/usr/share/backgrounds/976865336_a+view+of+queenstown.jpg', '/usr/share/backgrounds/DSC_0554.jpg', '/usr/share/backgrounds/02202012-01.jpg', '/usr/share/backgrounds/shades_of_blue.jpg', '/usr/share/backgrounds/IMG_1064-2.jpg', '/usr/share/backgrounds/StillStanding.jpg', '/usr/share/backgrounds/CrissyField-SaltMarsh-2.jpg', '/usr/share/backgrounds/20120820_road_to_bourg_00001.jpg', '/usr/share/backgrounds/DSC_1351.jpg', '/usr/share/backgrounds/20140310_Iceland_1392-Edit.jpg', '/usr/share/backgrounds/untouched.jpg', '/usr/share/backgrounds/RodeoBeach-sunset-16x9.jpg', '/usr/share/backgrounds/BakerBeach-SunsetColor.jpg', '/usr/share/backgrounds/The+Most+Beautiful+Road+in+the+World.jpg', '/usr/share/backgrounds/100731-4524-HapunaLight1.jpg', '/usr/share/backgrounds/090911-2088-AngelIslandSky2.jpg', '/usr/share/backgrounds/IMG_3144-3.jpg', '/usr/share/backgrounds/DSC_0540_39_41-Edit.jpg', '/usr/share/backgrounds/BayBridge-night-mono.jpg', '/usr/share/backgrounds/untitled-3-2.jpg', '/usr/share/backgrounds/090102-0143-SeaAndStorm.jpg', '/usr/share/backgrounds/100726-4239-LightAtAhalanui.jpg', '/usr/share/backgrounds/River+and+Mount.jpg', '/usr/share/backgrounds/CC+-+Sunrise+at+Miami+Beach.jpg', '/usr/share/backgrounds/The+Road+to+Lindis+Pass.jpg', '/usr/share/backgrounds/Mediterranean_Sea_by_simosx.jpg', '/usr/share/backgrounds/Colorado+River+Sunset.jpg', '/usr/share/backgrounds/In+Motion.jpg', '/usr/share/backgrounds/DSC_6902-Edit-Edit.jpg', '/usr/share/backgrounds/SanGregorioCliffReflection.jpg', '/usr/share/backgrounds/IMG_0293+he.jpg', '/usr/share/backgrounds/santa-cruz-trey-ratcliff.jpg', '/usr/share/backgrounds/MWF_6016.jpg', '/usr/share/backgrounds/Secret+Cove.jpg', '/usr/share/backgrounds/Sailing+Stones.jpg', '/usr/share/backgrounds/In+a+Foreign+Land+-+West+Fjords,+Iceland.jpg', '/usr/share/backgrounds/Primavera_by_Vivian_Morales.jpg', '/usr/share/backgrounds/Rust.jpg', '/usr/share/backgrounds/1-24-13.jpg', '/usr/share/backgrounds/070823-3044-PinnacleRock1.jpg', '/usr/share/backgrounds/Bean+Hollow+Sunset+2048.jpg', '/usr/share/backgrounds/Big-Sur-Coastal-Seascape-2.jpg', '/usr/share/backgrounds/SFBay-Sunrise-Hank-n-Pilings-2.jpg', "/usr/share/backgrounds/Trippin'-3.jpg", '/usr/share/backgrounds/071010-3287-SausMorn1.jpg', '/usr/share/backgrounds/080327-4706-JoshuaTreeOasis.jpg', '/usr/share/backgrounds/110429-7971-Faultlines.jpg', '/usr/share/backgrounds/full_moon_rise.jpg', '/usr/share/backgrounds/SutroSunset-WaterfallRock.jpg', '/usr/share/backgrounds/Trey+Ratcliff+-+New+York+-+Inception.jpg', '/usr/share/backgrounds/20545885454_85d4738117_o.jpg', '/usr/share/backgrounds/TetonSnakeOverlook.jpg', '/usr/share/backgrounds/6979723276_d91841e9f1_k.jpg', '/usr/share/backgrounds/Valley+Sunset.jpg', '/usr/share/backgrounds/RHeaRy_402.jpg', '/usr/share/backgrounds/8670434759_91e92fd1ee_k.jpg', '/usr/share/backgrounds/DolphinWalk.jpg', '/usr/share/backgrounds/Light_my_fire_evening_sun_by_Dariusz_Duma.jpg', '/usr/share/backgrounds/Trey+Ratcliff+-+NEX+7-+Sunset+2.jpg', '/usr/share/backgrounds/8272381830_825c27ae6b_k.jpg', '/usr/share/backgrounds/Seal_Rocks-centered.jpg', '/usr/share/backgrounds/217440037_8ca190627e_o.jpg', '/usr/share/backgrounds/21158301482_c1d0087c39_o.jpg', '/usr/share/backgrounds/071229-4276-LaJollaFalls.jpg', '/usr/share/backgrounds/_DX_3511_2_3_4_5_32bit-Edit.jpg', '/usr/share/backgrounds/CC+-+Santa+Cruz+Natural+Bridges.jpg', '/usr/share/backgrounds/the+trane+and+the+pharoah.jpg', '/usr/share/backgrounds/071227-4144-PtLomaReef.jpg', '/usr/share/backgrounds/Sierra+Heavens.jpg', '/usr/share/backgrounds/IMG_0642.jpg', '/usr/share/backgrounds/Temple+Over+Kyoto.jpg', '/usr/share/backgrounds/DSC_4154b.jpg', '/usr/share/backgrounds/Sloat-SunsetBeachFoam.jpg']
	examples=[]
	for afile in examples:
		add_file_to_displayed_files(afile)
	print(get_all_files())
	print(get_displayed_files())
	print(get_not_displayed_files())
	'''
	swrd = SimpleWallpaperRandomizerDialog()
	if swrd.run() == Gtk.ResponseType.ACCEPT:
		swrd.save_preferences()


'''
cron = CronTab(user=True)
iter = cron.find_comment('cron_change_wallpaper')
for ajob in list(iter):
	cron.remove(ajob)


job  = cron.new(command='/home/lorenzo/Escritorio/change_wallpaper.sh')
job.set_comment("cron_change_wallpaper")
job.minute.every(1)
job.enable()
print(job.is_valid())
cron.write()
for job in cron:
	print(job)
'''
