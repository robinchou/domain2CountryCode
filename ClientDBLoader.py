#!/usr/bin/python

import MySQLdb

def updateVerifiedCountryCode(clientID, countryCode):

	# Open database connection
	db = MySQLdb.connect("localhost","root","","mlcs" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# TODO need check the country_verified is already updated?
	sql = "update client set country_verified = '%s' where id = %d" % (countryCode, clientID)
	try:
		# Execute the SQL command
		cursor.execute(sql)
		# Commit your changes in the database
		db.commit()
	except:
		# Rollback in case there is any error
		db.rollback()
		print "DBERROR: failed to update countryCode[%s] for clientID[%s]" % (clientID, countryCode)

	# disconnect from server
	db.close()