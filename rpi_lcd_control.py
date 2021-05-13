#!/usr/bin/env python

import time
import VL53L0X
from os import system

tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
tof.open()
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.get_timing()

if timing < 100000:
    timing = 100000

sleeptime = timing/1000000.00

print("Timing %d ms" % (timing/1000))

ison = True
system('vcgencmd display_power 1')
countdown = 0

try:
    while True:
        distance = tof.get_distance()

        if distance < 6000:
            countdown = 0

            if not ison:
                ison = True
                system('vcgencmd display_power 1')
        else:
            if ison:
                countdown += sleeptime
                if countdown > 3:
                    ison = False
                    system('vcgencmd display_power 0')

        time.sleep(sleeptime)
except KeyboardInterrupt:
    pass

tof.stop_ranging()
tof.close()
