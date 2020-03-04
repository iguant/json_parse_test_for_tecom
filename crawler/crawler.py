import json

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from googleapiclient.discovery import build


class Crawler:
    def __init__(self, search_string: str, p_count: str, api_key: str, cse_id: str):
        self.search_string = search_string
        self.p_count = p_count
        self.api_key = api_key
        self.cse_id = cse_id
        self.result = []

    def _prepare_http_adapter(self, url):
        with requests.Session() as session:
            session.mount(url, HTTPAdapter())
        return session

    def request_url(func):
        def wrapper(self, **kwargs):
            session = kwargs.get("session")
            url = kwargs.get("url")
            headers = {
                'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.'}
            server_response = session.get(url, headers=headers)
            return func(data=server_response.text)

        return wrapper

    @request_url
    def _get_html(**kwargs):
        data = kwargs.get("data")
        return BeautifulSoup(data, "html.parser")

    def _google_search(self, **kwargs):
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=self.search_string, num=self.p_count, cx=self.cse_id, **kwargs).execute()
        return res

    def _parse_html(self, html):
        pass









    def process(self) -> list:
        search_results = self._google_search()
        for item in search_results["items"]:
            url = item["link"]
            session = self._prepare_http_adapter(url)
            html = self._get_html(session=session, url=url)
            self.result.append((item["title"], self._parse_html(html=html)))
        return self.result


