from machine import Pin, I2C
import time

# ---- I2C Setup ----
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

# Motor driver I2C address (default)
MOTOR_DRIVER_ADDR = 0x10  

# Register addresses for motor speed & direction
MOTOR1_SPEED = 0x00
MOTOR1_DIR = 0x01
MOTOR2_SPEED = 0x02
MOTOR2_DIR = 0x03

def set_motor(motor, speed, direction):
    """Control Motor 1 or 2 with speed (0-255) and direction (0=Reverse, 1=Forward)."""
    if motor == 1:
        i2c.writeto_mem(MOTOR_DRIVER_ADDR, MOTOR1_SPEED, bytes([speed]))
        i2c.writeto_mem(MOTOR_DRIVER_ADDR, MOTOR1_DIR, bytes([direction]))
    elif motor == 2:
        i2c.writeto_mem(MOTOR_DRIVER_ADDR, MOTOR2_SPEED, bytes([speed]))
        i2c.writeto_mem(MOTOR_DRIVER_ADDR, MOTOR2_DIR, bytes([direction]))

# ---- Motor Test Sequence ----
while True:
    print("Moving FORWARD...")
    set_motor(1, 200, 1)  # Motor 1 forward at speed 200
    set_motor(2, 200, 1)  # Motor 2 forward at speed 200
    time.sleep(2)

    print("Stopping...")
    set_motor(1, 0, 1)  # Stop Motor 1
    set_motor(2, 0, 1)  # Stop Motor 2
    time.sleep(1)

    print("Moving BACKWARD...")
    set_motor(1, 200, 0)  # Motor 1 reverse at speed 200
    set_motor(2, 200, 0)  # Motor 2 reverse at speed 200
    time.sleep(2)

    print("Stopping...")
    set_motor(1, 0, 0)  # Stop Motor 1
    set_motor(2, 0, 0)  # Stop Motor 2
    time.sleep(1)
