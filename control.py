import ev3dev2.motor as motor
import time

motor_a = motor.LargeMotor(motor.OUTPUT_B)
vol = 100
startTime = time.time()
while True:
    currentTime = time.time() - startTime
    motor_pose = motor_a.position
    motor_vel = motor_a.speed
    motor_a.run_direct(duty_cycle_sp = vol)
    if currentTime > 1:
        motor_a.run_direct(duty_cycle_sp = 0)
        break
        