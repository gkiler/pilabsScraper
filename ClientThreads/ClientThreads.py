from threading import Thread
from time import time

from clients.MayoclinicClient import MayoclinicClient
from clients.DrugsComClient import DrugsComClient
from scrapers.DrugsComScraper import DrugsComScraper
from scrapers.MayoclinicScraper import MayoclinicScraper
from scrapers.WebsiteScraper import WebsiteScraper

class MayoClinicThread(Thread):
    def run(self):
        print("[START] MayoClinicClient")
        mayoClinicClient = MayoclinicClient(
            name="Mayoclinic",
            base_url="https://www.mayoclinic.org/",
            ext=["", "drugs-supplements", "drug-list?letter=A"],
            verbose=False
        ).run(MayoclinicScraper)
        print("[END] MayoClinicClient")

class WebMDThreadTest(Thread):
    def run(self):
        print("[START] Redundant Thread")
        print("[END] Redundant Thread")
        pass

class DrugsComThread(Thread):
    def run(self):
        print("[START] DrugsComClient")
        drugsComClient = DrugsComClient(
            name="drugs.com",
            base_url="https://www.drugs.com",
            ext=["", "drug_information.html"],
            verbose=False
        ).run(DrugsComScraper)
        print("[START] DrugsComClient")

class WikiThreadTest(Thread):
    def run(self):
        print("[START] Redundant Thread")
        print("[END] Redundant Thread")
        pass