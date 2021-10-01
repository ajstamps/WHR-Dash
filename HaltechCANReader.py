# 1000000 bitrate
# interface socketcan
# channel can0

from can import *
import os
from threading import Thread


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

        self.can_data = {0x360: Message,
                         0x361: Message,
                         0x362: Message,
                         0x363: Message,
                         0x368: Message,
                         0x369: Message,
                         0x30A: Message,
                         0x36B: Message,
                         0x36C: Message,
                         0x36D: Message,
                         0x36E: Message,
                         0x36F: Message,
                         0x370: Message,
                         0x371: Message,
                         0x372: Message,
                         0x373: Message,
                         0x374: Message,
                         0x375: Message,
                         0x3E0: Message,
                         0x3E1: Message,
                         0x3E2: Message,
                         0X3E3: Message,
                         0X3E4: Message,
                         0x3E5: Message,
                         0x3E6: Message,
                         0x3E7: Message,
                         0x3E8: Message,
                         0x3E9: Message,
                         0x3EA: Message,
                         0x3EB: Message,
                         0x3EC: Message,
                         0x3ED: Message,
                         0x3DF: Message}

        self.thread = Thread(target=self.on_message_received, daemon=True)
        self.thread.start()

    def on_message_received(self):
        # Hashing the Arbitration ID to get its location in the Array
        while True:
            msg = self.bus.recv()

            try:
                self.can_data[msg.arbitration_id] = msg
            except IndexError:
                print(int(msg.arbitration_id, 16))

    # The default getter, returns things in the correct format that is specified.
    # can_frame is frame, hi is the high byte, lo is the low byte and scalar is what it should be multiplied by
    def default_get(self, can_frame, hi, lo, scalar):
        try:
            return (self.can_data[can_frame].data[hi] * 256 + self.can_data[can_frame].data[lo]) * scalar
        except (IndexError, AttributeError):
            print("Couldn't print data: frame {0}, hi {1}, lo {2}, scalar {3}".format(can_frame, hi, lo, scalar))
            return 1

    def default_get_mask(self, can_frame, data_no, mask):
        return self.can_data[can_frame].data[data_no] & mask

    def get_rpm(self):  # Expressed in Revolutions Per Minute
        return self.default_get(0x360, 0, 1, 1)

    def get_tps(self):  # A percentage of the throttles position
        return self.default_get(0x360, 4, 5, 0.1)

    def get_engine_temp(self):  # Expressed in degrees fahrenheit
        return self.default_get(0x3E0, 0, 1, 0.1)

    def get_oil_pressure(self):  # Expressed in PSI
        return self.default_get(0x391, 2, 3, 0.1)

    def get_lambda_1(self):  # Expressed as current AFR over stoichiometric ratio (X/14.7 for gasoline)
        return self.default_get(0x368, 0, 1, 0.001)

    def get_battery_voltage(self):  # Expressed in Voltage
        return self.default_get(0x372, 0, 1, 0.1)

    def get_gear(self):  # Supposed to what gear the driver is in, not reading correctly
        return self.default_get(0x370, 2, 3, 1)

    def get_digital_input_1(self):  # Front Left Wheel Speed. (MPH)
        return self.default_get(0x36C, 0, 1, 0.1)

    def get_digital_input_2(self):  # Front Right Wheel Speed. (MPH)
        return self.default_get(0x36C, 2, 3, 0.1)

    def get_digital_input_3(self):  # Back Left Wheel Speed (MPH)
        return self.default_get(0x36C, 4, 5, 0.1)

    def get_digital_input_4(self):  # Back Right Wheel Speed (MPH)
        return self.default_get(0x36C, 6, 7, 0.1)

    def get_drive_speed(self):  # This is the faster of the two back wheel speeds. TC/LC MUST be on for this to work.
        return self.default_get(9, 2, 3, 0.1)

    def get_ground_speed(self):  # Faster of the front wheel speeds. (MPH)
        return self.default_get(9, 0, 1, 0.1)

    def get_sig_acquired(self):  # Determines of Data Acquisition Component has a WiFi signal
        return self.default_get_mask(0x3DF, 0, 0b10000000)

    def get_sig_searching(self):  # Determines if we are searching for a WiFi Signal (opposite of get_sig_acquired
        return self.default_get_mask(0x3DF, 0, 0b01000000)

    def get_data_transfer_init(self):  # True if transferring data to DB
        return self.default_get_mask(0x3DF, 0, 0b00100000)

    def get_data_transfer_complete(self):  # True if data transfer is completed
        return self.default_get_mask(0x3DF, 0, 0b00010000)

    # def get_aux_out_2(self):  # Aux Out 2 (hopefully) refers to the fan, measured in a duty cycle (1%)
    #     return self.default_get(12, 0, 1, 1)
