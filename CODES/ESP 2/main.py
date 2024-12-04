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

class MQTTClientManager:
    def __init__(self, client_id, broker, port, topic, reconnect_delay=5):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.topic = topic
        self.reconnect_delay = reconnect_delay
        self.client = None
        self.connected = False

    def connect(self):
        try:
            self.client = MQTTClient(self.client_id, self.broker, port=self.port)
            self.client.connect()
            self.connected = True
            print('Connected to MQTT Broker:', self.broker)
        except Exception as e:
            print('Failed to connect to MQTT Broker:', e)
            self.connected = False
            self.client = None

    async def ensure_connection(self):
        while True:
            if not self.connected:
                print('Attempting to reconnect to MQTT Broker...')
                self.connect()
                if not self.connected:
                    print(f'Reconnection failed. Retrying in {self.reconnect_delay} seconds...')
                    await asyncio.sleep(self.reconnect_delay)
                else:
                    print('Reconnected to MQTT Broker.')
            await asyncio.sleep(self.reconnect_delay)

    def publish(self, topic, message):
        if self.connected and self.client:
            self.client.publish(topic, message)
        else:
            raise ConnectionError("MQTT client is not connected.")

async def control_and_publish(queue, mqtt_manager, ljos_task):
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
                mqtt_manager.publish(MQTT_TOPIC, payload)
                print("Published JSON:", payload.decode('utf-8'))
            except ConnectionError as ce:
                print('Failed to publish MQTT message:', ce)
                print('Message will be requeued and retrying...')
                queue.insert(0, (distance, state))
            except Exception as e:
                print('Unexpected error during MQTT publish:', e)
                queue.insert(0, (distance, state))

        await asyncio.sleep(0.1)

async def main():
    connect_wifi()

    mqtt_manager = MQTTClientManager(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC)
    mqtt_manager.connect()

    mqtt_reconnect_task = asyncio.create_task(mqtt_manager.ensure_connection())

    queue = []
    ljos_task = [None]

    skynjari_task = asyncio.create_task(sensor_loop(queue))

    control_publish_task = asyncio.create_task(control_and_publish(queue, mqtt_manager, ljos_task))

    try:
        await asyncio.gather(skynjari_task, control_publish_task, mqtt_reconnect_task)
    except asyncio.CancelledError:
        print("Program interrupted.")
        if ljos_task[0]:
            ljos_task[0].cancel()
            try:
                await ljos_task[0]
            except asyncio.CancelledError:
                pass
        skynjari_task.cancel()
        control_publish_task.cancel()
        mqtt_reconnect_task.cancel()
        await asyncio.gather(skynjari_task, control_publish_task, mqtt_reconnect_task, return_exceptions=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram stopped.")
