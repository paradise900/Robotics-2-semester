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


def change_coordinates(x_cur, y_cur, x_goal, y_goal):
    return (y_goal - y_cur, x_goal - x_cur)



DOTS = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 0)]
RADIUS = 0.041
BASE = 0.165
ERROR = 0.05
X, Y = 0, 0
k_s = 300
k_r = 100


motorleft = motor.LargeMotor('outB') # left wheel
motorright = motor.LargeMotor('outA') # right wheel

startPosleft = motorleft.position * pi / 180
startPosright = motorright.position * pi / 180

lastposleft = 0
lastposright = 0

x_current, y_current, theta = 0, 0, 0
timeStart = time.time()
i = 0
try:
    for x_goal, y_goal in DOTS:
        file = open("coord" + str(i), 'w')
        while True:
            timeNow = time.time() - timeStart
            posleft = motorleft.position * pi / 180 - startPosleft
            posright = motorright.position * pi / 180 - startPosright
            deltaposleft = posleft - lastposleft
            deltaposright = posright - lastposright
            x_current = x_current + (deltaposleft + deltaposright) * RADIUS * cos(theta) / 2
            y_current = y_current + (deltaposleft + deltaposright) * RADIUS * sin(theta) / 2
            theta = theta + (deltaposright - deltaposleft) * RADIUS / BASE
            distance = ((x_current - x_goal) ** 2 + (y_current - y_goal) ** 2) ** 0.5
            psi = atan2(y_goal - y_current, x_goal - x_current)
            alpha = check_angel(psi - theta)
            voltage_dist = check_vol(k_s * distance)
            voltage_ang = check_vol(k_r * alpha)
            motorleft.run_direct(duty_cycle_sp=check_vol(voltage_dist - voltage_ang))
            motorright.run_direct(duty_cycle_sp=check_vol(voltage_dist + voltage_ang))
            lastposleft = posleft
            lastposright = posright
            file.write(str(timeNow) + ',' + str(x_current) + ',' + str(y_current) + '\n')
            if distance < ERROR:
                file.close()
                i += 1
                break

except:
    print('asdlkjdklajdalskd')
    motorleft.run_direct(duty_cycle_sp = 0)
    motorright.run_direct(duty_cycle_sp = 0)
    file.close()
