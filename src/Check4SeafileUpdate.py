from subprocess import Popen,PIPE
import urllib2, re, os
import tempfile, platform
import time
from ConfigHandler import loadConfig, saveConfig, timeSinceLastCheck, confExisted

url = "http://seafile.com/en/download/"

def getPath():
	sep = os.sep
	sfStart = "%sSeafile%sbin%sseafile-applet.exe" % (sep,sep,sep)
	getPath = os.environ["ProgramFiles"]+sfStart
	if not(os.path.exists(getPath)):
		getPath = os.environ["ProgramFiles(x86)"] + sfStart
		if not(os.path.exists(getPath)):
			raise "Warning: Could not start seafile"
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

	# Shutdown any running seafile
	cmd = "taskkill /im seafile-applet.exe"
	pipe = Popen(cmd, shell=True).wait()

	# Check that it is really dead
	cmd ='tasklist /FI "IMAGENAME eq seafile-applet.exe"'
	pipe = Popen(cmd, shell=True, stdout=PIPE).stdout
	output = pipe.read()

	if "PID" in output:
		raise "Failed to kill seafile nicely, please close the application"

	# Install the file
	cmd = "msiexec /passive /quiet /i %s" % f.name
	if Popen(cmd, shell=True).wait() != 0:
		raise "Installing went wrong"

	try:
		cmd = "\"%s\"" % getPath()
		Popen(cmd)
		print "Seafile should be started now"
	except:
		print "Warning: Could not find the installed path, please start seafile manually."
	return addr

if __name__=="__main__":
	if not "Windows" in platform.platform():
		raise "The autoupdate only works on windows"

	last_updated, interval_in_days, installed_addr = loadConfig()
	if not confExisted: # Updated directly first time
		interval_in_days = 0

	while True:
		passedtime =  timeSinceLastCheck(last_updated) if last_updated else 0
		time.sleep(max(interval_in_days*24*3600-passedtime,0))

		try:
			installed_addr = update(url,installed_addr)
		except Exception, e:
			print e

		last_updated, interval_in_days, _ = loadConfig()
		saveConfig(interval_in_days,installed_addr)
