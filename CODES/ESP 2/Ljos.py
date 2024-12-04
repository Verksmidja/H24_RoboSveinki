import machine
import neopixel
import uasyncio as asyncio

NUM_PIXELS_1 = 10
NUM_PIXELS_2 = 10
PIN_1 = 5
PIN_2 = 6

np1 = neopixel.NeoPixel(machine.Pin(PIN_1), NUM_PIXELS_1)
np2 = neopixel.NeoPixel(machine.Pin(PIN_2), NUM_PIXELS_2)

led1 = [0,0,0]
led2 = [0,0,0]

def get_leds():
    return led1, led2

def clear_strip(np):
    for i in range(len(np)):
        np[i] = (0, 0, 0)
    np.write()

async def red_green_switch(np):
    state = True
    try:
        while True:
            if state:
                for i in range(len(np)):
                    if i % 2 == 0:
                        led2 = [255, 0, 0]
                        np[i] = (255, 0, 0)
                    else:
                        led1 = [0, 255, 0]
                        np[i] = (0, 255, 0)
            else:
                for i in range(len(np)):
                    if i % 2 == 0 :
                        led2 = [0, 255, 0]
                        np[i] = (0, 255, 0)
                    else:
                        led1 = [255, 0, 0]
                        np[i] = (255, 0, 0)
            np.write()
            state = not state
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        clear_strip(np)
        raise 

async def ljos():
    task1 = asyncio.create_task(red_green_switch(np1))
    task2 = asyncio.create_task(red_green_switch(np2))
    try:
        await asyncio.gather(task1, task2)
    except asyncio.CancelledError:
        task1.cancel()
        task2.cancel()
        await asyncio.gather(task1, task2, return_exceptions=True)
        raise
