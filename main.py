from ClientThreads.ClientThreads import *
from pathvalidate import sanitize_filename #not native


THREADS = [NHSScottishThread]  #, MedlineThread,WebMDThread,DrugsComThread, MayoClinicThread, CDCThread, 

def main():
    # Runs every thread at the same time. Might want to wait a bit to run them
    for i in range(len(THREADS)):
        t = THREADS[i]()
        t.start()

if __name__ == "__main__":
    main()