#coding:utf-8

from threading import Thread, Condition, Lock

class Timer(Thread) :
    def __init__(self, func, args = [], kwargs = {}) :
        Thread.__init__(self)
        self.__cond = Condition(Lock())
        self.runFlag = True
        self.newInterval = 0
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.runFunc = False

    def reset(self, interval) :
        self.__cond.acquire()
        try :
            self.newInterval = interval
            self.runFunc = True
            self.__cond.notify_all()
        finally :
            self.__cond.release()
    
    def run(self) :
        self.__cond.acquire()
        try :
            while self.runFlag:
                if self.newInterval == 0 :
                    timeout = 100
                else :
                    timeout = self.newInterval
                    self.newInterval = 0
                
                self.__cond.wait(timeout)

                if self.runFunc and self.newInterval == 0 :
                    self.runFunc = False
                    self.func(*self.args, **self.kwargs)
        finally :
            self.__cond.release()
            
    def cancel(self) :
        self.__cond.acquire()
        try :
            self.runFunc = False
            self.__cond.notify_all()
        finally :
            self.__cond.release()

    def exit(self) :
        self.__cond.acquire()
        try :
            self.runFlag = False
            self.runFunc = False
            self.__cond.notify_all()
        finally :
            self.__cond.release()
