#coding: utf-8

class GP(object) :
    OUT = 0
    def __init__(self, no = 0) :
        self.no = no
    def setup(self, no, noType) :
        print 'setup', no, noType
    def PWM(self, no, hz) :
        print 'pwm', no, hz
        return GP(no)
    def start(self, speed) :
        print 'start', self.no, speed
    def stop(self) :
        print 'stop', self.no
    def ChangeDutyCycle(self, speed) :
        print 'change', self.no, speed

GPIO = GP()


