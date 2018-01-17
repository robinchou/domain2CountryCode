#!/usr/bin/python

import RegistrationDBLoader
import CountryCodeDBLoader
import ClientDBLoader
import CountryConverter
import re


results = RegistrationDBLoader.loadB2UrlFromDB()

for row in results:
	b2Url,clientId = row
	countryCode = CountryConverter.convertFromUrl(b2Url)

	# break down if exceed max attempts for freegeoip API
	if countryCode == "ERROR_FREEGEOIP_FORBBIDEN":
		print "Exceed max attempts for freegeoip API, break down and please try again one hour later."
		break

	# convert alpha2 code to alpha3 code unless the code is started with error 
	if re.match("ERROR_*",countryCode) is None:
		countryCode = CountryCodeDBLoader.loadAlpha3Code(countryCode)
	
	# update verified country code to `client`
	ClientDBLoader.updateVerifiedCountryCode(clientId, countryCode)