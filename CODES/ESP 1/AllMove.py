import network
import time
import json
from umqtt.simple import MQTTClient
import ubinascii, machine
import uasyncio as asyncio
from machine import Pin, PWM, ADC
from Lib.dfplayer import DFPlayer

# WiFi and MQTT Configurations
WIFI_SSID = 'TskoliVESM'
WIFI_PASSWORD = 'Fallegurhestur'

MQTT_BROKER = '10.201.48.99'
MQTT_PORT = 1883
MQTT_TOPIC = 'esp32/sensor/robot'
MQTT_CLIENT_ID = f'esp32-receiver-{ubinascii.hexlify(machine.unique_id()).decode("utf-8")}'

# Shared state for MQTT
state = False
mqtt_client = None

# RGB LEDs setup (sharing channels for each color)
FREQ = 1000  # 1 kHz frequency
pwm_red = PWM(Pin(9), freq=FREQ)  # Shared channel for red
pwm_green = PWM(Pin(10), freq=FREQ)  # Shared channel for green
pwm_blue = PWM(Pin(11), freq=FREQ)  # Shared channel for blue

# Assign pins for second LED (reusing PWM channels)
red2 = Pin(2)  # Pin to control LED 2 red
green2 = Pin(42)  # Pin to control LED 2 green
blue2 = Pin(41)  # Pin to control LED 2 blue

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

# Hand movement setup
servo1 = PWM(Pin(12), freq=50)
servo2 = PWM(Pin(13), freq=50)

# Servo on pin 37 setup for continuous movement
servo_pin = PWM(Pin(37), freq=50)

# Servo on pin 35 setup for specific movement range
servo_pin_35 = PWM(Pin(35), freq=50)

# Function to set servo angles
def set_angle1(angle):
    duty = int((angle / 180) * 102 + 26)
    servo1.duty(duty)

def set_angle2(angle):
    duty = int((angle / 180) * 102 + 26)
    servo2.duty(duty)

def set_servo_angle(angle):
    # Map the angle to duty cycle (0° to 180°)
    min_duty = 1300  # Corresponds to 0° (adjust if needed)
    max_duty = 7800  # Corresponds to 180° (adjust if needed)
    duty = int(min_duty + (max_duty - min_duty) * (angle / 180))
    servo_pin.duty_u16(duty)

def set_servo_angle_35(angle):
    # Map the angle to duty cycle (40° to 80°)
    min_duty = 1700  # Corresponds to 40° (adjust if needed)
    max_duty = 3300  # Corresponds to 80° (adjust if needed)
    duty = int(min_duty + (max_duty - min_duty) * ((angle - 40) / 40))
    servo_pin_35.duty_u16(duty)

# Function to adjust ADC range
def adjust_adc_range(adc_value):
    global min_adc_value, max_adc_value
    if adc_value < min_adc_value and adc_value > noise_threshold:
        min_adc_value = adc_value
    if adc_value > max_adc_value:
        max_adc_value = adc_value

# Function to map ADC value to jaw angle
def map_adc_to_jaw_angle(adc_value):
    if adc_value < noise_threshold:
        return min_jaw_angle
    if max_adc_value == min_adc_value:
        return min_jaw_angle
    scaled_adc_value = (adc_value - min_adc_value)
    scaled_adc_value = max(0, min(scaled_adc_value, max_adc_value - min_adc_value))
    return min_jaw_angle + (scaled_adc_value / (max_adc_value - min_adc_value)) * (max_jaw_angle - min_jaw_angle)

# Function to set jaw angle
def set_jaw_angle(angle):
    duty = int(40 + (angle / 180) * 115)
    jaw_servo.duty(duty)

# WiFi Connection
async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            print('.', end='')
            await asyncio.sleep(0.5)
    print('\nWi-Fi connected:', wlan.ifconfig())

# MQTT Callback
def mqtt_callback(topic, msg):
    global state
    try:
        message_str = msg.decode('utf-8')
        print(f"Received raw message: {message_str}")
        payload = json.loads(message_str)
        state = payload.get('state', False)
        print(f"Json delivered, state: {state}")
        if not state:
            # Turn off lights and stop music
            pwm_red.duty_u16(0)
            pwm_green.duty_u16(0)
            pwm_blue.duty_u16(0)
            asyncio.create_task(df.pause())
    except (ValueError, Exception) as e:

        print("Received invalid JSON")
        print(f"Error: {e}")
        print(f"Raw message: {msg}")

