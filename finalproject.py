#!/usr/bin/python3
import sqlite3
import pandas
import sys
import os
import datetime
import time
import argparse

def get_browser_path(browser):
    #get the home directory operating system you are working on
    os_env_dir = os.path.expanduser('~')
    req_path = ""
    #print(os_env_dir)

    #check if the browser is firefox
    if browser == 'firefox':
        #set the path according to the operating system
        if sys.platform.startswith('win') == True:
            req_path = os_env_dir + "/AppData/Roaming/Mozilla/Firefox/Profiles/"
        elif sys.platform.startswith('linux') == True:
            req_path = os_env_dir + "/.mozilla/firefox/"
    return req_path
# This defines a function that clears the history based off of a defined
# time frame
def clear_history_by_time(starting_time , ending_time , ff_cursor):
	history_time = datetime.datetime.utcnow() - datetime.timedelta(hours = starting_time)
	final_starting_time = time.mktime(history_time.timetuple())
	final_starting_time = int(final_starting_time*1000000)
	history_time = datetime.datetime.utcnow() - datetime.timedelta(hours = ending_time)
	final_ending_time = time.mktime(history_time.timetuple())
	final_ending_time = int(final_ending_time*1000000)

	count = 1
	print("The following history items matched your query: ")
	print("")
	for row in ff_cursor.execute("SELECT url FROM moz_places where last_visit_date > ? and last_visit_date < ?" , (final_starting_time , final_ending_time ,  )):
		print('%s. %s' %(count , row[0]))
		count+=1
	else:
		print("Deleting History................")
		ff_cursor.execute("DELETE FROM moz_places where last_visit_date > ? and last_visit_date < ?" , (final_starting_time , final_ending_time , ))

if __name__ == "__main__":
	#parsing
	parser = argparse.ArgumentParser(description="Manipulate your browsing history using keywords or timespan")
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("-d" , "--delete" , action="store_true" , help="Deletion mode: Actual deletion of history takes place.")
#	mode.add_argument("-t" , "--test" , action="store_true" , help="Testing mode: selected history is just displayed (no actual deletion)")
	deleteBy = parser.add_mutually_exclusive_group()
	deleteBy.add_argument("-kw" , "--keywords" , action="store_true" , help="Deletion/Selection by keywords")
#	deleteBy.add_argument("-ts" , "--timespan" , action="store_true" , help="Deletion/Selection by timespan")
	args = parser.parse_args()

	#printing the choices
	ch = 1
    # A lot of code existed here that prompted the user for input
    # We were able to get rid of the irrelevant code and slim down the
    # application so that it performed the way that we wanted it do.
	firefox_path = get_browser_path('firefox')
	profiles = [i for i in os.listdir(firefox_path) if i.endswith('.default')]
	sqlite_path = firefox_path+ profiles[0]+'/places.sqlite'
	if os.path.exists(sqlite_path):
		firefox_connection = sqlite3.connect(sqlite_path)
		ff_cursor = firefox_connection.cursor()
	        #print("connection successful")
		#clearing history in firefox
		con = sqlite3.connect(sqlite_path)
		table = pandas.read_sql('select * from moz_places', con)
		table.to_csv('moz_hist.csv')

		try:
			if ch == 1:
				starting_time = 500
				ending_time = 1

				clear_history_by_time(starting_time , ending_time , ff_cursor)
				print("Done.........")
			firefox_connection.commit()
			ff_cursor.close()
		except Exception as err:
			print(err)
	else:
		print("Firefox browser not found")
