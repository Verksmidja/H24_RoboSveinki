from Ljos import ljos
from Skynjari import sensor_loop
import uasyncio as asyncio

async def main():
    queue = []
    ljos_task = None

    async def control_ljos():
        nonlocal ljos_task
        while True:
            if queue:
                _, state = queue.pop(0)
                if state and ljos_task is None:
                    print("Starting Ljos...")
                    ljos_task = asyncio.create_task(ljos())
                elif not state and ljos_task:
                    print("Stopping Ljos...")
                    ljos_task.cancel()
                    try:
                        await ljos_task
                    except asyncio.CancelledError:
                        pass
                    ljos_task = None
            await asyncio.sleep(0.1)
            
    skynjari_task = asyncio.create_task(sensor_loop(queue))
    ljos_control_task = asyncio.create_task(control_ljos())

    try:
        await asyncio.gather(skynjari_task, ljos_control_task)
    except asyncio.CancelledError:
        print("Program interrupted.")
        if ljos_task:
            ljos_task.cancel()
            await ljos_task
        skynjari_task.cancel()
        await skynjari_task

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped.")

