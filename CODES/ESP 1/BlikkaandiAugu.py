import uasyncio as asyncio
from machine import Pin, PWM, UART

# Define LED pins for left eye
left_eye_r = PWM(Pin(9))
left_eye_g = PWM(Pin(10))
left_eye_b = PWM(Pin(11))

# Define LED pins for right eye
right_eye_r = PWM(Pin(2))
right_eye_g = PWM(Pin(42))
right_eye_b = PWM(Pin(41))

# Setup PWM frequency for LEDs
left_eye_r.freq(1000)
left_eye_g.freq(1000)
left_eye_b.freq(1000)
right_eye_r.freq(1000)
right_eye_g.freq(1000)
right_eye_b.freq(1000)

# Initialize UART for MP3-TF-18P module
uart = UART(1, baudrate=9600, tx=17, rx=16)

# Define RGB values for blinking
def set_eye_color(r, g, b):
    left_eye_r.duty(r)
    left_eye_g.duty(g)
    left_eye_b.duty(b)
    right_eye_r.duty(r)
    right_eye_g.duty(g)
    right_eye_b.duty(b)

# Function to send command to MP3 module to play the specified MP3
def play_mp3():
    # Command to play the MP3 file from folder 01, track 001.mp3
    uart.write(b'\x7E\xFF\x06\x03\x00\x01\x01\xEF')

# Blinking task
async def blink_eyes():
    while True:
        # Set eyes to a color (e.g., red)
        set_eye_color(512, 0, 0)  # Set red
        await asyncio.sleep(0.5)
        
        # Turn off the LEDs
        set_eye_color(0, 0, 0)  # Turn off
        await asyncio.sleep(0.5)

# Music playback task
async def play_music():
    while True:
        play_mp3()  # Send play command to the MP3 module
        await asyncio.sleep(30)  # Wait for track duration before replaying

# Main async function to run both tasks
async def main():
    # Run both tasks concurrently
    await asyncio.gather(blink_eyes(), play_music())

# Run the main function
asyncio.run(main())
