import threading
import time

from threading import Thread

class threadTesting:

    def __init__(self):
        self.exampleText = 'thread end test'
        self.exampleOtherText = 'testing thread'

    def scrapeExample(self):
        print(self.exampleOtherText)
        time.sleep(3)
        print(self.exampleText)

    def otherExample(self):
        print('Other thread')
        time.sleep(1)
        print('other thread finished')

    def run(self):
        t1 = threading.Thread(target=self.scrapeExample)
        t2 = threading.Thread(target=self.otherExample)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

class MayoThreadTest(Thread):
    def run(self):
        print("MayoThreadTest Start")
        time.sleep(2)
        print("MayoThreadTest End")

class WebMDThreadTest(Thread):
    def run(self):
        print("WebMDThreadTest Start")
        time.sleep(2)
        print("WebMDThreadTest End")

class DrugsThreadTest(Thread):
    def run(self):
        print("DrugsThreadTest Start")
        time.sleep(2)
        print("DrugsThreadTest End")

class WikiThreadTest(Thread):
    def run(self):
        print("WikiThreadTest Start")
        time.sleep(2)
        print("WikiThreadTest End")

if __name__ == '__main__':
    threads = [MayoThreadTest, WebMDThreadTest, DrugsThreadTest, WikiThreadTest]

    for i in range(4):
        t = threads[i]()
        t.start()

    # test = threadTesting()
    # test.run()