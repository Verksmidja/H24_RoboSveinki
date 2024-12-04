import network
import time
import uasyncio as asyncio
import json
from umqtt.simple import MQTTClient
import ubinascii, machine 
from Ljos import ljos, get_leds
from Skynjari import sensor_loop


WIFI_SSID = 'TskoliVESM'
WIFI_PASSWORD = 'Fallegurhestur'

MQTT_BROKER = '10.201.48.99' 
MQTT_PORT = 1883
MQTT_TOPIC = 'esp32/sensor'

MAC = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
MQTT_CLIENT_ID = f'esp32-sender-{MAC}'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            print('.', end='')
            time.sleep(0.5)
    print('\nWi-Fi connected:', wlan.ifconfig())

def mqtt_connect(retries=5, delay=2):
    for attempt in range(retries):
        try:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
            client.connect()
            print('Connected to MQTT Broker:', MQTT_BROKER)
            return client
        except Exception as e:
            print(f'Connection attempt {attempt + 1} failed:', e)
            time.sleep(delay)
    print('Failed to connect to MQTT Broker after multiple attempts.')
    return None

async def control_and_publish(queue, mqtt_client, ljos_task):
    while True:
        if queue:
            distance, state = queue.pop(0)

            if state and ljos_task[0] is None:
                print("Starting Ljos...")
                print(get_leds())
                ljos_task[0] = asyncio.create_task(ljos())
            elif not state and ljos_task[0]:
                print("Stopping Ljos...")
                ljos_task[0].cancel()
                try:
                    await ljos_task[0]
                except asyncio.CancelledError:
                    pass
                ljos_task[0] = None

            payload = json.dumps({"state": state}).encode('utf-8') 
            try:
                mqtt_client.publish(MQTT_TOPIC, payload)
                print("Published JSON:", payload.decode('utf-8')) 
            except Exception as e:
                print('Failed to publish MQTT message:', e)
                print('Attempting to reconnect to MQTT Broker...')
                mqtt_client = mqtt_connect()
                if not mqtt_client:
                    print('Reconnection failed. Retrying in 5 seconds...')
                    await asyncio.sleep(5)
                else:
                    print('Reconnected to MQTT Broker.')

        await asyncio.sleep(0.1)

async def main():
    connect_wifi()

    mqtt_client = mqtt_connect()
    if not mqtt_client:
        print('Exiting due to MQTT connection failure.')
        return

    queue = []
    ljos_task = [None]

    skynjari_task = asyncio.create_task(sensor_loop(queue))

    control_publish_task = asyncio.create_task(control_and_publish(queue, mqtt_client, ljos_task))

    try:
        await asyncio.gather(skynjari_task, control_publish_task)
    except asyncio.CancelledError:
        print("Program interrupted.")
        if ljos_task[0]:
            ljos_task[0].cancel()
            await ljos_task[0]
        skynjari_task.cancel()
        control_publish_task.cancel()
        await asyncio.gather(skynjari_task, control_publish_task, return_exceptions=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program stopped.")
