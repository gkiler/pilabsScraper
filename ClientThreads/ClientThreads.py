from threading import Thread

# Scrapers
from scrapers.DrugsComScraper import DrugsComScraper
from scrapers.MayoclinicScraper import MayoclinicScraper
from scrapers.MedlineScraper import MedlineScraper
from scrapers.WebMDScraper import WebMDScraper
from scrapers.CDCScraper import CDCScraper
from scrapers.NHSScottishScraper import NHSScottishScraper
from scrapers.FamilyDoctorScraper import FamilyDoctorScraper
from scrapers.ECDCScraper import ECDCScraper

# Clients
from clients.WebsiteClient import WebsiteClient

class NHSScottishThread(Thread):
    def run(self):
        print("[START] NHSClient")
        nhsClient = WebsiteClient(
            name="NHS",
            base_url="https://www.nhsinform.scot",
            ext=[""],
            verbose = False
        ).run(NHSScottishScraper)
        print("[END] NHSClient")

class CDCThread(Thread):
    def run(self):
        print("[START] CDCClient")
        cdcClient = WebsiteClient(
            name="CDC",
            base_url="https://www.cdc.gov",
            ext=[""],
            verbose=False
        ).run(CDCScraper)
        print("[END] CDCClient")

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

class FamilyDoctorThread(Thread):
    def run(self):
        print("[START] FamilyDoctorThread")
        familyDoctorClient = WebsiteClient(
            name="Family Doctor",
            base_url="https://familydoctor.org/",
            ext=[""],
            verbose=False
        ).run(FamilyDoctorScraper)

class ECDCThread(Thread):
    def run(self):
        print("[START] ECDCThread")
        ECDCClient = WebsiteClient(
            name="ECDC",
            base_url="https://www.ecdc.europa.eu/en",
            ext=[""],
            verbose=False
        ).run(ECDCScraper)

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