from bs4 import BeautifulSoup
import requests
import time
import io
import os
import multiprocessing

from clients.MayoclinicClient import MayoclinicClient
from clients.DrugsComClient import DrugsComClient
from scrapers.DrugsComScraper import DrugsComScraper
from scrapers.MayoclinicScraper import MayoclinicScraper
from scrapers.WebsiteScraper import WebsiteScraper

def main():
    scrapeMayoclinic = MayoclinicScraper(base_url="https://www.mayoclinic.org/", ext=["drugs-supplements", "drug-list?letter=A"])
    # mayoClinicClient = MayoclinicClient(
    #     name="Mayoclinic",
    #     base_url="https://www.mayoclinic.org/",
    #     ext=["drugs-supplements", "drug-list?letter=A"],
    #     verbose=True
    #     ).run(MayoclinicScraper)
    drugsComClient = DrugsComClient(
        name="drugs.com",
        base_url="https://www.drugs.com",
        ext="[]",
        verbose=1
    ).run(DrugsComScraper)

if __name__ == "__main__":
    main()