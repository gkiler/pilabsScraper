import string


class WebsiteScraper:
    def __init__(self, base_url=None, ext=list(), verbose=False):
        '''
        * Initializes the WebsiteScraper. \n
        base_url: url for the base website\n
        ext: list of extensions to the base url\n
        '''
        self._verbose = verbose
        self._base_url = base_url
        self._ext = ext
        self._query_url = self._base_url + "/".join(self._ext)

        self.verboseprint = print if self._verbose else lambda x: None

    def scrape(self) -> string:
        # Querying
        self.verboseprint(f"            - querying \"{self._query_url}\"... ")
        # query TBD

        # Done querying
        self.verboseprint("(done)")
        pass

    def run(self) -> None:
        '''Runs the scraper based on the user-defined methods'''

        self.verboseprint("         Scraping...")
        self.scrape()