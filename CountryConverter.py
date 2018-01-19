#!/usr/bin/python

from urlparse import urlparse
import urllib2
import socket
import json


def convertFromUrl(httpUrl):
	parseResult = urlparse(httpUrl)
	IPOrHostname = parseResult.hostname
	if IPOrHostname is None:
		print "Error: cannot acqure IP or hostname from host url: %s" % httpUrl
		return "ERROR_NONE_HOST"
	else:
		return convertFromIPOrHostname(parseResult.hostname)


def convertFromIPOrHostname(IPOrHostname):
	url = "http://freegeoip.net/json/" + IPOrHostname
	try:
		print url
		response = urllib2.urlopen(url, timeout = 10)
		responseData = response.read()
		countryCode = json.loads(responseData)['country_code']
		if (countryCode is None or countryCode == ''):
			return "ERROR_FREEGEOIP_NOT_FOUND"
		else:
			return countryCode

		print countryCode
	except urllib2.HTTPError as e:
		if e.code == 404:
			print "Error: target not found from freegeoip: %s" % IPOrHostname
			return "ERROR_FREEGEOIP_NOT_FOUND"
		elif e.code == 403:
			print "Error: exceed max numbers of attempt for FREEGEOIP API"
			return "ERROR_FREEGEOIP_FORBBIDEN"
		else:
			print "Error: unknown http error for %s \n" % IPOrHostname
			return "ERROR_FREEGEOIP_UNKOWN_HTTPERROR"
	except socket.timeout as e:
		print "Error: timeout for hostname lookup: %s" % IPOrHostname
		return "ERROR_FREEGEOIP_TIMEOUT"
	except:
		print "Error: unrecognized error for %s \n" % IPOrHostname
		return "ERROR_FREEGEOIP_UNKOWN_ERROR"