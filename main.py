from bs4 import BeautifulSoup
import requests
import io
import os
import multiprocessing

from clients.MayoclinicClient import MayoclinicClient
from clients.DrugsComClient import DrugsComClient
from scrapers.DrugsComScraper import DrugsComScraper
from scrapers.MayoclinicScraper import MayoclinicScraper
from scrapers.WebsiteScraper import WebsiteScraper

from ClientThreads.ClientThreads import *

from time import sleep

THREADS = [DrugsComThread]

def main():
    # Runs every thread at the same time. Might want to wait a bit to run them
    for i in range(len(THREADS)):
        t = THREADS[i]()
        t.start()

if __name__ == "__main__":
    main()