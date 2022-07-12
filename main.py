from ClientThreads.ClientThreads import *
from pathvalidate import sanitize_filename #not native

# going to add ECDCThread once I'm done
THREADS = [ECDCThread]  #FamilyDoctorThread, MedlineThread, WebMDThread, DrugsComThread, MayoClinicThread, CDCThread, NHSScottishThread

def main():
    # Runs every thread at the same time. Might want to wait a bit to run them
    for i in range(len(THREADS)):
        t = THREADS[i]()
        t.start()

if __name__ == "__main__":
    main()