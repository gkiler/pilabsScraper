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
        self._ext_list = list()

        self.verboseprint = print if self._verbose else lambda x: None 

    def run(self, Scraper) -> None:
        '''Runs the client based on the user-defined methods.'''

        self.verboseprint(f"[LOG] Running {self._name} client...")

        # Parse the extension list
        self.verboseprint(f"[LOG]    - Parsing list for {self._name} client... ")
        self.parse_list()
        self.verboseprint("[LOG] (done)") 

        # Create base_url
        self.verboseprint(f"[LOG]    - Creating base_url for {self._name} client... ")
        self.create_base_url()
        self.verboseprint("(done)") 

        # Make the scraper
        self.verboseprint(f"[LOG]    - Creating scraper for {self._name} client... ")
        self.scraper = Scraper(self._base_url, self._ext_list, verbose=True)
        self.verboseprint("[LOG] (done)") 

        # Run the scraper
        self.verboseprint(f"[LOG]    - Running scraper for {self._name} client... ")
        self.scraper.run()
        self.verboseprint(f"[LOG]    - Running scraper for {self._name} client... (done)")

        # Dump into file
        self.verboseprint(f"[LOG]    - Dumping scraper output for {self._name} client... ")
        # self.dump()
        self.verboseprint("[LOG] (TBD)") 

        # Print regardless of verbosity
        print(f"[LOG] Done running {self._name}.\n")

    def parse_list(self) -> None:
        '''user-defined method to control how to parse the typically-found ordered list for any type of object on any type of website.'''
        # self.verboseprint("ERROR: calling abstract class WebsiteClient::parse_list()")
        pass

    def create_base_url(self) -> None:
        '''user-defined method to control how to create the base_url member passed onto WebsiteController for any website.'''
        # self.verboseprint("ERROR: calling abstract class WebsiteClient::create_base_url()") 
        pass