import pygame


class Display:
    Colors = None

    try:
        symbols = {
            "search": pygame.image.load("Pictures/wifi-disconnect.png"),
            "found": pygame.image.load("Pictures/wifi-connect.png"),
            "init": pygame.image.load("Pictures/uploading.png"),
            "complete": pygame.image.load("Pictures/upload-complete.png"),
            "AFR": pygame.image.load("Pictures/AFRatioImage.png"),
            "Battery": pygame.image.load("Pictures/batteryImage.png"),
            "Oil Pressure": pygame.image.load("Pictures/oilPressureImage.png"),
            "Water Temp": pygame.image.load("Pictures/waterTempImage.png"),
            "Fan On": pygame.image.load("Pictures/fanOnImage.png")
        }
    except pygame.error:
        symbols = {
            "search": pygame.image.load("/home/pi/Dash/Pictures/wifi-disconnect.png"),
            "found": pygame.image.load("/home/pi/Dash/Pictures/wifi-connect.png"),
            "init": pygame.image.load("/home/pi/Dash/Pictures/uploading.png"),
            "complete": pygame.image.load("/home/pi/Dash/Pictures/upload-complete.png"),
            "AFR": pygame.image.load("/home/pi/Dash/Pictures/AFRatioImage.png"),
            "Battery": pygame.image.load("/home/pi/Dash/Pictures/batteryImage.png"),
            "Oil Pressure": pygame.image.load("/home/pi/Dash/Pictures/oilPressureImage.png"),
            "Water Temp": pygame.image.load("/home/pi/Dash/Pictures/waterTempImage.png"),
            "Fan On": pygame.image.load("/home/pi/Dash/Pictures/fanOnImage.png")
        }

    font_sizes = {
        "medium": pygame.font.Font(None, 100),
        "small": pygame.font.Font(None, 32)
    }

    def __init__(self, surface):
        self.surface = surface

    class DisplayBlock:
        def __init__(self, rect, text, color, surface):
            self.rect = rect
            self.text = text
            self.color = color
            self.surface = surface
            self.image = None

            if self.text in Display.symbols:
                self.image = Display.symbols[self.text]

        def display(self, data):
            text = Display.font_sizes[""].render("{0}".format(data), 1, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.right = self.rect.right - 2
            text_rect.top = self.rect.bottom - 2

            image_rect = self.image.get_rect()

            image_display_rect = (self.rect / 2 - image_rect.width / 2, self.rect[1] - 2)

            if self.image:
                self.surface.blit(self.image, image_display_rect)
            else:
                pygame.draw.rect(self.surface, Display.Colors[self.color], (400, 0, 195, 135))

    class HiLoDisplayBlock(DisplayBlock):
        def __init__(self, rect, text, color, surface, hi, lo, hi_color, lo_color):
            super().__init__(rect, text, color, surface)
            self.hi = hi
            self.lo = lo
            self.hi_color = hi_color
            self.lo_color = lo_color

        def display(self, data):
            text = Display.font_sizes[""].render("{0}".format(data), 1, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.right = self.rect.right - 2
            text_rect.top = self.rect.bottom - 2

            if data > self.hi:
                color = self.hi_color
            elif data < self.lo:
                color = self.lo_color
            else:
                color = self.color

            image_rect = self.image.get_rect()

            image_display_rect = (self.rect/2 - image_rect.width/2, self.rect[1] - 2)

            if self.image:
                self.surface.blit(self.image, image_display_rect)

            pygame.draw.rect(self.surface, color, (400, 0, 195, 135))
