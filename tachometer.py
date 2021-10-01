from neopixel import *


class Tachometer:
    def __init__(self, max_val, can):
        self.strip = Adafruit_NeoPixel(16, 18, 800000, 5, False, 255)
        self.strip.begin()
        self.max_val = max_val  # The RPM max (currently 15000)
        self.can = can

    def rev(self):  # val refers to the value that the LEDs should reflect (RPM)
        val = self.can.get_rpm()
        # This calculates how many LEDs we should turn on
        val_led = int((val/self.max_val) * self.strip.numPixels())

        # We have to go through all the LEDs, otherwise they all won't be updated
        for i in range(self.strip.numPixels()):
            if i <= val_led:  # If the LED is less than or equal to the value, turn it on
                # These set the color of the LED starting at the lowest val, then moving up
                if i <= 1:
                    self.strip.setPixelColor(i, Color(0, 0, 255))
                elif i <= 8:
                    self.strip.setPixelColor(i, Color(255, 0, 0))
                elif i <= 12:
                    self.strip.setPixelColor(i, Color(255, 255, 0))
                elif i <= 15:
                    self.strip.setPixelColor(i, Color(0, 255, 0))
            else:
                self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

    def clear(self):  # This just turns all the NeoPixels off
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
