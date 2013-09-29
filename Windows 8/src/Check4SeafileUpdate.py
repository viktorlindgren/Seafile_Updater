from ConfigHandler import loadConfig, saveConfig, timeSinceLastCheck, confExisted
from subprocess import Popen
import tempfile, platform
import urllib2, re, os
import time

url = "http://seafile.com/en/download/"

def getPath():
	sep = os.sep
	sfStart = "%sSeafile%sbin%sseafile-applet.exe" % (sep,sep,sep)
	getPath = os.environ["ProgramFiles"]+sfStart
	if not(os.path.exists(getPath)):
		getPath = os.environ["ProgramFiles(x86)"] + sfStart
		if not(os.path.exists(getPath)):
			raise Exception("Warning: Could not start seafile")
	return getPath

def dl(url):
	response = urllib2.urlopen(url)
	r = response.read()
	response.close()
	return r


def update(url, oldaddr):

	data = dl(url)
	regexp = "<a href=(?:\"|\')(.+).msi"
	regex = re.compile(regexp,re.MULTILINE)

	addr = regex.findall(data)[0] + ".msi"

	if addr == oldaddr: # Don't install same version again
		return addr

	f = tempfile.NamedTemporaryFile(suffix='.msi', delete=False)

	f.write(dl(addr))
	f.close()

	# Install the file
	cmd = "msiexec /passive /quiet /i %s %s" % (f.name,"/l*v %temp%\\msi.log")
	installerStatusCode = Popen(cmd, shell=True).wait()

	try:
		# Starting seafile again
		cmd = "\"%s\"" % getPath()
		Popen(cmd)
	except:
		print "Warning: Could not find the installed path, please start seafile manually."

	if installerStatusCode != 0:
		raise Exception("Installing went wrong")
	return addr

if __name__ == "__main__":
	if not "Windows" in platform.platform():
		raise Exception("The autoupdate only works on windows")

	last_updated, interval_in_days, installed_addr = loadConfig()
	if not confExisted: # Updated directly first time
		interval_in_days = 0

	while True:
		passedtime = timeSinceLastCheck(last_updated)
		time.sleep(max(interval_in_days*24*3600-passedtime,0))

		try:
			installed_addr = update(url,installed_addr)
		except Exception, e:
			print e
			with open("seafile.debug.log", 'w') as debuglog:
				debuglog.write(e)

		last_updated, interval_in_days, _ = loadConfig()
		saveConfig(interval_in_days,installed_addr)
