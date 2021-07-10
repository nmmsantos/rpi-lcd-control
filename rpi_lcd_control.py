#!/usr/bin/env python

import time
from subprocess import run  # nosec

import VL53L0X

vcgencmd = "/usr/bin/vcgencmd"

tof = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)
tof.open()
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.GOOD)

timing = tof.get_timing()

if timing < 20000:
    timing = 20000

sleeptime = timing / 1000000.00

print("Timing %d ms" % (timing / 1000))

ison = True
run([vcgencmd, "display_power", "1"], shell=False, check=True)  # nosec
countdown = 0
distances = [0, 0, 0]

try:
    while True:
        distance = tof.get_distance()

        if distance > 0:
            distances[0] = distances[1]
            distances[1] = distances[2]
            distances[2] = distance
            dmean = sum(distances) // 3

            if dmean < 2800:
                countdown = 0

                if not ison:
                    ison = True
                    print(distances)
                    run([vcgencmd, "display_power", "1"], shell=False, check=True)  # nosec
            else:
                if ison:
                    countdown += sleeptime
                    if countdown > 3:
                        ison = False
                        run([vcgencmd, "display_power", "0"], shell=False, check=True)  # nosec

        time.sleep(sleeptime)
except KeyboardInterrupt:
    pass

tof.stop_ranging()
tof.close()
