import ev3dev2.motor as motor
import time

mototA = LargeMotor('outA')
voltages = [100, 80, 60, 40, 20, -20, -40, -60, -80, -100]
try:
    for vol in voltages:
        timeStart = time.time()
        startPos = mototA.position
        name = "data" + str (vol)
        file = open (name,"w")
        while True:
            timeNow = time.time() - timeStart
            motorA.run_direct(duty_cycle_sp = vol)
            pos = motorA. position - startPos
            file.write(str(timeNow) + ',' + str(pos) + ',' + str(motorA.speed) + "\n")
            if timeNow > 1:
                mototA.run_direct(duty_cycle_sp = 0)
                break
        file.close()
except Exception as e:
    raise e
finally:
    mototA.stop(stop_action = 'brake')
    file.close()