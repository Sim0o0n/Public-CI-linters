from threading import Semaphore, Thread
import time
import sys

sem: Semaphore = Semaphore()
running = True

def fun1():
    while running:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)

def fun2():
    while running:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)

t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)

try:
    t1.start()
    t2.start()
except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    running = False
    t1.join()
    t2.join()
    print('Threads have been successfully terminated.')
    sys.exit(0)

