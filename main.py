from screen import Screen
from timer import Timer
import pygame
import sys
# from HaltechCANReader import CANBusReader


def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    size = width, height = 800, 480
    screen = pygame.display.set_mode(size)
    display = Screen(screen)
    timer = Timer()
    # can = CANBusReader()

    while True:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_ESCAPE]:
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # GET VALUES #
        # engine_temp = can.get_engine_temp()
        # battery_voltage = can.get_battery_voltage()
        # oil_pressure = can.get_oil_pressure()
        # speed = can.get_ground_speed()
        # _lambda = can.get_lambda_1()
        # gear = can.get_gear()
        # fan = can.get_aux_out_2()
        # fan = 0
        # rpm = can.get_rpm()
        # tps = can.get_tps()

        engine_temp = 220
        battery_voltage = 12.8
        oil_pressure = 35.1
        speed = 35.3
        _lambda = 0.95
        gear = 2
        fan = 0
        rpm = 9500

        # SCREEN RESET #
        screen.fill((255, 255, 0))  # seems to take a long time, but might be the only way to do this

        # TIMER #
        timer.run_timer(speed, rpm)

        # TACHOMETER #

        # DRAW MODULES #
        display.draw_battery_voltage(battery_voltage)
        display.draw_gear(gear)
        display.draw_lambda(_lambda)
        display.draw_oil_pressure(oil_pressure)
        display.draw_speed(speed)
        display.draw_engine_temp(engine_temp, fan)
        display.draw_calcs(timer.get_fifteen(), timer.get_thirty(), timer.get_sixty(), timer.get_launch_rpm())
        display.draw_info("Not Connected", fan)  # TODO Add in IP Address

        # UPDATE SCREEN #
        pygame.display.update()


if __name__ == '__main__':
    main()
