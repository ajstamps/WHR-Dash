# 0-60 Timer file for WHR17 Dash
# receives ground speed and engine speed and calculates the zero to sixty time
# Created by Alex Stamps
# 4-29-17

import time
from datetime import datetime


# This class will not be rewritten for fear of hurting our current values.
# These are the way we store how long the engine is on.

# There are two files that we write to. One is a constant list that logs start times
# and every time it logs, and the other is the master value that refers to what the time is at the moment.
class TimeLogger:
    def __init__(self):
        specific_times = open('/home/pi/Dash/specificTimes.txt', 'a')
        specific_times.write('\nENGINE TIME FOR: ' + datetime.now().strftime('%Y/%m/%d-%H:%M') + '\n')
        specific_times.close()
        self.last_update_time = time.time()

    def check_if_update_needed(self, shifts):  # Checks if we have a new time update. Goes by minutes.
        if time.time()-self.last_update_time > 60:
            specific_times = open('/home/pi/Dash/specificTimes.txt', 'a')
            specific_times.write(datetime.now().strftime('%Y/%m/%d-%H:%M') + '\n')
            specific_times.close()
            self.write_new_time_and_shifts(shifts)
            self.last_update_time = time.time()

    @staticmethod
    def get_engine_time():  # Pulls the current time from the file
        times = open('/home/pi/Dash/times.txt', 'r')
        line = times.readline()
        try:
            eng_time = int(line[13:-1])
        except ValueError:  # I have no clue why, but for some reason it would give a ValueError and this is what worked
            eng_time = int(line[24:-1])
        times.close()
        return eng_time

    @staticmethod
    def get_shifts():  # Pulls how many shifts to date we have. Not very accurate, but a good reference)
        times = open('/home/pi/Dash/times.txt', 'r')
        times.readline()
        line = times.readline()
        shifts = int(line[7:-1])
        times.close()
        return shifts

    def write_new_time_and_shifts(self, val):  # Writes the new shift and time.
        eng_time = self.get_engine_time() + 1
        shifts = self.get_shifts() + val
        times = open('/home/pi/Dash/times.txt', 'w')
        times.write('Engine Time: {}\nShifts: {}\n'.format(eng_time, shifts))
        times.close()
