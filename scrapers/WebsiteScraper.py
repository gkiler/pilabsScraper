
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
        self._headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}

        self.verboseprint = print if self._verbose else lambda x: None
    
    def parse():
        '''User-defined parse function to get through the website specifically'''
        pass

    def run(self) -> None:
        '''
        Calls the scrape method
        '''
        self.scrape()