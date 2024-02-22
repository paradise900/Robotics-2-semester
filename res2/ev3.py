import ev3dev2.motor as motor
import time

motorA = motor.LargeMotor('outA')
voltages = [10, 15, 20, 25, 30, 35, 40, 45, 50]
try:
    for vol in voltages:
        timeStart = time.time()
        startPos = motorA.position
        name = "data" + str (vol)
        file = open (name,"w")
        while True:
            timeNow = time.time() - timeStart
            motorA.run_direct(duty_cycle_sp = vol)
            pos = motorA. position - startPos
            file.write(str(timeNow) + ',' + str(pos) + ',' + str(motorA.speed) + "\n")
            if timeNow > 1:
                motorA.run_direct(duty_cycle_sp = 0)
                break
        file.close()
except Exception as e:
    raise e
finally:
    motorA.stop(stop_action = 'brake')
    file.close()
