import ev3dev2.motor as motor
import time
import math


def check_vol(vol):
    if vol > 100:
        vol = 100
    elif vol < -100:
        vol = -100
    return vol

motorleft = motor.LargeMotor('outA') # left wheel
motorright = motor.LargeMotor('outB') # right wheel
# goals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
goals = [(1, 0)]
r = 0.0212
B = 0.156
eps = 0.01
k_s = 100
k_r = 100

timeStart = time.time()
startPosleft = motorleft.position
startPosright = motorright.position
lastposleft = startPosleft * math.pi / 180
lastposright = startPosright * math.pi / 180
x_cur, y_cur, theta = 0, 0, 0
try:
    for x_goal, y_goal in goals:
        # file = open(f'coord({x_goal}, {y_goal})', 'w')
        while True:
            timeNow = time.time() - timeStart

            posleft = (motorleft.position - startPosleft) * math.pi / 180
            posright = (motorright.position - startPosright) * math.pi / 180

            d_posleft = posleft - lastposleft
            d_posright = posright - lastposright
            
            x_cur = x_cur + (d_posleft + d_posright) * r * math.cos(theta) / 2
            y_cur = y_cur + (d_posleft + d_posright) * r * math.sin(theta) / 2
            theta = theta + (d_posright - d_posleft) * r / B

            ro = ((x_cur - x_goal) ** 2 + (y_cur - y_goal) ** 2) ** 0.5
            psi = math.atan2((y_goal - y_cur), (x_goal - x_cur))
            alpha = psi - theta

            U_s = check_vol(k_s * ro)
            U_r = check_vol(k_r * alpha)

            # motorleft.run_direct(duty_cycle_sp=(check_vol(U_s - U_r)))
            # motorright.run_direct(duty_cycle_sp=(check_vol(U_s + U_r)))
            motorleft.run_direct(duty_cycle_sp=100)
            motorright.run_direct(duty_cycle_sp=100)


            # file.write(str(timeNow) + ',' + str(x) + ',' + str(y) + ',' + str(theta))

            print(x_cur, y_cur, theta)
            lastposleft = posleft
            lastposright = posright
            if ro < eps:
                break
except:
    motorleft.run_direct(duty_cycle_sp = 0)
    motorright.run_direct(duty_cycle_sp = 0)

