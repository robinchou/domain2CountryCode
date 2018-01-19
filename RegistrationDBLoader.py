#!/usr/bin/python

import MySQLdb

def loadB2UrlFromDB():

	b2UrlWithClientIds = []

	# Open database connection
	db = MySQLdb.connect("localhost","root","","mlcs" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	sql = "select * from registration where country is null limit 10000"
	try:
		# Execute the SQL command
		cursor.execute(sql)
		# Fetch all the rows in a list of lists.
		results = cursor.fetchall()
		for row in results:
	   		b2UrlWithClientIds.append((row[0],row[4]))

	except:
		print "Error: unable to load B2 url"
		raise

	finally:
		# disconnect from server
		db.close()

	return b2UrlWithClientIds

def updateCountryCode(ID, countryCode):

	# Open database connection
	db = MySQLdb.connect("localhost","root","","mlcs" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# TODO need check the country_verified is already updated?
	sql = "update `registration` set `country` = '%s' where `id` = %d" % (countryCode, ID)
	try:
		# Execute the SQL command
		cursor.execute(sql)
		# Commit your changes in the database
		db.commit()
	except:
		# Rollback in case there is any error
		db.rollback()
		print "DBERROR: failed to update countryCode[%s] for ID[%s]" % (ID, countryCode)
		raise
	finally:
		# disconnect from server
		db.close()
