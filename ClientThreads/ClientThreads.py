from re import S
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
from scrapers.RareDiseaseScraper import RareDiseaseScraper
from scrapers.RIDHScraper import RIDHScraper 
from scrapers.HealthlineDrugsScraper import HealthlineDrugsScraper
from scrapers.IllinoisScraper import IllinoisScraper
from scrapers.MedlineDiseaseScraper import MedlineDiseaseScraper
from scrapers.DBpediaScraper import DBpediaScraper
from scrapers.RxlistScraper import RxlistScraper
from scrapers.HonDossierScraper import HonDossierScraper
# from scrapers.HealthlineDrugsScraper import HealthlineDrugsScraper

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

class RareDiseaseThread(Thread):
    def run(self):
        print("[START] RareDiseaseThread")
        RareDiseaseClient = WebsiteClient(
            name="Rare Disease",
            base_url="https://rarediseases.org",
            ext=[""],
            verbose=False
        ).run(RareDiseaseScraper)

class RIDHThread(Thread):
    def run(self):
        print("[START] RIDHThread")
        RIDHClient = WebsiteClient(
            name="RIDH",
            base_url="https://health.ri.gov",
            ext=[""],
            verbose=False
        ).run(RIDHScraper) 

class RxlistThread(Thread):
    def run(self):
        print("[START] RxlistThread")
        RIDHClient = WebsiteClient(
            name="Rxlist",
            base_url="https://www.rxlist.com",
            ext=[""],
            verbose=False
        ).run(RxlistScraper)

class HonDossierThread(Thread):
    def run(self):
        print("[START] HonDossierThread")
        HonDossierClient = WebsiteClient(
            name="Hon Dossier",
            base_url="https://www.hon.ch/Dossier/110_HONDossier.htm",
            ext=[""],
            verbose=False
        ).run(HonDossierScraper)
        
class HealthlineDrugsThread(Thread):
    def run(self):
        print("[START] HealthlineDrugsThread")
        HealthlineDrugsClient = WebsiteClient(
            name="Healthline(Drugs)",
            base_url="https://www.healthline.com",
            ext=[""],
            verbose=False
        ).run(HealthlineDrugsScraper)

class IllinoisThread(Thread):
    def run(self):
        print("[START] IllinoisThread")
        IllinoisClient = WebsiteClient(
            name="IDPH",
            base_url="https://dph.illinois.gov",
            ext=[""],
            verbose=False
        ).run(IllinoisScraper)
        print("[END] IllinoisClient")

class MedlineDiseaseThread(Thread):
    def run(self):
        print("[START] Medline Disease")
        MedlineDClient = WebsiteClient(
            name="Medline Plus Encyclopedia",
            base_url="https://medlineplus.gov/ency/",
            ext=[""],
            verbose=False
        ).run(MedlineDiseaseScraper)
        print("[END] MedlineDClient")        

class DBpediaThread(Thread):
    def run(self):
        print("[START] DBpediaThread")
        DBpediaClient = WebsiteClient(
            name="DBpedia",
            base_url="https://dbpedia.org/",
            ext=[""],
            verbose=False
        ).run(DBpediaScraper)

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