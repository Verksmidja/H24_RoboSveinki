import asyncio
from machine import Pin, PWM
import time

# Initialize PWM on GPIO pins
servo1 = PWM(Pin(12), freq=50)  # Servo 1 connected to port 12
servo2 = PWM(Pin(13), freq=50)  # Servo 2 connected to port 13

def set_angle1(angle):
    duty = int((angle / 180) * 102 + 26)  # Adjust for your servo if needed
    servo1.duty(duty)

def set_angle2(angle):
    duty = int((angle / 180) * 102 + 26)  # Adjust for your servo if needed
    servo2.duty(duty)

async def move_servo1():
    while True:
        for angle in range(35, 80, 3):  # Move up, skip by 3
            set_angle1(angle)
            await asyncio.sleep(0.05)  # Faster speed
        for angle in range(80, 35, -3):  # Move down, skip by 3
            set_angle1(angle)
            await asyncio.sleep(0.05)

async def move_servo2():
    while True:
        for angle in range(150, 181, 3):  # Move from 150° to 180°
            set_angle2(angle)
            await asyncio.sleep(0.05)  # Adjust delay for speed
        for angle in range(180, 149, -3):  # Move from 180° back to 150°
            set_angle2(angle)
            await asyncio.sleep(0.05)  # Adjust delay for speed

async def main():
    # Run both servo movements concurrently
    await asyncio.gather(move_servo1(), move_servo2())

# Run the asyncio event loop
asyncio.run(main())

