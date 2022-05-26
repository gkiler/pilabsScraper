from ClientThreads.ClientThreads import *

THREADS = [DrugsComThread, MayoClinicThread, MedlineThread, WebMDThread]

def main():
    # Runs every thread at the same time. Might want to wait a bit to run them
    for i in range(len(THREADS)):
        t = THREADS[i]()
        t.start()

if __name__ == "__main__":
    main()