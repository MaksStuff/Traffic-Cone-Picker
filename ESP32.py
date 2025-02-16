from machine import I2C, Pin
import time
import struct

# I2C Setup
I2C_SCL_PIN = 22  # GPIO 22 for SCL
I2C_SDA_PIN = 21  # GPIO 21 for SDA
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)  # 400 kHz I2C frequency

##------------------------ Use this to reference the tank motors
# Motor driver I2C address
MOTOR_ADDR = 0x34 

# Register addresses
ADC_BAT_ADDR = 0x00  # Battery voltage
MOTOR_TYPE_ADDR = 0x14  # Motor type
MOTOR_ENCODER_POLARITY_ADDR = 0x15  # Encoder polarity
MOTOR_FIXED_PWM_ADDR = 0x1F  # Fixed PWM control (open-loop)
MOTOR_FIXED_SPEED_ADDR = 0x33  # Fixed speed control (closed-loop)
MOTOR_ENCODER_TOTAL_ADDR = 0x3C  # Total encoder pulses

# Motor type values
MOTOR_TYPE_WITHOUT_ENCODER = 0
MOTOR_TYPE_TT = 1
MOTOR_TYPE_N20 = 2
MOTOR_TYPE_JGB37_520_12V_110RPM = 3  
##------------------------
# Motor type and encoder polarity
MotorType = MOTOR_TYPE_JGB37_520_12V_110RPM
MotorEncoderPolarity = 1  # Try flipping polarity for Motor 2 (0 or 1)

# Speed values for fixed speed control
speed1 = [50, 60, 0, 0]  # Motor 1 at 50%, Motor 2 at 60%
speed2 = [-50, -60, 0, 0]  # Motor 1 at -50%, Motor 2 at -60%
speed3 = [0, 0, 0, 0]  # Stop

def motor_init():
    """Initialize the motor driver with the correct motor type and encoder polarity."""
    try:
        i2c.writeto_mem(MOTOR_ADDR, MOTOR_TYPE_ADDR, bytes([MotorType]))  # Set motor type
        time.sleep(0.5)
        i2c.writeto_mem(MOTOR_ADDR, MOTOR_ENCODER_POLARITY_ADDR, bytes([MotorEncoderPolarity]))  # Set encoder polarity
        print("Motor driver initialized successfully.")
    except OSError as e:
        print(f"Failed to initialize motor driver: {e}")

def read_battery_voltage():
    """Read and return the battery voltage in millivolts."""
    try:
        data = i2c.readfrom_mem(MOTOR_ADDR, ADC_BAT_ADDR, 2)
        voltage = data[0] + (data[1] << 8)
        return voltage
    except OSError as e:
        print(f"Failed to read battery voltage: {e}")
        return 0

def read_encoder_values():
    """Read and return the total encoder pulses for all motors."""
    try:
        data = i2c.readfrom_mem(MOTOR_ADDR, MOTOR_ENCODER_TOTAL_ADDR, 16)
        encoder_values = struct.unpack('iiii', data)  # Unpack 4 integers (one for each motor)
        return encoder_values
    except OSError as e:
        print(f"Failed to read encoder values: {e}")
        return [0, 0, 0, 0]

def set_motor_speed(speed):
    """Set the motor speed using fixed speed control."""
    try:
        speed_bytes = bytearray(speed)
        i2c.writeto_mem(MOTOR_ADDR, MOTOR_FIXED_SPEED_ADDR, speed_bytes)
    except OSError as e:
        print(f"Failed to set motor speed: {e}")

def main():
    """Main function to control the motors and read sensor data."""
    motor_init()  # Initialize the motor driver

    while True:
        # Read and print battery voltage
        battery_voltage = read_battery_voltage()
        print(f"Battery Voltage: {battery_voltage} mV")

        # Read and print encoder values
        encoder_values = read_encoder_values()
        print(f"Encoder Values: Motor1 = {encoder_values[0]}, Motor2 = {encoder_values[1]}, Motor3 = {encoder_values[2]}, Motor4 = {encoder_values[3]}")

        # Move forward at adjusted speed (Motor 1 and Motor 2)
        print("Moving FORWARD...")
        set_motor_speed(speed1)
        time.sleep(3)

        # Print encoder values after moving forward
        encoder_values = read_encoder_values()
        print(f"Encoder Values After Forward: Motor1 = {encoder_values[0]}, Motor2 = {encoder_values[1]}")

        # Move reverse at adjusted speed (Motor 1 and Motor 2)
        print("Moving REVERSE...")
        set_motor_speed(speed2)
        time.sleep(3)

        # Print encoder values after moving reverse
        encoder_values = read_encoder_values()
        print(f"Encoder Values After Reverse: Motor1 = {encoder_values[0]}, Motor2 = {encoder_values[1]}")

        # Stop
        print("Stopping...")
        set_motor_speed(speed3)
        time.sleep(2)

# Run the main function
if __name__ == "__main__":
    main()
