import RPi.GPIO as GPIO
import time

# Setup RPi.GPIO for LEDs
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

led_ids = {
    'green': 12,
    'yellow': 10,
    'red': 8,
    'ped_green': 11,
    'ped_red': 13,
    'white': 15
}

button_pin = 35
button_pressed = False

class Led:
    def __init__(self, pin: int, color="Not specified"):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
    
    def on_for(self, seconds: int):
        self.on()
        time.sleep(seconds)
        self.off()
    
    def blink_for(self, blink_count: int, blink_time=0.5):
        for _ in range(blink_count):
            self.on_for(blink_time)
            time.sleep(blink_time)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

leds = {color: Led(color=color, pin=pin) for color, pin in led_ids.items()}

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def check_button():
    global button_pressed
    state = GPIO.input(button_pin)
    if state == GPIO.LOW:
        button_pressed = True
        leds['white'].on_for(1)

# Setup lgpio for the button
def traffic_light():
    global button_pressed
    while True:
        leds['red'].on()
        for _ in range(50):
            check_button()
            time.sleep(0.1)
        leds['red'].off()
        
        if button_pressed:
            leds['ped_red'].off()
            leds['ped_green'].on_for(5)
            leds['ped_red'].on()
            button_pressed = False
        
        leds['yellow'].on_for(1)
        leds['green'].on()
        for _ in range(50):
            check_button()
            time.sleep(0.1)
        leds['green'].off()
        leds['yellow'].blink_for(3)

try:
    leds['ped_red'].on()
    traffic_light()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
