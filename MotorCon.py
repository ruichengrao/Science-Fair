#from RpiMotorLib import RpiMotorLib
#import RPi.GPIO as GPIO
import schedule
from time import sleep, time
from pyephem_sunpath.sunpath import sunpos
from datetime import datetime, date
from geopy.geocoders import Nominatim
import csv
from tkinter import *
import tkinter.messagebox
from Py_Weather import get_weather


# Import Module
from tkinter import *
 
# create root window
root = Tk()
 
# root window title and dimension
root.title("MSH Solar Interface")
# Set geometry(widthxheight)
root.geometry('450x250')

# adding a label to the root window
lb0 = Label(root, text = "Weather Determined Solar Tracking")
lb0.grid()
lbS = Label(root, text = "")
lbS.grid()

lbl = Label(root, text = "Nearest Address")
lbl.grid()
lb2 = Label(root, text = "City*")
lb2.grid()
lb3 = Label(root, text = "State/Proviences/Regions*")
lb3.grid()
lb4 = Label(root, text = "Click Finish Calibration when all enter are clicked!")
lb4.grid()
# adding Entry Field
txt = Entry(root, width=10)
txt.grid(column =1, row =2)
txt2 = Entry(root, width=10)
txt2.grid(column =1, row =3)
txt3 = Entry(root, width=10)
txt3.grid(column =1, row =4)
 

def Close():
    root.destroy()

# function to display user text when
# button is clicked
def clicked():
    global nearestAddress, City, State
    nearestAddress = txt.get()
    City = txt2.get()
    State = txt3.get()

 

exit_button = Button(root, text="Finish Calibration", command=Close)
exit_button.grid(column=3, row=5) 
# button widget with red color text inside

btn2 = Button(root, text = "Enter" ,
             fg = "black", command=clicked)
btn3 = Button(root, text = "Enter" ,
             fg = "black", command=clicked)
btn4 = Button(root, text = "Enter" ,
             fg = "black", command=clicked, )

# Set Button Grid
btn2.grid(column=3, row=2)
btn3.grid(column=3, row=3)
btn4.grid(column=3, row=4)



# Execute Tkinter
root.mainloop()
#getting the weather to determine to use sensors or algoritm

weather = get_weather(City)


if weather == "cloudy":
    print("Enabling Sensors")
elif weather == "sunny":
     print("Enabling Algroithem")
     pass

#getting lon/lat 
geolocator = Nominatim(user_agent="Solar Tracker")

location = geolocator.geocode(nearestAddress)
global lat
lat = location.latitude
global lon
lon = location.longitude

print((lon,lat))

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
