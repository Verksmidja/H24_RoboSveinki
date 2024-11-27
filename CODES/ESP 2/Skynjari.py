from machine import Pin
import time
import uasyncio as asyncio

echo = Pin(15, Pin.IN)
trig = Pin(7, Pin.OUT)

async def measure_distance(echo, trig):
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    while not echo.value():
        pass

    start_time = time.ticks_us()

    while echo.value():
        pass

    end_time = time.ticks_us()

    elapsed_time = time.ticks_diff(end_time, start_time)

    elapsed_time /= 2
    sound_speed = 34000 / 1000000
    distance = elapsed_time * sound_speed

    return int(distance)

async def sensor_loop(queue):
    while True:
        distance = await measure_distance(echo, trig)
        state = distance > 12
        if len(queue) < 10:
            queue.append((distance, state))
        await asyncio.sleep(0.1)
