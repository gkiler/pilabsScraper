import sys
sys.path.append("./..")

from scrapers.WebsiteScraper import WebsiteScraper

class WebsiteClient:
    def __init__(self, name="NONAME", base_url=None, ext=list(), verbose=True) -> None:
        '''
        * Controls how the specified website scraping will happen. \n
        base_url: url for the base website \n
        ext: list of extensions to the base url \n

        user-defined methods
        - self.parse_list(self) -> None
        - self.create_base_url(self) -> None
        '''
        self._verbose = verbose
        self._name = name
        self._base_url = base_url
        self._ext = ext

        self.verboseprint = print if self._verbose else lambda x: None 

    def run(self, Scraper) -> None:
        '''Runs the client based on the user-defined methods.'''

        self.verboseprint(f"[LOG] Running {self._name} client...")

        # Make the scraper
        self.verboseprint(f"[LOG]    - Creating scraper for {self._name} client... ")
        self.scraper = Scraper(
            base_url=self._base_url,
            ext=self._ext,
            verbose=True)
        self.verboseprint("[LOG] (done)")

        # Run the scraper
        self.verboseprint(f"[LOG]    - Running scraper for {self._name} client... ")
        self.scraper.run()
        self.verboseprint(f"[LOG]    - Running scraper for {self._name} client... (done)")

        # Print regardless of verbosity
        print(f"[LOG] Done running {self._name}.\n")