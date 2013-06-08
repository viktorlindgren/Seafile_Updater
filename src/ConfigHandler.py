from datetime import datetime
import ConfigParser,os

section = "Seafile Updater"

config = ConfigParser.RawConfigParser()
dateformat = "%Y-%m-%d %H:%M:%S"

settingsfolder = (os.getenv('AppData') or os.getenv('HOME') + ".config/") + \
	os.sep + section
configPath = settingsfolder + os.sep + "config.txt"

def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)

ensure_dir(configPath)
confExisted = os.path.exists(configPath)

def timeSinceLastCheck(lastcheck):

	now = datetime.now()
	return (now - lastcheck).total_seconds()


def saveConfig(interval_in_days,installed_addr):

	try:
		config.add_section(section)
	except ConfigParser.DuplicateSectionError:
		pass


	config.set(section, 'interval_in_days',interval_in_days)
	config.set(section, 'last_updated', datetime.now().strftime(dateformat))
	config.set(section, 'installed_addr',installed_addr)

	with open(configPath, 'wb') as configfile:
		config.write(configfile)

def loadConfig():

	# Default values
	interval_in_days = 7
	last_updated = None
	installed_addr = ""

	try:
		config.read(configPath)
	except:
		pass
	try:
		interval_in_days = config.getint(section, "interval_in_days")
		assert interval_in_days > 0, "Invalid interval_in_days time, must be more than 0 days"
	except:
		pass
	try:
		last_updated_str = config.get(section, 'last_updated')
		last_updated = datetime.strptime(last_updated_str, dateformat)
	except:
		pass
	try:
		installed_addr = config.get(section, 'installed_addr')
	except:
		pass
	return last_updated, interval_in_days,installed_addr


