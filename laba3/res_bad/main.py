from ev3dev2.motor import LargeMotor
import time

finish_position = 200
motor = LargeMotor('outB')
k_p = 3.5
k_i = 0
k_d = 0.00
h = 0.05
with open("data.csv", "w") as file:
    start_time = time.time()
    start_position = motor.position
    time_pred = 0
    ei = 0
    e_pred = finish_position
    while True:
        t1 = time.time()
        position_from_start = motor.position - start_position
        e = finish_position - position_from_start
        de = (e - e_pred) / h
        ei += (e + e_pred) * h / 2
        time_pred = t1
        e_pred = e
        U = (k_p * e + k_i * ei + k_d * de)
        print(e, ei, de, U)
        if U > 100:
            U = 100
        if U < -100:
            U = -100
        motor.run_direct(duty_cycle_sp=U)
        t2 = time.time()
        time_from_start = time.time() - start_time
        dt = t2 - t1
        if (h > dt):
            time.sleep(h - dt)
        else:
            print('warning')
        file.write("{},{},{}\n".format(t1 - start_time, position_from_start, motor.speed))
        if time_from_start > 10:
            motor.run_direct(duty_cycle_sp=0)
            break
    file.write("end\n")

