import time


class Timer:
    def __init__(self):
        self.fifteen = 0.0
        self.thirty = 0.0
        self.sixty = 0.0
        self.current_time = 0.0
        self.start_time = 0.0
        self.launch_rpm = 0
        self.timing = False
        self.fifteen_done = False
        self.thirty_done = False
        self.sixty_done = False
        self.done = False

    # We time speed and log launch RPM for launch control/traction control
    def run_timer(self, speed, rpm):
        if speed == 0:  # The base value, we could reset the values here, but not necessary.
            self.timing = False  # Refers to ALL the timing. If one value is still being timed, it will stay true.
            self.fifteen_done = False  # This (and all other variables) refer to whether it is still being timed.
            self.thirty_done = False
            self.sixty_done = False
            # self.done is the final say in whether it is done timing or not.
            # If this isn't here, when speed drops below the value (e.g. 15)
            # it will start timing again.
            self.done = False

        elif speed != 0 and not self.timing and not self.done:
            self.timing = True
            self.start_time = time.time()
            self.launch_rpm = rpm

        elif self.timing:

            # This set of if statements continually counts up the values.
            # When the speed goes above its value (e.g. 16 MPH), we want
            # to stop incrementing it. We could tie this into the if
            # block below, but I see them as 2 separate pieces. One is
            # incrementing the times, and the other is checking to see
            # if we have hit the speed we want.
            if speed < 15 and not self.fifteen_done:
                self.fifteen = time.time() - self.start_time
                self.thirty = time.time() - self.start_time
                self.sixty = time.time() - self.start_time
            elif speed < 30 and not self.thirty_done:
                self.thirty = time.time() - self.start_time
                self.sixty = time.time() - self.start_time
            elif speed < 60 and not self.sixty_done:
                self.sixty = time.time() - self.start_time

            # Check to see if we should stop timing for 0-15
            if speed > 15 and not self.fifteen_done:
                self.fifteen = time.time() - self.start_time
                self.fifteen_done = True

            # Check to see if we should stop timing for 0-30
            if speed > 30 and not self.thirty_done:
                self.thirty = time.time() - self.start_time
                self.thirty_done = True

            # Check to see if we should stop timing for 0-60, aka stop altogether
            if speed > 60 and not self.sixty_done:
                self.sixty = time.time() - self.start_time
                self.sixty_done = True
                self.done = True
                self.timing = False

            # If the time goes above 10 seconds, just stop.
            if time.time() - self.start_time >= 10:
                self.done = True
                self.timing = False

    # Returns the value. I'm not a big fan of (object).variables, feels wrong.
    # I was always taught to use setters and getters to help regulate what the
    # program can and can't change/see.
    def get_fifteen(self):  # 0-15 time
        return self.fifteen

    def get_thirty(self):  # 0-30 time
        return self.thirty

    def get_sixty(self):  # 0-60 time
        return self.sixty

    def get_launch_rpm(self):
        return self.launch_rpm  # Launch RPM
