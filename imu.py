

import accelerom
import gyro2
import pressure_sensor
import gpsdata
import magnet


#print(accelerom.address)
#print(pressure_sensor.address)

accelerom.configure()
gyro2.configure()
magnet.configure()
cal_data=pressure_sensor.calibration()
#no GPS config

def read_all():
    (temperature, pressure, altitude) = pressure_sensor.read(cal_data)
    (accel_x, accel_y, accel_z) = accelerom.read()
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z) = gyro2.read()
    (x_out,y_out,z_out)=magnet.read()
    (latitude, latNS, longitude, lonEW, status, nsatellites, altitude, grspeed) = gpsdata.read()
    print(latitude, latNS, longitude, lonEW, status, nsatellites, altitude)
    print(temperature, pressure, altitude)
    print(accel_x, accel_y, accel_z)
    print(x_out,y_out,z_out)
    print(gyro_scaled_x, gyro_scaled_y, gyro_scaled_z)
