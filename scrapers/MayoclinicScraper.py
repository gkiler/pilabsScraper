from scrapers.WebsiteScraper import WebsiteScraper

class MayoclinicScraper(WebsiteScraper):
    def scrape(self):
        # Querying
        self.verboseprint(f"            - querying \"{self._query_url}\"... ", end="")
        # query TBD

        # Done querying
        self.verboseprint("(done)")
        pass