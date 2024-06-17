import ev3dev2.motor as motor
import time
from math import pi, cos, sin, atan2


def check_vol(vol):
    if vol > 100:
        vol = 100
    elif vol < -100:
        vol = -100
    return vol


def check_angel(angel):
    if angel > pi:
        return angel - 2 * pi
    elif angel + pi < 0:
        return angel + 2 * pi
    else:
        return angel


DOTS = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 0)]
RADIUS = 0.0217
BASE = 0.158
ERROR = 0.05
delta_t = 0.001
X, Y = 0, 0
k_s = 400
k_r = 100
a = 0.2
b = 0.5
c = 0.12

motorleft = motor.LargeMotor('outC') # left wheel
motorright = motor.LargeMotor('outB') # right wheel

startPosleft = motorleft.position * pi / 180
startPosright = motorright.position * pi / 180

lastposleft = 0
lastposright = 0

x_current, y_current, theta = 0, 0, 0
timeStart = time.time()
try:
    file = open("task3", 'w')
    while True:
        posleft = motorleft.position * pi / 180 - startPosleft
        posright = motorright.position * pi / 180 - startPosright
        deltaposleft = posleft - lastposleft
        deltaposright = posright - lastposright
        
        x_current = x_current + (deltaposleft + deltaposright) * RADIUS * cos(theta) / 2
        y_current = y_current + (deltaposleft + deltaposright) * RADIUS * sin(theta) / 2
        theta = theta + (deltaposright - deltaposleft) * RADIUS / BASE

        timeNow = time.time() - timeStart
        x_goal = a + b * sin(2 * c * (timeNow + delta_t))
        y_goal = b * sin(c * (timeNow + delta_t))

        distance = ((x_current - x_goal) ** 2 + (y_current - y_goal) ** 2) ** 0.5
        psi = atan2(y_goal - y_current, x_goal - x_current)
        alpha = check_angel(psi - theta)

        voltage_dist = check_vol(k_s * distance * cos(alpha))
        voltage_ang = check_vol(k_s * cos(alpha) * sin(alpha) + k_r * alpha)

        motorleft.run_direct(duty_cycle_sp=check_vol(voltage_dist - voltage_ang))
        motorright.run_direct(duty_cycle_sp=check_vol(voltage_dist + voltage_ang))
        lastposleft = posleft
        lastposright = posright
        file.write(str(timeNow) + ',' + str(x_current) + ',' + str(y_current) + '\n')
        if timeNow > 210:
            file.close()
            motorleft.run_direct(duty_cycle_sp = 0)
            time.sleep(0.1)
            motorright.run_direct(duty_cycle_sp = 0)
            time.sleep(0.1)
            break
except:
    print('Error')
    motorleft.run_direct(duty_cycle_sp = 0)
    time.sleep(0.1)
    motorright.run_direct(duty_cycle_sp = 0)
    time.sleep(0.1)
    file.close()