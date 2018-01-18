#!/usr/bin/python

import RegistrationDBLoader
import CountryCodeDBLoader
import ClientDBLoader
import CountryConverter
import threading
import time
import re
from multiprocessing.pool import ThreadPool

def convertHostnameToCountryCode(registrationID,b2Url):	
	countryCode = CountryConverter.convertFromUrl(b2Url)

	# break down if exceed max attempts for freegeoip API
	if countryCode == "ERROR_FREEGEOIP_FORBBIDEN":
		print "Exceed max attempts for freegeoip API, break down and please try again one hour later."
	
	else:
		# convert alpha2 code to alpha3 code unless the code is started with error 
		if re.match("ERROR_*",countryCode) is None:
			countryCode = CountryCodeDBLoader.loadAlpha3Code(countryCode)
		
		# update country code to `registration`
		RegistrationDBLoader.updateCountryCode(registrationID, countryCode)


# init count and thread pool
count = 0
threadpool = ThreadPool(100)

results = RegistrationDBLoader.loadB2UrlFromDB()
print "%d registrations remaining..." % len(results)

try:
	for row in results:
		# create 1000 thread at a time then wait till finished
		if count < 100:
			count += 1
		else:
			# reset count
			count = 0
			time.sleep(20)
			# # wait till all threads finished
			# activeThreads = threading.enumerate()
			# print activeThreads
			# activeThreadsCount = threading.activeCount()
			# while activeThreadsCount > 1:
			# 	print "%d active threads remaining..." % activeThreadsCount
			# 	time.sleep(10)

		registrationID,b2Url = row
		threadpool.apply_async(convertHostnameToCountryCode,args=(registrationID,b2Url))

except Exception, e:
	print "Error: unable to start thread"
	print e