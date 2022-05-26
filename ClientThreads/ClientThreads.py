from threading import Thread

# Scrapers
from scrapers.DrugsComScraper import DrugsComScraper
from scrapers.MayoclinicScraper import MayoclinicScraper
from scrapers.MedlineScraper import MedlineScraper
from scrapers.WebMDScraper import WebMDScraper

# Clients
from clients.WebsiteClient import WebsiteClient

class MayoClinicThread(Thread):
    def run(self):
        print("[START] MayoClinicClient")
        mayoClinicClient = WebsiteClient(
            name="Mayoclinic",
            base_url="https://www.mayoclinic.org/",
            ext=["", "drugs-supplements", "drug-list?letter=A"],
            verbose=False
        ).run(MayoclinicScraper)
        print("[END] MayoClinicClient")

class DrugsComThread(Thread):
    def run(self):
        print("[START] DrugsComClient")
        drugsComClient = WebsiteClient(
            name="drugs.com",
            base_url="https://www.drugs.com",
            ext=["", "drug_information.html"],
            verbose=False
        ).run(DrugsComScraper)
        print("[END] DrugsComClient")

class MedlineThread(Thread):
    def run(self):
        print("[START] MedlineThread")
        medlineClient = WebsiteClient(
            name="medline",
            base_url="https://medlineplus.gov",
            ext=[""],
            verbose=False
        ).run(MedlineScraper)
        print("[END] MedlineClient")

class WebMDThread(Thread):
    def run(self):
        print("[START] WebMDThread")
        webMDClient = WebsiteClient(
            name="webmd",
            base_url="https://www.webmd.com",
            ext=[""],
            verbose=False
        ).run(WebMDScraper)

# class WikiThread(Thread):
#     def run(self):
#         print("[START] Redundant Thread")
#         print("[END] Redundant Thread")

'''
Read below to add your own thread for your website scraper. Each one of these declarations will result in an additional website
being added to a thread and being scraped.

In order to RUN your own WebsiteThread class, you need to add the name of the class into the `THREADS` variable in ~/main.py.

Please read the README.md file for more information.
'''
# # Choose your scraper for Website
# from scrapers.WebsiteScraper import WebsiteScraper

# class WebsiteThread(Thread):
#     def run(self):
#         print("[START] WebsiteClient")
#         websiteClient = WebsiteClient(
#             name="website.com",
#             base_url="",
#             ext=["", "some_extension1", "some_extension2"],
#             verbose=False
#         ).run(WebsiteScraper)
#         print("[END] WebsiteClient")