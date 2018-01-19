#!/usr/bin/python

import MySQLdb

def loadAlpha3Code(alpha2Code):

	# Open database connection
	db = MySQLdb.connect("localhost","root","","mlcs" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	sql = "select alpha3_code from country_code where alpha2_code='{}'".format(alpha2Code)
	try:
		# Execute the SQL command
		cursor.execute(sql)
		if cursor.rowcount == 0:
			print "Error: alpha 3 code not found for %s" % alpha2Code
			result = "ERROR_COUNTRY_CODE_NOT_FOUND"
		else:
			result = cursor.fetchone()[0]
	except:
		print "Failed to execute sql:\n %s" % (sql)
		raise
	finally:
		# disconnect from server
		db.close()

	return result