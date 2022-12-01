# Science Fair 2022-2023 

- Motor_Controller
  - Controls the 28BYJ stepper motor with the calculation of the azimuth tracking the sun
 
![image](https://user-images.githubusercontent.com/106492499/205093171-ddad79e5-9ba0-40dd-9b64-3a772337b538.png)

- Solar_Calc
  - Calculates the sun azimuth & altitude angle through pyephem_sunpath algorithm. 
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
- Voltage Sensor/Detector
  - Calculate the amout of volts that is collected from the solar panel
  
  


<!---
ruichengrao/ruichengrao is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