# MQTT Connect
async def mqtt_connect():
    global mqtt_client
    for attempt in range(5):
        try:
            mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
            mqtt_client.set_callback(mqtt_callback)
            mqtt_client.connect()
            mqtt_client.subscribe(MQTT_TOPIC)
            print('Connected to MQTT Broker and subscribed to topic:', MQTT_TOPIC)
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} to connect to MQTT broker failed: {e}")
            await asyncio.sleep(2)
    print('Failed to connect to MQTT Broker after multiple attempts.')

# Task Functions
async def control_leds():
    while True:
        if state:
            pwm_red.duty_u16(int(255 * 65535 / 255))
            pwm_green.duty_u16(int(255 * 65535 / 255))
            pwm_blue.duty_u16(int(255 * 65535 / 255))
            await asyncio.sleep(0.5)
            pwm_red.duty_u16(int(0 * 65535 / 255))
            pwm_green.duty_u16(int(255 * 65535 / 255))
            pwm_blue.duty_u16(int(0 * 65535 / 255))
            await asyncio.sleep(0.5)
        else:
            pwm_red.duty_u16(0)
            pwm_green.duty_u16(0)
            pwm_blue.duty_u16(0)
            await asyncio.sleep(0.1)

async def control_jaw():
    await df.wait_available()
    await df.volume(30)

    while True:
        if state:
            await df.resume()
            raw_adc = audio_intensity_pin.read()
            adjust_adc_range(raw_adc)
            jaw_angle = map_adc_to_jaw_angle(raw_adc)
            print(f"Raw ADC: {raw_adc}, Jaw Angle: {jaw_angle}")
            set_jaw_angle(jaw_angle)
        else:
            set_jaw_angle(min_jaw_angle)
            await df.pause()
        await asyncio.sleep(0.03)

async def move_servo1():
    while True:
        if state:
            for angle in range(35, 80, 3):
                set_angle1(angle)
                await asyncio.sleep(0.05)
            for angle in range(80, 35, -3):
                set_angle1(angle)
                await asyncio.sleep(0.05)
        else:
            await asyncio.sleep(0.1)

async def move_servo2():
    while True:
        if state:
            for angle in range(150, 181, 3):
                set_angle2(angle)
                await asyncio.sleep(0.05)
            for angle in range(180, 149, -3):
                set_angle2(angle)
                await asyncio.sleep(0.05)
        else:
            await asyncio.sleep(0.1)

async def move_servo_continuous():
    while True:
        if state:
            # Move servo from 180° to 60°
            for angle in range(180, 59, -5):  # Step of -5 degrees
                set_servo_angle(angle)
                await asyncio.sleep(0.1)
            # Move servo from 60° to 180°
            for angle in range(60, 181, 5):  # Step of 5 degrees
                set_servo_angle(angle)
                await asyncio.sleep(0.1)
        else:
            await asyncio.sleep(0.1)

async def move_servo_35():
    while True:
        if state:
            for angle in range(40, 81, 5):
                set_servo_angle_35(angle)
                await asyncio.sleep(0.1)
            for angle in range(80, 39, -5):
                set_servo_angle_35(angle)
                await asyncio.sleep(0.1)
        else:
            await asyncio.sleep(0.1)

# Main Function
async def main():
    await connect_wifi()
    await mqtt_connect()

    async def control_tasks():
        while True:
            await asyncio.gather(
                control_leds(),
                control_jaw(),
                move_servo1(),
                move_servo2(),
                move_servo_continuous(),
                move_servo_35()
            )

    async def mqtt_loop():
        while True:
            try:
                mqtt_client.check_msg()
            except OSError as e:
                print(f"Connection lost: {e}")
                await mqtt_connect()
            await asyncio.sleep(0.1)

    await asyncio.gather(control_tasks(), mqtt_loop())

# Run Main
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nProgram stopped by user.")

