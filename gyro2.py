import math
import smbus

bus = smbus.SMBus(1)
address=0x69

CTRL_REG1 = 0x20
CTRL_REG2 = 0x21
CTRL_REG3 = 0x22
CTRL_REG4 = 0x23
CTRL_REG5 = 0x24

GYRO_START_BLOCK = 0x28
GYRO_XOUT_H = 0  #0x28
GYRO_XOUT_L = 1  #0x29
GYRO_YOUT_H = 2  #0x2a
GYRO_YOUT_L = 3  #0x2b
GYRO_ZOUT_H = 4  #0x2c
GYRO_ZOUT_L = 5  #0x2d

FS_250 = 250
FS_500 = 500
FS_2000 = 2000

FS_250_SCALE = 8.75 / 1000  # milli degrees per second page 10 of the datasheet
FS_500_SCALE = 17.50 / 1000  # milli degrees per second page 10 of the datasheet
FS_2000_SCALE = 70.00 / 1000  # milli degrees per second page 10 of the datasheet

GYRO_SCALE=FS_250_SCALE

gyro_raw_x = 0
gyro_raw_y = 0
gyro_raw_z = 0

gyro_scaled_x = 0
gyro_scaled_y = 0
gyro_scaled_z = 0

raw_temp = 0
scaled_temp = 0


def twos_complement(high,low):
    val = (high << 8) + low
    if (val >= 0x8000):
        return -((0xffff - val) + 1)
    else:
        return val


def configure():
    # Wake up the deice and get output for each of the three axes,X, Y & Z
    bus.write_byte_data(address, CTRL_REG1, 0b00001111)

    # Select Big endian so we can use existing I2C library and include the scaling
    ctrl_reg4 = 0b01000000      #big endian, 250dps scale
    bus.write_byte_data(address, CTRL_REG4, ctrl_reg4)


def read():

    raw_gyro_data = bus.read_i2c_block_data(address, GYRO_START_BLOCK, 6)

    gyro_raw_x = twos_complement(raw_gyro_data[GYRO_XOUT_H], raw_gyro_data[GYRO_XOUT_L])
    gyro_raw_y = twos_complement(raw_gyro_data[GYRO_XOUT_H], raw_gyro_data[GYRO_XOUT_L])
    gyro_raw_z = twos_complement(raw_gyro_data[GYRO_XOUT_H], raw_gyro_data[GYRO_XOUT_L])

    # We convert these to radians for consistency and so we can easily combine later in the filter
    gyro_scaled_x = math.radians(gyro_raw_x * GYRO_SCALE)
    gyro_scaled_y = math.radians(gyro_raw_y * GYRO_SCALE)
    gyro_scaled_z = math.radians(gyro_raw_z * GYRO_SCALE)
    return (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z)
