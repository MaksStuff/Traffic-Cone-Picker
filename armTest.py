from machine import Pin, PWM
import time

# Defines the servo control pins on the esp 32 
servo_pins = [15, 2, 4, 19] #Servos 1,2,3 and 6 in that order
servos = [PWM(Pin(pin), freq=50) for pin in servo_pins]  # 50Hz PWM

# Servo angle range (adjust if needed)
MIN_DUTY = 26   # 0°
MAX_DUTY = 128  # 180°

# Function to set servo angle **slowly**
def gradual_move(servo, start_angle, end_angle, step=1, delay=0.05):
    if start_angle > end_angle:
        step = -step  # Reverse step for decreasing movement

    for angle in range(start_angle, end_angle + step, step):
        duty = int(((angle / 180) * (MAX_DUTY - MIN_DUTY)) + MIN_DUTY)
        servo.duty(duty)
        print(f"Moving to {angle}° (Duty: {duty})")
        time.sleep(delay)  # Small delay for smooth movement

# **Set arm to upright position and hold**
print("\n⚙️ Setting arm to upright position...")

# **Adjust these angles based on real-world positioning**
upright_positions = [90, 45, 90, 180]  

for i, servo in enumerate(servos):
    gradual_move(servo, 90, upright_positions[i], step=2, delay=0.02)  # Slow setup

print("\n✅ Arm is now holding upright!")

# **Test each servo one at a time**
try:
    for i, servo in enumerate(servos):
        print(f"\n➡️ Testing Servo {i+1} on GPIO {servo_pins[i]}")

        gradual_move(servo, upright_positions[i], upright_positions[i] + 30)  # Small move
        time.sleep(2)  
        gradual_move(servo, upright_positions[i] + 30, upright_positions[i] - 30)  # Opposite move
        time.sleep(2)
        gradual_move(servo, upright_positions[i] - 30, upright_positions[i])  # Return to start
        time.sleep(2)

        print(f"✅ Servo {i+1} test complete!\n")

    print("\n🏗️ Arm returned to upright position and will HOLD.")

except KeyboardInterrupt:
    print("\nTest interrupted. Servos holding position.")
