#!/usr/bin/env python3
#import numpy as numpy
import math as math
import ev3dev.ev3 as motor
import time

motor_a = motor.LargeMotor(motor.OUTPUT_A)
motor_b = motor.LargeMotor(motor.OUTPUT_B)

startTime = time.time()
theta_star = 500
vol = 0


j = 0
start_position = motor_a.position

k_p = 15.0
k_i = 24.0
k_d = 23.0

x = 0
y = 0
theta =0

r = 0.05536/2 
my_file = open(str(vol)+str(k_p)+" "+str(k_i)+" "+str(k_d)+" "+"file.txt","w+")
my_file.write(str(vol) + ":\n")
integral_i = 0.0
e = theta_star
h = 0.03
B = 0.17
dx = 0
dy = 0
dtheta = 0

px = 0.3
py = 0.3
ptheta = math.atan2(py, px)

x_speed_last = 0
y_speed_last = 0
omega_last = 0


while(theta != ptheta and x != px and y != py):
    t1 = time.time()
    omega_l = motor_b.speed * math.pi / 180
    omega_r = motor_a.speed * math.pi / 180

    vel_l = omega_l * r
    vel_r = omega_r * r

    vel = (vel_l + vel_r)/2
    
    
    omega = (omega_r - omega_l) * r / B

    print(str(x) + " " + str(y))

    dx_p = dx
    dy_p = dy
    dtheta_prev = dtheta

    dtheta = omega
    dx = vel * math.cos(theta)
    dy = vel * math.sin(theta)

    x += (dx_p + dx)*h/2
    y += (dy + dy_p)*h/2
    theta += dtheta*h




    ex = px - x
    ey = py - y
    
    beta = math.atan2(ey, ex)
    etheta = beta - theta
    
    e2 = math.sqrt(ex*ex + ey*ey)

    vol_l = 50.0 * e2 - 1.0 * etheta

    vol_r = 50.0 * e2 + 1.0 * etheta

    if (vol_l> 50.0):
        vol_l= 50.0
    if( vol_l< -50.0):
        vol_l= -50.0

    if (vol_r> 50.0):
        vol_r= 50.0
    if( vol_r< -50.0):
        vol_r= -50.0



    motor_a.run_direct(duty_cycle_sp = vol_l)
    motor_b.run_direct(duty_cycle_sp = vol_r)


    j = j + 1


    t2 = time.time()
    dt = (t2 - t1)
    
    if(h > dt):
        time.sleep(h - dt)
    else:
        print("warn")

   