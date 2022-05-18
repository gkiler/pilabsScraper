from clients.WebsiteClient import WebsiteClient

class MayoclinicClient(WebsiteClient):
    def parse_list(self) -> None:
        pass

    def create_base_url(self) -> None:
        self._base_url = self._base_url + "/".join(self._ext)
        pass