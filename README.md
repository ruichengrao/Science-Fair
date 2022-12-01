# Science Fair 2022-2023 

### Motor_Controller.py
  - Controls the 28BYJ stepper motor with the calculation of the azimuth tracking the sun
<img src="https://i5.walmartimages.com/asr/838c6723-db4a-4633-a21f-e78275c34adc.5a119ee038bbda92210043dafdafbdc1.jpeg" width=25% height=25%>

```
def runner():
   # Calculating step count
    step_count = difference / 5.625
    global round_step
    round_step = round(step_count, 0)
    print(round_step)
#calls the function
runner()

def motorCon():
    GpioPins = [18, 23, 24, 25]
    mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
    mymotortest.motor_run(GpioPins, .01, round_step, False, True, "half", .05)

motorCon()

schedule.every(5).minutes.do(motorCon)
```
 
 

### Solar_Calc.py
 - Calculates the sun azimuth & altitude angle through pyephem_sunpath algorithm. 
<img src="https://www.photopills.com/sites/default/files/tutorials/2014/2-azimuth-elevation.jpg" width=25% height=25%>

 
``` 
    from pyephem_sunpath.sunpath import sunpos
#getting azimuth
    tz = -4
    global rounded_alt
    global rounded_azm
    alt, azm = sunpos(exact_date, lat, lon, tz, dst=False)
    rounded_alt = round(alt,5)
    rounded_azm = round(azm,5)
```
### Voltage Sensor/Detector.py
  - Calculate the amout of volts that is collected from the solar panel 
  
      #### [Steps For Volt Sensor Setup](https://kookye.com/2017/06/01/design-a-voltmeter-with-the-raspberry-pi-board-and-voltage-sensor/)
      
  
      <img src="http://osoyoo.com/wp-content/uploads/2017/04/voltage_bb.jpg" width=40% height=40%>
  
   
 ``` 
 def main():
        init()
        while True:
               #reads the volts
                ad_value = readadc(AO_pin, SPICLK, SPIMOSI, SPIMISO, SPICS)
                global voltage
                voltage = ad_value*(3.3/1024)*5
                global volts
               #gets the volts and turn it into a string in order to log it into a csv file
                volts = [str(voltage)]
               #open csv file
                with open(filename, 'a', newline="\n") as file:
                        csvwriter = csv.writer(file)
                       #skips header line after the first run
                        if a:
                         csvwriter.writerow(header)
                         a = False
                         csvwriter.writerow(volts)
                                
                GPIO.cleanup() 
          

schedule.every(5).minutes.do(main)
```

 
 
  
  



