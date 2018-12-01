import requests
import json
import sys, codecs
import csv
import pandas as pd
import datetime
from time import sleep

def get_Coordinates(address_str, app_id):
	
	
	# 1.1 Setting Opions
	url_option = "&recursive=true&exclude_prefecture=false&exclude_seireishi=false&results=1&output=json&callbac"
	
	
	# 1.2 Create URL
	url_header = "https://map.yahooapis.jp/geocode/V1/geoCoder?"
	request_url = url_header + "appid=" + app_id + "&query=" + address_str + url_option
	
	
	# 1.3 Execute Request
	r = requests.get(request_url)
	res = r.json()
	
	# 2. Get Lat lon Geopoint
	
	for i in res["Feature"]:  #Multi results returned when matching level is low
		
		matching_lv = int(i["Property"]["AddressMatchingLevel"])
		coordinates = i["Geometry"]["Coordinates"].split(",")
		lon = coordinates[0]
		lat = coordinates[1]
		
	coordinates = i["Geometry"]["Coordinates"].split(",")
	
	lon = coordinates[0]
	lat = coordinates[1]
	
	return [matching_lv,lon,lat]
	
	



if __name__ == '__main__':
	
	
	#####################
	#     SETTINGS      #
	#####################
	
	time = datetime.datetime.today().isoformat().replace('.','').replace(':','_')
	
	argvs = sys.argv
	
	col_target_num = int(argvs[1])
	
	in_file = argvs[2]
	
	app_id = argvs[3]
	
	
	
	#####################
	#     EXECUTION     #
	#####################
	
	reader = csv.reader(open( in_file , 'r'))
	
	i = 1
	for row in reader:
		try:
			result = get_Coordinates( row[col_target_num],app_id )
			output = row
			
		except Exception as e:
			
			f_logout = open("./log/" + time + ".log","a")
			err_str = str(e)
			print( "ERROR MESSAGE = " + err_str )
			
			f_logout.writelines("Err row = " + str(i) + "\n")
			f_logout.writelines("Error Message = " + err_str + "\n")
			f_logout.close()
			result = [0, "null","null"]
			output = row + result
		
		print(row + result)
		f_out = open("./output/" + time + ".csv","a")
		writer = csv.writer(f_out,lineterminator='\n')
		writer.writerow(row + result)
		f_out.close()
		
		i += 1
		sleep(1)
	
	