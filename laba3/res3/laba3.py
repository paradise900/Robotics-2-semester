import ev3dev2.motor as motor
import time
import math


class laba3:
    h = 0.001
    theta_goal = 360
    vol = 100
    motorA = motor.LargeMotor('outA')


    def check_vol(self, vol):
        if vol > 100:
            vol = 100
        elif vol < -100:
            vol = -100
        return vol


    def rele(self):
        vol = 100
        timeStart = time.time()
        startPos = self.motorA.position
        file = open('rele', 'w')
        while True:
            timeNow = time.time() - timeStart
            self.motorA.run_direct(duty_cycle_sp = vol)
            pos = self.motorA.position - startPos
            file.write(str(timeNow) + ',' + str(pos) + "\n")
            timeNow1 = time.time() - timeStart
            if time.time() - timeStart > 3:
                self.motorA.run_direct(duty_cycle_sp = 0)
                break
            if pos < self.theta_goal:
                vol = 100
            elif pos == self.theta_goal:
                vol = 0
            else:
                vol = -100
        file.close()
    

    def p_reg(self, k_p):
        vol = 100
        timeStart = time.time()
        startPos = self.motorA.position
        file = open('p_reg', 'w')
        while True:
            timeNow = time.time() - timeStart
            self.motorA.run_direct(duty_cycle_sp = vol)
            pos = self.motorA.position - startPos
            file.write(str(timeNow) + ',' + str(pos) + "\n")
            timeNow1 = time.time() - timeStart
            if timeNow1 - timeNow < self.h:
                time.sleep(h - timeNow1 + timeNow)
            if time.time() - timeStart > 3:
                self.motorA.run_direct(duty_cycle_sp = 0)
                break
            vol = k_p * (self.theta_goal - pos)
            vol = self.check_vol(vol)
        file.close()


    def pi_reg(self, k_p, k_i):
        vol = 100
        timeStart = time.time()
        startPos = self.motorA.position
        integral = 0
        pos = [0, 0]
        file = open('pi_reg', 'w')
        
        self.motorA.run_direct(duty_cycle_sp = vol)
        timeNow = time.time() - timeStart
        if timeNow < self.h:
            time.sleep(h - timeNow)
            timeNow = time.time() - timeStart
        pos.append(self.motorA.position - startPos)
        file.write(str(timeNow) + ',' + str(pos[-1]) + "\n")
        timeLast = timeNow

        while True:
            self.motorA.run_direct(duty_cycle_sp = vol)
            timeNow = time.time() - timeStart
            if timeNow - timeLast < self.h:
                time.sleep(h - timeNow + timeLast)
                timeNow = time.time() - timeStart
        
            pos[-2] = pos[-1]
            pos[-1] = self.motorA.position - startPos
            file.write(str(timeNow) + ',' + str(pos[-1]) + "\n")
        
            if time.time() - timeStart > 3:
                self.motorA.run_direct(duty_cycle_sp = 0)
                break

            integral += (pos[-1] + pos[-2]) * (timeNow - timeLast) / 2
            vol = k_p * (self.theta_goal - pos[-1]) + k_i * integral
            print(pos[-1])
            vol = self.check_vol(vol)
            
            timeLast = timeNow   
        file.close()

    def pd_reg(self, k_p, k_d):
        vol = 100
        timeStart = time.time()
        startPos = self.motorA.position
        integral = 0
        pos = [0, 0]
        file = open('pd_reg', 'w')
        
        self.motorA.run_direct(duty_cycle_sp = vol)
        timeNow = time.time() - timeStart
        if timeNow < self.h:
            time.sleep(h - timeNow)
            timeNow = time.time() - timeStart
        pos.append(self.motorA.position - startPos)
        file.write(str(timeNow) + ',' + str(pos[-1]) + "\n")
        timeLast = timeNow

        
        while True:
            self.motorA.run_direct(duty_cycle_sp = vol)
            timeNow = time.time() - timeStart
            if timeNow - timeLast < self.h:
                time.sleep(h - timeNow + timeLast)
                timeNow = time.time() - timeStart
            pos[-2] = pos[-1]
            pos[-1] = self.motorA.position - startPos
            file.write(str(timeNow) + ',' + str(pos[-1]) + "\n")
        
            if time.time() - timeStart > 3:
                self.motorA.run_direct(duty_cycle_sp = 0)
                break

            dif = (pos[-1] - pos[-2]) / (timeNow - timeLast)
            vol = k_p * (self.theta_goal - pos[-1]) + dif * k_d
            vol = self.check_vol(vol)
            timeLast = timeNow   
        file.close()


    def pid_reg(self, k_p, k_i, k_d):
        vol = 100
        timeStart = time.time()
        startPos = self.motorA.position
        integral = 0
        pos = [0, 0]
        file = open('pid_reg', 'w')
        
        self.motorA.run_direct(duty_cycle_sp = vol)
        timeNow = time.time() - timeStart
        if timeNow < self.h:
            time.sleep(h - timeNow)
            timeNow = time.time() - timeStart
        pos.append(self.motorA.position - startPos)
        file.write(str(timeNow) + ',' + str(pos[-1]) + "\n")
        timeLast = timeNow

        
        while True:
            self.motorA.run_direct(duty_cycle_sp = vol)
            timeNow = time.time() - timeStart
            if timeNow - timeLast < self.h:
                time.sleep(h - timeNow + timeLast)
                timeNow = time.time() - timeStart
            pos[-2] = pos[-1]
            pos[-1] = self.motorA.position - startPos
            file.write(str(timeNow) + ',' + str(pos[-1]) + "\n")
        
            if time.time() - timeStart > 3:
                self.motorA.run_direct(duty_cycle_sp = 0)
                break

            integral += (pos[-1] + pos[-2]) * (timeNow - timeLast) / 2
            dif = (pos[-1] - pos[-2]) / (timeNow - timeLast)
            vol = k_p * (self.theta_goal - pos[-1]) + k_i * integral + dif * k_d
            print(pos[-1])
            vol = self.check_vol(vol)
            timeLast = timeNow   
        file.close()

a = laba3()

k_d = 0.1
k_i = 0
k_p = 0.55
a.rele()
time.sleep(1)
a.p_reg(k_p)
time.sleep(1)
a.pi_reg(k_p, k_i)
time.sleep(1)
a.pd_reg(k_p, k_d)
k_p = 1.2
k_i = 0.001
k_d = 0.02
time.sleep(1)
a.pid_reg(k_p, k_i, k_d)