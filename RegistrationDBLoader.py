#!/usr/bin/python

import MySQLdb

def loadB2UrlFromDB():

	b2UrlWithClientIds = []

	# Open database connection
	db = MySQLdb.connect("localhost","root","","mlcs" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	sql = "select r.* from registration as r left join client as c on r.client_id=c.id where \
		c.country_verified='' limit 10000"
	try:
		# Execute the SQL command
		cursor.execute(sql)
		# Fetch all the rows in a list of lists.
		results = cursor.fetchall()
		for row in results:
	   		b2UrlWithClientIds.append((row[4],row[9]))

	except:
	   print "Error: unable to load B2 url"

	# disconnect from server
	db.close()

	return b2UrlWithClientIds