import pygame


# Screen is what is output on the screen.
class Screen:
    def __init__(self, surface):
        # Colors in a dict. It just works.
        self.Colors = dict(
            black=(0, 0, 0),
            red=(255, 0, 0),
            blue=(0, 0, 255),
            green=(0, 255, 0),
            purple=(255, 0, 255),
            yellow=(255, 255, 0),
            orange=(255, 128, 0),
            darkGrey=(64, 64, 64),
            white=(255, 255, 255)
        )

        # FONTS #
        self.font_xlarge = pygame.font.Font(None, 256)
        self.font_large = pygame.font.Font(None, 192)
        self.font_xmedium = pygame.font.Font(None, 128)  # Yes, extra medium.
        self.font_medium = pygame.font.Font(None, 100)
        self.font_small = pygame.font.Font(None, 64)
        self.font_xsmall = pygame.font.Font(None, 32)
        # We currently don't use them all, but might some day. They all look good, so keeping them

        try:
            self.battery_image = pygame.image.load("Pictures/batteryImage.png")
            self.water_temp_image = pygame.image.load("Pictures/waterTempImage.png")
            self.oil_pressure_image = pygame.image.load("Pictures/oilPressureImage.png")
            self.lambda_image = pygame.image.load("Pictures/AFRatioImage.png")
            self.fan_on_image = pygame.image.load("Pictures/fanOnImage.png")

            # self.symbols = {
            #     "search" : pygame.image.load("/home/pi/Dash/Pictures/wifiSearch.png"),
            #     "found" : pygame.image.load("/home/pi/Dash/Pictures/WifiFound.png"),
            #     "init" : pygame.image.load("/home/pi/Dash/Pictures/DataInit.png"),
            #     "complete" : pygame.image.load("/home/pi/Dash/Pictures/DataComplete.png")
            # }
        except pygame.error:
            self.battery_image = pygame.image.load("/home/pi/Dash/Pictures/batteryImage.png")
            self.water_temp_image = pygame.image.load("/home/pi/Dash/Pictures/waterTempImage.png")
            self.oil_pressure_image = pygame.image.load("/home/pi/Dash/Pictures/oilPressureImage.png")
            self.lambda_image = pygame.image.load("/home/pi/Dash/Pictures/AFRatioImage.png")
            self.fan_on_image = pygame.image.load("/home/pi/Dash/Pictures/fanOnImage.png")


            # self.symbols = {
            #     "search": pygame.image.load("Pictures/wifiSearch.png"),
            #     "found": pygame.image.load("Pictures/WifiFound.png"),
            #     "init": pygame.image.load("Pictures/DataInit.png"),
            #     "complete": pygame.image.load("Pictures/DataComplete.png")
            # }

        self.symbol_rects = {
            
        }
        self.battery_image_rect = (195 / 2 - self.battery_image.get_rect().width / 2 + 600, 140)
        self.water_temp_image_rect = (195 / 2 - self.water_temp_image.get_rect().width / 2 + 200, 0)
        self.oil_pressure_image_rect = (195 / 2 - self.oil_pressure_image.get_rect().width / 2, 0)
        self.lambda_image_rect = (195 / 2 - self.lambda_image.get_rect().width / 2 + 400, 140)
        self.fan_on_image_rect = (195 / 2 - self.fan_on_image.get_rect().width / 2 + 200, 0)

        # I declared this up here since it never actually changes
        self.info_title = self.font_small.render("Information", 1, self.Colors['black'])
        self.info_title_rect = (395 / 2 - self.info_title.get_rect().width / 2 + 0, 140)

        self.calcs_title = self.font_small.render("ACCEL TIMES", 1, self.Colors['black'])
        self.calcs_title_rect = (400 / 2 - self.calcs_title.get_rect().width / 2 + 400, 280)

        self.surface = surface  # This is the surface to draw to

    def draw_gear(self, gear):
        # CALCULATE VALUES #
        text = self.font_xlarge.render("{0}".format(gear), 1, (0, 0, 0))  # The text to be output to the screen.

        # I'll be honest, I'm really proud of this simple fix.
        # I'm gonna talk about it for a bit. text_rect refers to the
        # rectangle that the text would occupy. We haven't given it
        # its coordinates to occupy yet, so we can give it what its
        # right and top edge should be touching, and pygame will calculate
        # what the x and y values should be. We do this because when we just give it x and y values,
        # it likes to bounce around as the value changes. This keeps the decimal points lined up
        # as the value changes, much easier for the driver to read.
        # My original solution involved calculating it the hard way.
        # Out of all this code, these 3 lines are my favorite. IT JUST WORKS SO WELL!
        text_rect = text.get_rect()
        text_rect.right = 550
        text_rect.top = -10

        # PRINT #
        pygame.draw.rect(self.surface, self.Colors['green'], (400, 0, 195, 135))
        self.surface.blit(text, text_rect)

    def draw_engine_temp(self, engine_temp, fan_on):
        # CALCULATE VALUES #
        text = self.font_medium.render("{0:.1f}".format(round(engine_temp, 1)), 1, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.right = 380
        text_rect.top = 60

        # COLOR #
        if engine_temp < 150:
            color = self.Colors['yellow']
        elif engine_temp > 230:
            color = self.Colors['red']
        else:
            color = self.Colors['green']

        # PRINT #
        pygame.draw.rect(self.surface, color, (200, 0, 195, 135))
        if not fan_on:
            self.surface.blit(self.water_temp_image, self.water_temp_image_rect)
        else:
            self.surface.blit(self.fan_on_image, self.fan_on_image_rect)
        self.surface.blit(text, text_rect)

    def draw_oil_pressure(self, oil_pressure):
        # CALCULATE VALUES #
        text = self.font_medium.render("{0:.1f}".format(round(oil_pressure, 1)), 1, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.right = 180
        text_rect.top = 60

        # COLOR #
        if oil_pressure < 10:
            color = self.Colors['red']
        elif oil_pressure > 50:
            color = self.Colors['yellow']
        else:
            color = self.Colors['green']

        # PRINT #
        pygame.draw.rect(self.surface, color, (0, 0, 195, 135))
        self.surface.blit(self.oil_pressure_image, self.oil_pressure_image_rect)
        self.surface.blit(text, text_rect)

    def draw_battery_voltage(self, battery_voltage):
        # CALCULATE VALUES #
        text = self.font_medium.render("{0:.2f}".format(round(battery_voltage, 2)), 1, self.Colors['black'])
        text_rect = text.get_rect()
        text_rect.right = 780
        text_rect.top = 200

        # COLOR #
        if battery_voltage < 12:
            color = self.Colors['orange']
        elif battery_voltage > 14.6:  # This might have to raised, but anything higher than 13.8 is too high IMO.
            color = self.Colors['red']
        else:
            color = self.Colors['green']

        # PRINT #
        pygame.draw.rect(self.surface, color, (600, 140, 200, 135))
        self.surface.blit(self.battery_image, self.battery_image_rect)
        self.surface.blit(text, text_rect)

    def draw_speed(self, speed):
        # CALCULATE VALUES #
        text = self.font_large.render("{0}".format(int(speed)), 1, self.Colors['black'])
        text_rect = text.get_rect()
        text_rect.right = 775
        text_rect.top = 0

        # PRINT #
        pygame.draw.rect(self.surface, self.Colors['green'], (600, 0, 200, 135))
        self.surface.blit(text, text_rect)

    def draw_lambda(self, _lambda):  # lambda is a built in name to Python, thus _lambda
        # CALCULATE VALUES #
        text = self.font_medium.render("{0:.3f}".format(round(_lambda, 3)), 1, self.Colors['black'])

        # This part makes it so the decimal always lines up, easier to read at a glance
        text_rect = text.get_rect()
        text_rect.right = 580
        text_rect.top = 200

        # PRINT #
        pygame.draw.rect(self.surface, self.Colors['green'], (400, 140, 195, 135))
        self.surface.blit(self.lambda_image, self.lambda_image_rect)
        self.surface.blit(text, text_rect)

    # Renamed to draw log, as its function has changed from errors to other things
    def draw_calcs(self, fifteen, thirty, sixty, launch_rpm):
        # pygame.draw.rect(self.surface, self.Colors['blue'], (0, 140, 395, 340))
        pygame.draw.rect(self.surface, self.Colors['blue'], (400, 280, 400, 240))
        sixty_text = self.font_xsmall.render("Sixty: {0:.2f}".format(sixty), 1, self.Colors['black'])
        thirty_text = self.font_xsmall.render("Thirty: {0:.2f}".format(thirty), 1, self.Colors['black'])
        fifteen_text = self.font_xsmall.render("Fifteen: {0:.2f}".format(fifteen), 1, self.Colors['black'])
        launch_rpm_text = self.font_xsmall.render("Launch RPM: {0}".format(launch_rpm), 1, self.Colors['black'])

        self.surface.blit(self.calcs_title, self.calcs_title_rect)
        self.surface.blit(sixty_text, (615, 320))
        self.surface.blit(thirty_text, (615, 345))
        self.surface.blit(fifteen_text, (615, 370))
        self.surface.blit(launch_rpm_text, (600, 395))

    def draw_info(self, ip_address, aux_out_2):
        pygame.draw.rect(self.surface, self.Colors['blue'], (0, 140, 395, 340))
        ip_address_text = self.font_xsmall.render("IP Address: {0}".format(ip_address), 1, self.Colors['black'])
        aux_out_2_text = self.font_xsmall.render("Aux Out 2: {0}%".format(aux_out_2), 1, self.Colors['black'])

        self.surface.blit(self.info_title, self.info_title_rect)
        self.surface.blit(ip_address_text, (15, 205))
        self.surface.blit(aux_out_2_text, (15, 230))

    # def draw_symbols(self, symbols):
