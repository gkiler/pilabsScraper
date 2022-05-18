import threading
import time

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

if __name__ == '__main__':
    test = threadTesting()
    test.run()