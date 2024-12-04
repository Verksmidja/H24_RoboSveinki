from machine import Pin, PWM, ADC
import asyncio
from Lib.dfplayer import DFPlayer

# Initialize DFPlayer
df = DFPlayer(2)
df.init(tx=17, rx=16)

# Servo for jaw movement
jaw_pin = 36
jaw_servo = PWM(Pin(jaw_pin), freq=50)

# ADC to read values from DAC
audio_intensity_pin = ADC(Pin(14))
audio_intensity_pin.atten(ADC.ATTN_11DB)  # 3.3V range

# Jaw angle settings
min_jaw_angle = 0  # Fully closed
max_jaw_angle = 44  # Fully open

# ADC range and dynamic scaling
min_adc_value = 700 # Starting min (adjust for noise floor)
max_adc_value = 2000  # Starting max (adjust based on observed values)
noise_threshold = 600  # Ignore ADC values below this

# Function to dynamically adjust ADC range
def adjust_adc_range(adc_value):
    global min_adc_value, max_adc_value
    # Dynamically expand the range as needed
    if adc_value < min_adc_value and adc_value > noise_threshold:
        min_adc_value = adc_value
    if adc_value > max_adc_value:
        max_adc_value = adc_value

# Function to map ADC value to jaw angle
def map_adc_to_jaw_angle(adc_value):
    # Ignore noise
    if adc_value < noise_threshold:
        return min_jaw_angle
    # Avoid divide-by-zero errors
    if max_adc_value == min_adc_value:
        return min_jaw_angle
    # Scale ADC value within the dynamic range
    scaled_adc_value = (adc_value - min_adc_value)
    scaled_adc_value = max(0, min(scaled_adc_value, max_adc_value - min_adc_value))  # Clamp to range
    # Map to jaw angle range
    return min_jaw_angle + (scaled_adc_value / (max_adc_value - min_adc_value)) * (max_jaw_angle - min_jaw_angle)

# Set jaw angle on servo
def set_jaw_angle(angle):
    duty = int(40 + (angle / 180) * 115)  # Convert angle to PWM
    jaw_servo.duty(duty)

# Main function
async def main():
    global min_adc_value, max_adc_value
    await df.wait_available()
    await df.volume(30)  # Set volume
    await df.play(1, 1)  # Start playback

    while True:
        # Read ADC value
        raw_adc = audio_intensity_pin.read()

        # Adjust ADC range dynamically
        adjust_adc_range(raw_adc)

        # Map ADC value to jaw angle
        jaw_angle = map_adc_to_jaw_angle(raw_adc)
        
        # Debug output
        print(f"Raw ADC: {raw_adc}, Min ADC: {min_adc_value}, Max ADC: {max_adc_value}, Jaw Angle: {jaw_angle}")

        # Set jaw angle
        set_jaw_angle(jaw_angle)
        
        await asyncio.sleep(0.03)

# Run the main function
asyncio.run(main())

