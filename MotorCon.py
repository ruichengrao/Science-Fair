from RpiMotorLib import RpiMotorLib
import RPi.GPIO as GPIO
import schedule
from time import sleep, time
from pyephem_sunpath.sunpath import sunpos
from datetime import datetime
from geopy.geocoders import Nominatim
from datetime import date
import csv


#getting lon/lat 
geolocator = Nominatim(user_agent="Solar Tracker")
location = geolocator.geocode("201 Walt Banks Rd, Peachtree City, GA 30269")
global lat
lat = location.latitude
global lon
lon = location.longitude

#getting date
exact_date = datetime.now()

#getting azimuth
tz = -4
global rounded_alt
global rounded_azm
alt, azm = sunpos(exact_date, lat, lon, tz, dst=False)
rounded_azm = round(azm,0)

# csv file name
filename = "Solar_Tracking.csv"
#currentRow = 
# initializing the titles and rows list
fields = []
rows = []
 
# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
     
    # extracting field names through first row
    fields = next(csvreader)
 
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
index2 = csvreader.line_num - 2
index1 = csvreader.line_num - 3

 
for row in rows[index1:index2]:
    global GRow
    GRow = row
    # parsing each column of a row

    
def listToString(s):

	# initialize an empty string
	str1 = ""

	# traverse in the string
	for ele in s:
		str1 += ele

	# return string
	return str1


# Driver code

strAzm = listToString(GRow)
floAzm = float(strAzm)
rounded_strAzm = round(floAzm, 0)
difference = int(rounded_azm) - int(rounded_strAzm)
print(difference)

def runner():
    # Calculating step count
    step_count = difference / 5.625
    global round_step
    round_step = round(step_count, 0)
    print(round_step)

runner()

def motorCon():
    GpioPins = [18, 23, 24, 25]
    mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
    mymotortest.motor_run(GpioPins, .01, round_step, False, True, "half", .05)

motorCon()

schedule.every(5).minutes.do(motorCon)
