#from RpiMotorLib import RpiMotorLib
#import RPi.GPIO as GPIO
import schedule
from time import sleep, time
from pyephem_sunpath.sunpath import sunpos
from datetime import datetime, date
from geopy.geocoders import Nominatim
import csv
from bs4 import BeautifulSoup
import requests
from tkinter import *
import tkinter.messagebox
  

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

#getting lon/lat 
geolocator = Nominatim(user_agent="Solar Tracker")
address = input("Type the Nearest Address to Panel:")
cityLst = address.split(",")
city = (cityLst[1])

def weather(city):
    city=city.replace(" ","+")
    res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')  
    location1 = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()  
    global info     
    info = soup.select('#wob_dc')[0].getText().strip() 
    weather = soup.select('#wob_tm')[0].getText().strip()
    print(location1)
    print(time)
    print(info)
    print(weather +"°C") 


city = city+ "weather"
weather(city)

if info == "Cloudy":
    tkinter.messagebox.showinfo("","Weather is cloudly, enabling sensors.")
    #USE SENSORSSSSSSSSSSSSSS ADD SENSORSSSSSSSSSSSSSSSSSSSSSSS



elif info == "Clear":
    tkinter.messagebox.showinfo("","Weather is clear, enabling sun calculating.")




location = geolocator.geocode(address)
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
