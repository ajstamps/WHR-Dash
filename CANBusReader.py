from can import *
import os
import crcmod
from time import sleep


class CANBusReader:
    def __init__(self):
        # This sets up the channel for the can hat to read from
        os.system("sudo /sbin/ip link set can0 up type can bitrate 1000000")

        # USED FOR TESTING #
        # os.system("sudo modprobe vcan")
        # os.system("sudo ip link add dev vcan0 type vcan")
        # os.system("sudo ip link set up vcan0")

        # This sets up the reader itself
        self.bus = interface.Bus(channel='can0', bustype='socketcan_native')

        # Each one of these hold data at one point or another. #
        # This first one is the one that holds the current values
        self.can_data = [Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message]

        # This one is temporary to check if the data is valid (CRC32 checksum)
        self.temp_data = [Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message]

        # In early version, somehow things would return as not a number,
        # this was how I got around it. I kept the last sent data and
        # used a 'try except' just in case it blew up.
        self.prev_data = [Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message]

        self.crc32_func = crcmod.predefined.mkCrcFun('crc-32')

    # This is a fairly simple function. It grabs the values from the CAN bus,
    # checks their CRC, and if it passes sets it as the good to go values.
    def get_can_data(self):
        i = 0  # i is the counter for frames.

        # I should probably specify what I mean by frame. To me,
        # a frame is what one line from the CAN bus is. an example
        # would be RPM, which is on frame 0, at bytes 4 and 5.
        # It almost certainly isn't the correct word, but it's
        # what I came up with, so it's what I'm going to refer to it as.

        self.temp_data[i] = self.bus.recv()  # We grab one value to check if it is the beginning value

        # We then continually check if we have found the start frame (signified by 3 bytes)
        # see the function "is_message_start" to see what they are.
        while not self.is_message_start():
            self.temp_data[i] = self.bus.recv()

        # When it gets out of the loop we have found our start, then it's onto collecting the
        # rest of the frames. They always come out in the same order.
        while i < 21:
            i += 1
            self.temp_data[i] = self.bus.recv()

        # This is the CRC check. This checks the integrity of our data. If it isn't good, we just ignore it.
        if self.crc_check():
            self.prev_data = self.can_data[:]
            self.can_data = self.temp_data[:]

    def get_thread(self):
        while True:
            self.get_can_data()
            sleep(.1)

    def is_message_start(self):
        return self.temp_data[0].data[0] == 130 and self.temp_data[0].data[1] == 129 \
            and self.temp_data[0].data[2] == 128 and self.temp_data[0].data[3] == 84

    # I must've been doing something funky when I wrote this. It works, but don't ask me how.
    def crc_check(self):
        try:  # As is tradition, it's wrapped in a try except block
            dataval = bytearray()
            check = True

            for i in range(22):  # Go through all the CAN data (22 frames)
                if i < 21:  # We only have to worry about the last frame, as it has the CRC
                    for j in range(8):
                        dataval.append(self.temp_data[i].data[j])
                else:
                    for j in range(4):  # The last 4 bytes store the CRC value, so we don't add them in.
                        dataval.append(self.temp_data[i].data[j])
            # From here on down, it's just a mess. It works, so I'm not gonna touch it.
            crc = hex(self.crc32_func(dataval))  # This calculates the CRC check sum, now to just check it...

            # This splits up the CRC into 4 separate bytes.
            splitdataval = [crc[i:i + 2] for i in range(0, len(crc), 2)]

            # This checks the CRC Byte by Byte to the one provided by the M84 (ECU)
            for i in range(4):
                if hex(int(splitdataval[i + 1], 16)) == hex(self.temp_data[21].data[i + 4]) and check:
                    check = True
                else:
                    check = False

        except (IndexError, AttributeError):  # easily the hackiest solution I've ever made
            return False

        # If everything is all good, return the value
        return check

    # The default getter, returns things in the correct format that is specified.
    # can_frame is frame, hi is the high byte, lo is the low byte and scalar is what it should be multiplied by
    def default_get(self, can_frame, hi, lo, scalar):
        try:
            return (self.can_data[can_frame].data[hi] * 256 + self.can_data[can_frame].data[lo]) * scalar
        except (IndexError, AttributeError):
            print("Couldn't print data: frame {0}, hi {1}, lo {2}, scalar {3}".format(can_frame, hi, lo, scalar))
            return (self.prev_data[can_frame].data[hi] * 256 + self.prev_data[can_frame].data[lo]) * scalar

    # The data gets returned by taking its high byte, multiplying it by 256,
    # and adding its low byte. Some need to be multiplied by a scalar value.
    def get_rpm(self):  # Expressed in RPM (duh...)
        return self.default_get(0, 4, 5, 1)

    def get_tps(self):  # A percentage of the throttles position
        return self.default_get(0, 6, 7, 0.1)

    def get_engine_temp(self):  # Expressed in degrees fahrenheit
        return self.default_get(1, 4, 5, 0.1)

    def get_oil_pressure(self):  # Expressed in PSI (IIRC)
        return self.default_get(3, 4, 5, 0.1)

    def get_lambda_1(self):  # Expressed as current AFR over stoichiometric ratio (X/14.7) Less is rich, more is lean
        return self.default_get(1, 6, 7, 0.001)

    def get_battery_voltage(self):
        return self.default_get(6, 0, 1, 0.01)

    def get_gear(self):  # Supposed to what gear the driver is in, currently not calculated correctly by the ECU
        return self.default_get(14, 4, 5, 1)

    def get_digital_input_1(self):  # Supposed to be front left wheel speed, but is back left. No idea why. (MPH)
        return self.default_get(6, 4, 5, 0.1)

    def get_digital_input_2(self):  # Same story, just the other side. Back right instead of front right. (MPH)
        return self.default_get(6, 6, 7, 0.1)

    def get_digital_input_3(self):  # Front Left Wheel Speed (MPH)
        return self.default_get(7, 0, 1, 0.1)

    def get_digital_input_4(self):  # Front Right Wheel Speed (MPH)
        return self.default_get(7, 2, 3, 0.1)

    def get_drive_speed(self):  # This is the faster of the two back wheel speeds. TC/LC MUST be on for this to work.
        return self.default_get(7, 4, 5, 0.1)

    def get_ground_speed(self):  # Faster of the front wheel speeds. (MPH)
        return self.default_get(7, 6, 7, 0.1)

    def get_aux_out_2(self):  # Aux Out 2 (hopefully) refers to the fan, measured in a duty cycle (1%)
        return self.default_get(12, 0, 1, 1)
