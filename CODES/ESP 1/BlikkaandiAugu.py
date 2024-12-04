from machine import Pin, PWM

# Define PWM frequency
FREQ = 1000  # 1 kHz frequency

# RGB LED 1 (Pins 9, 10, 11)
red1 = PWM(Pin(9))
green1 = PWM(Pin(10))
blue1 = PWM(Pin(11))

# RGB LED 2 (Pins 3, 42, 41)
red2 = PWM(Pin(2))
green2 = PWM(Pin(42))
blue2 = PWM(Pin(41))

# Set PWM frequency for all pins
red1.freq(FREQ)
green1.freq(FREQ)
blue1.freq(FREQ)
red2.freq(FREQ)
green2.freq(FREQ)
blue2.freq(FREQ)

# Function to set color for an RGB LED
def set_color(led_red, led_green, led_blue, r, g, b):
    led_red.duty_u16(int(r * 65535 / 255))
    led_green.duty_u16(int(g * 65535 / 255))
    led_blue.duty_u16(int(b * 65535 / 255))

# Set both LEDs to white
set_color(red1, green1, blue1, 255, 255, 255)  # Full brightness for RGB LED 1
set_color(red2, green2, blue2, 255, 255, 255)  # Full brightness for RGB LED 2
