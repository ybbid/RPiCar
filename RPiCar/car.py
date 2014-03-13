#coding:utf-8

import RPi.GPIO as gp
from timer import Timer
import math
PWM_HZ = 2000

class Wheel(object) :
    def __init__(self, fPin, bPin):
        self.fPin = fPin
        self.bPin = bPin
        self.revise = 0

        gp.setup(self.fPin, gp.OUT)
        gp.setup(self.bPin, gp.OUT)
        self.fp = gp.PWM(self.fPin, PWM_HZ)
        self.bp = gp.PWM(self.bPin, PWM_HZ)
        self.speed = 0
        self.isRun = 0

    def setRevise(self, revise) :
        self.revise = revise

    def run(self, speed) :
        if speed < 0 :
            front = False
            speed = -speed
        else :
            front = True

        speed -= self.revise
        if speed < 0 :
            speed = 0

        if speed == 0 :
            self.speed = 0
            if self.isRun == 1 :
                self.fp.stop()
                self.isRun = 0
            elif self.isRun == -1 :
                self.bp.stop()
                self.isRun = 0
            return

        if speed > 7 : 
            speed = 7
        speed = speed * 10 + 30
        
        if self.isRun == 0 :
            if front :
                self.fp.start(speed)
                self.isRun = 1
            else :
                self.bp.start(speed)
                self.isRun = -1
        elif self.isRun == 1 :
            if front :
                if self.speed != speed :
                    self.fp.ChangeDutyCycle(speed)
            else :
                self.fp.stop()
                self.bp.start(speed)
                self.isRun = -1
        else :
            if front :
                self.fp.start(speed)
                self.bp.stop()
                self.isRun = 1
            else :
                if self.speed != speed :
                    self.bp.ChangeDutyCycle(speed)
        self.speed = speed

    def stop(self) :
        if isRun == 1 :
            self.fp.stop()
        elif isRun == -1 :
            self.bp.stop()

class Car(object) :
    def __init__(self, gpMode = gp.BOARD) :
        gp.setmode(gpMode)

    INSTANCE = None
    @staticmethod
    def getCar() :
        if Car.INSTANCE == None :
            Car.INSTANCE = Car()
            Car.INSTANCE.initWhell(11, 12, 13, 15)
        return Car.INSTANCE

    def initWhell(lfPin, lbPin, rfPin, rbPin) :
        self.lWheel = Wheel(lfPin, lbPin)
        self.lWhell.setRevise(0.1)
        self.rWheel = Wheel(rfPin, rbPin)
        self.timer = Timer(self.stop)
        self.timer.start()

    def run(self, lSpeed, rSpeed, duration = 0) :
        self.lWheel.run(lSpeed)
        self.rWheel.run(rSpeed)
        if duration != 0 :
            self.timer.reset(duration / 1000)

    def run2(self, x, y, duration = 0) :
        base = math.sqrt(x*x + y*y)
        lSpeed = 0
        rSpeed = 0
        d = math.degrees(math.atan2(y, x))
        if x >= 0 and y >= 0 :
            lSpeed = base
            rSpeed = base * (d - 45) / 45
        elif x >= 0 and y < 0 :
            lSpeed = base * (d + 45) / 45
            rSpeed = -base
        elif x < 0 and y >= 0 :
            lSpeed = base * (135 - d) / 45
            rSpeed = base
        elif x < 0 and y < 0 :
            lSpeed = -base
            rSpeed = base * (-d - 135) / 45
        lSpeed = int(lSpeed)
        rSpeed = int(rSpeed)
        self.run(lSpeed, rSpeed, duration)

    def stop(self) :
        self.lWheel.stop()
        self.rWheel.stop()

    def close(self) :
        self.stop()
        self.timer.exit()

