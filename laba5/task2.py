import ev3dev2.motor as motor
import time
from math import pi, cos, sin, atan2


def check_vol(vol):
    if vol > 50:
        vol = 50
    elif vol < -50:
        vol = -50
    return vol


def check_angel(angel):
    if angel > pi:
        return angel - 2 * pi
    elif angel + pi < 0:
        return angel + 2 * pi
    else:
        return angel


DOTS = [(0.7, 0), (0, 0.7), (-0.7, 0), (0, -0.7), (0.7, 0)]
RADIUS = 0.0279
BASE = 0.178
ERROR = 0.05
X, Y = 0, 0
k_s = 1500
k_r = 800


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
    file = open("task2", 'w')
    for x_goal, y_goal in DOTS:
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

            voltage_dist = check_vol(k_s * distance * cos(alpha))
            voltage_ang = check_vol(k_s * cos(alpha) * sin(alpha) + k_r * alpha)
            
            motorleft.run_direct(duty_cycle_sp=check_vol(voltage_dist - voltage_ang))
            motorright.run_direct(duty_cycle_sp=check_vol(voltage_dist + voltage_ang))

            lastposleft = posleft
            lastposright = posright
            file.write(str(timeNow) + ',' + str(x_current) + ',' + str(y_current) + '\n')
            if distance < ERROR:
                motorleft.stop(stop_action = 'brake')
                motorright.stop(stop_action = 'brake')
                break
except:
    print('Error')
    motorleft.run_direct(duty_cycle_sp = 0)
    motorright.run_direct(duty_cycle_sp = 0)
    file.close()

file.close()