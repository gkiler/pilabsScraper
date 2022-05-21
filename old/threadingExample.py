import threading
import time
import logging
import sys
import random

random.seed(time.localtime)

def func1():
    print('Start task 1\n')
    time.sleep(random.randint(2,10))
    print('Done task 1')

def func2():
    print('Start task 2\n')
    time.sleep(random.randint(2,10))
    print('Done task 2')

def func3():
    print('Start task 3\n')
    time.sleep(random.randint(2,10))
    print('Done task 3')

def func4():
    print('Start task 4\n')
    time.sleep(random.randint(2,10))
    print('Done task 4')


root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

threads = list() #list threads
print('startExec\n')
tempThread = threading.Thread(target=func1) #create instance of thread
threads.append(tempThread) #add thread to list of threads 
tempThread.start() #start individual thread
#overwrite and so on
tempThread = threading.Thread(target=func2)
threads.append(tempThread)
tempThread.start()

tempThread = threading.Thread(target=func3)
threads.append(tempThread)
tempThread.start()

tempThread = threading.Thread(target=func4)
threads.append(tempThread)
tempThread.start()

for index, thread in enumerate(threads):
    logging.info("Before join thread %d",index)
    thread.join()
    logging.info("After thread %d done",index)
