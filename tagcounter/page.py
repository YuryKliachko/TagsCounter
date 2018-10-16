class Page:
    def __init__(self, url):
        import requests
        self.url = url.strip()
        try:
            self.page = requests.get(self.url)
            self.status_code = self.page.status_code
        except requests.ConnectionError:
            self.status_code = None

    def get_data(self):
        data = self.page.text
        return data