# -*- coding: utf-8 -*-
import thread

__author__ = 'jeong-yonghan'

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, mydelay, count):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.mydelay = mydelay
        self.count = count
    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.mydelay, self.count)
        print "Exiting " + self.name

def print_time(threadName, delay, counter):
    for i in range(3):
        time.sleep(delay)
        print  i, "hello"


# Create new threads
thread1 = myThread(1, "Thread-1", 0.1,3)
thread2 = myThread(2, "Thread-2", 0.3,3)

# Start new Threads
thread1.start()
thread2.start()

