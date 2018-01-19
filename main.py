#!/usr/bin/python

import RegistrationDBLoader
import CountryCodeDBLoader
import ClientDBLoader
import CountryConverter
import threading
import time
import re

def convertHostnameToCountryCode(clientId,b2Url):	
	countryCode = CountryConverter.convertFromUrl(b2Url)

	# break down if exceed max attempts for freegeoip API
	if countryCode == "ERROR_FREEGEOIP_FORBBIDEN":
		print "Exceed max attempts for freegeoip API, break down and please try again one hour later."
		sys.exit("Exceed max attempts for freegeoip API, break down and please try again one hour later.")

	# convert alpha2 code to alpha3 code unless the code is started with error 
	if re.match("ERROR_*",countryCode) is None:
		countryCode = CountryCodeDBLoader.loadAlpha3Code(countryCode)
	
	# update verified country code to `client`
	ClientDBLoader.updateVerifiedCountryCode(clientId, countryCode)


# init count
count = 0
results = RegistrationDBLoader.loadB2UrlFromDB()
print "%d clients remaining..." % len(results)

try:
	for row in results:
		# create 1000 thread at a time then wait till finished
		if count < 100:
			count += 1
		else:
			# reset count
			count = 0
			time.sleep(10)
			# wait till all threads finished
			activeThreadsCount = threading.activeCount()
			while activeThreadsCount > 1:
				print "%d active threads remaining..." % activeThreadsCount
				time.sleep(10)

		b2Url,clientId = row
		threading.Thread(target=convertHostnameToCountryCode,args=(clientId,b2Url)).start()

except Exception, e:
	print "Error: unable to start thread"
	print e