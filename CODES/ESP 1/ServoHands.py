import asyncio
from machine import Pin, PWM
import time

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

async def main():
    await asyncio.gather(move_servo1(), move_servo2())

asyncio.run(main())
