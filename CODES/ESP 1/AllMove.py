from machine import Pin, PWM, ADC
import asyncio
from Lib.dfplayer import DFPlayer

# Shared PWM frequency
FREQ = 1000  # 1 kHz frequency

# RGB LEDs setup (sharing channels for each color)
pwm_red = PWM(Pin(9), freq=FREQ)  # Shared channel for red
pwm_green = PWM(Pin(10), freq=FREQ)  # Shared channel for green
pwm_blue = PWM(Pin(11), freq=FREQ)  # Shared channel for blue

# Assign pins for second LED (reusing PWM channels)
red2 = Pin(2)  # Pin to control LED 2 red
green2 = Pin(42)  # Pin to control LED 2 green
blue2 = Pin(41)  # Pin to control LED 2 blue

# Function to set color for both RGB LEDs
def set_color(r, g, b):
    pwm_red.duty_u16(int(r * 65535 / 255))
    pwm_green.duty_u16(int(g * 65535 / 255))
    pwm_blue.duty_u16(int(b * 65535 / 255))

    # Second LED mirrors the same color
    red2.value(1 if r > 0 else 0)
    green2.value(1 if g > 0 else 0)
    blue2.value(1 if b > 0 else 0)

# DFPlayer and jaw setup
df = DFPlayer(2)
df.init(tx=17, rx=16)

jaw_pin = 36
jaw_servo = PWM(Pin(jaw_pin), freq=50)

audio_intensity_pin = ADC(Pin(14))
audio_intensity_pin.atten(ADC.ATTN_11DB)  # 3.3V range

min_jaw_angle = 0  # Fully closed
max_jaw_angle = 44  # Fully open
min_adc_value = 700
max_adc_value = 2000
noise_threshold = 600

def adjust_adc_range(adc_value):
    global min_adc_value, max_adc_value
    if adc_value < min_adc_value and adc_value > noise_threshold:
        min_adc_value = adc_value
    if adc_value > max_adc_value:
        max_adc_value = adc_value

def map_adc_to_jaw_angle(adc_value):
    if adc_value < noise_threshold:
        return min_jaw_angle
    if max_adc_value == min_adc_value:
        return min_jaw_angle
    scaled_adc_value = (adc_value - min_adc_value)
    scaled_adc_value = max(0, min(scaled_adc_value, max_adc_value - min_adc_value))
    return min_jaw_angle + (scaled_adc_value / (max_adc_value - min_adc_value)) * (max_jaw_angle - min_jaw_angle)

def set_jaw_angle(angle):
    duty = int(40 + (angle / 180) * 115)
    jaw_servo.duty(duty)

# Hand movement setup
servo1 = PWM(Pin(12), freq=50)
servo2 = PWM(Pin(13), freq=50)

def set_angle1(angle):
    duty = int((angle / 180) * 102 + 26)
    servo1.duty(duty)

def set_angle2(angle):
    duty = int((angle / 180) * 102 + 26)
    servo2.duty(duty)

async def move_servo1():
    while True:
        for angle in range(35, 80, 3):
            set_angle1(angle)
            await asyncio.sleep(0.05)
        for angle in range(80, 35, -3):
            set_angle1(angle)
            await asyncio.sleep(0.05)

async def move_servo2():
    while True:
        for angle in range(150, 181, 3):
            set_angle2(angle)
            await asyncio.sleep(0.05)
        for angle in range(180, 149, -3):
            set_angle2(angle)
            await asyncio.sleep(0.05)

# RGB LED task
async def control_leds():
    while True:
        set_color(255, 255, 255)  # White
        await asyncio.sleep(0.5)
        set_color(0, 255, 0)  # Green
        await asyncio.sleep(0.5)

# Jaw movement task
async def control_jaw():
    await df.wait_available()
    await df.volume(30)
    await df.play(1, 1)

    while True:
        raw_adc = audio_intensity_pin.read()
        adjust_adc_range(raw_adc)
        jaw_angle = map_adc_to_jaw_angle(raw_adc)
        print(f"Raw ADC: {raw_adc}, Jaw Angle: {jaw_angle}")
        set_jaw_angle(jaw_angle)
        await asyncio.sleep(0.03)

# Servo movement task (from the first code)
async def control_servos():
    servo_pin = PWM(Pin(37), freq=50)

    # Function to set the servo angle
    def set_servo_angle(angle):
        min_duty = 1300  # Corresponds to 0° (adjust if needed)
        max_duty = 7800  # Corresponds to 180° (adjust if needed)
        duty = int(min_duty + (max_duty - min_duty) * (angle / 180))
        servo_pin.duty_u16(duty)

    while True:
        # Move servo from 180° to 60°
        for angle in range(180, 59, -5):  # Step of -5 degrees
            set_servo_angle(angle)
            await asyncio.sleep(0.1)
        # Move servo from 60° to 180°
        for angle in range(60, 181, 5):  # Step of 5 degrees
            set_servo_angle(angle)
            await asyncio.sleep(0.1)

# Main function
async def main():
    await asyncio.gather(
        control_leds(),
        control_jaw(),
        move_servo1(),
        move_servo2(),
        control_servos()
    )

asyncio.run(main())

