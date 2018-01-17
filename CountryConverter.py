#!/usr/bin/python

from urlparse import urlparse
import urllib
import urllib2
import json


def convertFromUrl(httpUrl):
	parseResult = urlparse(httpUrl)
	IPOrHostname = parseResult.hostname
	if IPOrHostname is None:
		return "ERROR_NONE_HOST"
	else:
		return convertFromIPOrHostname(parseResult.hostname)


def convertFromIPOrHostname(IPOrHostname):
	url = "http://freegeoip.net/json/" + IPOrHostname
	try:
		response = urllib2.urlopen(url)
		jsonData = json.loads(response.read())
		return jsonData['country_code']
	except urllib2.HTTPError as e:
		if e.code == 404:
			print "Error: target not found from freegeoip: %s" % IPOrHostname
			return "ERROR_FREEGEOIP_NOT_FOUND"
		elif e.code == 403:
			return "ERROR_FREEGEOIP_FORBBIDEN"
		else:
			return "ERROR_FREEGEOIP_UNKOWN"