# A not so simple web screen grabber 
# this one uses the Selenium "chromedriver" 
# It is assuming the chromedriver.exe is in the current directory.
# To make sure you have the correct Chrome Driver, visit here:
# https://sites.google.com/a/chromium.org/chromedriver/downloads 
# 
# Although this says "urls.txt" is your input file, 
# as written, this wants BASE DOMAIN urls ... so the list should look like this:
# 
# mydomain.com
# yourwebsite.info
# badsite.xyz 

from selenium import webdriver
import time
import re
import csv
import requests

# path to input file
ipath = "C://Tools//grabber//urls.txt"
# path to chromedriver
dpath = "C:\\Tools\\grabber\\chromedriver.exe"

# pass in list of keys to be searched for
# returns list of hits 
def filter(keys):
	uFile = open(ipath,"r")
	l = uFile.readlines()
	uFile.close()
	trash = []
	for i in l:
		# i came up with this at 2 am dont ask how it works idk
		res = [k for k in keys if (k in i)]
		if bool(res) == False:
			trash.append(i)

	for i in trash:
		l.remove(i)
	return l


# grab only connected to Facebook.com
# can refine to further connection but will lose some types of links
def scrapeF(iList):
	for domain in iList:
		print(int((iList.index(domain)/len(iList)))*100,'%')
		print(domain)
		try:
			browser = webdriver.Chrome(executable_path = dpath)
			browser.get("http://"+domain.strip())
			html = browser.page_source
			time.sleep(1)
			if "buy this domain" in html or "?source=parked" in html:
				continue
			if "parking" in html or "Parking" in html:
				continue
			if "http://courtesy.register.it/" in html:
				continue
			if "this domain is for sale" in html or "This domain is for sale" in html:
				continue
			if "this domain is not linked" in html:
				continue
			elif "facebook.com" in html:
				sheet = open("C://Tools//grabber//out.csv","a")
				sheet.write(domain)
				sheet.close()
				browser.save_screenshot('C:\\tools\\Grabber\\output\\' + str(domain.strip()) + '.png')
				browser.get_screenshot_as_file('C:\\tools\\grabber\\output\\' + str(domain.strip()) + '.png')
				browser.quit()
			else:
				continue
		except:
			print (str(domain) + "Error!")

# grab all regardless of connection
def scrapeAll(iList):
	# REGEX pattern to match btc addresses (not fullproof)
	pattern = '([13]|bc1)[A-HJ-NP-Za-km-z1-9]{27,34}'
	# loop through all domains
	for domain in iList:
		print(domain)
		try:
			browser = webdriver.Chrome(executable_path = dpath)
			browser.get("http://"+domain.strip())
			# wait a bit so the website can load otherwise source wont fully load
			time.sleep(2)
			# better script to grab source
			html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
			# parked handling
			if "parking" in html or "Parking" in html:
				continue
			if "http://courtesy.register.it/" in html:
				continue
			if "this domain is for sale" in html or "This domain is for sale" in html:
				continue
			if "this domain is not linked" in html:
				continue
			#this splits the html and searches it for BTC addresses	
			# need to add api function calls	
			a = html.split("\n")
			for i in a:
				m = re.search(pattern,i)
				if m:
					# wait 10 seconds between api calls otherwise get banned lmao
					time.sleep(10)
					add = addressGrab(m.group(0))
					if bool(add):
						data = readAddress(add)
					else:
						continue

					with open("C://Tools//grabber//Cout.csv","a",newline = '') as f:
						writer = csv.writer(f)
						writer.writerow([domain,m.group(0),data])
						f.close()
			# write all results to output sheet
			sheet = open("C://Tools//grabber//out.csv","a")
			sheet.write(domain)
			sheet.close()
			browser.save_screenshot('C:\\tools\\Grabber\\output\\' + str(domain.strip()) + '.png')
			browser.get_screenshot_as_file('C:\\tools\\grabber\\output\\' + str(domain.strip()) + '.png')
			browser.quit()
		except:
			print (str(domain) + "Error!")


# grab address balances and txs
# maybe make a loop for this so i can pass in lists of pulled addresses that may 
# make analysis easier
# pass in a bitcoin address it will return a REST object with the API response
# this function allows for much more data gathering then just the total recieved so keep that
# in mind customize the json call to your needs
def addressGrab(add):
	# make request to blockchain.com api for address data
	requesadd = "https://blockchain.info/rawaddr/"
	# add address to the end of request
	req = requesadd + add
	# this should return JSON with all needed data with error handling
	try:
		adr_data = requests.get(req,timeout=5)
		adr_data.raise_for_status()
	except requests.exceptions.HTTPError as errh:
		print(errh)
	except requests.exceptions.ConnectionError as errc:
		print(errc)
	except requests.exceptions.Timeout as errt:
		print(errt)
	except requests.exceptions.RequestException as err:
		print(err)
	return adr_data

# if you want to just grab a boatload of addresses pass them in here and it
# will return a list of REST api response objects make sure to loop through reading these otherwise it wont work
def multGrab(adds):
	obs = []
	for i in adds:
		a = addressGrab(i)
		obs.append(a)
	return obs


def readAddress(data):
	a = data.json()['total_received']
	actual = a/100000000
	actual = actual*32000
	return actual

