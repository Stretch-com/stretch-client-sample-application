class WebClient:
    def __init__(self):
        self.base_url = f"http://0.0.0.0:8000/api/v1/public"

    def get(self, url, params):
        url = f"{self.base_url}/{url}"

    def post(self, url, params, body):
        self.base_url