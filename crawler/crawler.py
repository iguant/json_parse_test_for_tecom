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

    def _parce_json(self, json_data):
        result = {}

        def nested_recurse_json(piece: dict):
            for key in piece:
                if type(piece[key]) is str:
                    result[key] = piece[key]
                if type(piece[key]) is dict:
                    nested_recurse_json(piece[key])

        nested_recurse_json(json_data)
        return result

    def _parse_html(self, html):
        result_json = {}
        found = 0

        def nested_recurse_text(piece_text: str, found):
            open_bracket = piece_text.find('{')
            substring = piece_text[open_bracket:]
            pointer = 1
            for char in range(1, len(substring)):
                if substring[char] is "{":
                    pointer += 1
                if substring[char] is "}":
                    pointer -= 1
                if pointer is 0:
                    found += 1
                    try:
                        pre_json = json.loads(substring[:char + 1])
                        print("Loaded JSON")
                        parsed_json = self._parce_json(json_data=pre_json)
                        json_object = f"object_{found}"
                        result_json[json_object] = parsed_json
                    except:
                        print("Cannot load JSON")
                    if len(substring[char:]) > 1:
                        nested_recurse_text(substring[char:], found)
                    break
        nested_recurse_text(html.text, found)
        return result_json

    def process(self) -> list:
        search_results = self._google_search()
        for item in search_results["items"]:
            url = item["link"]
            print(item["link"])
            session = self._prepare_http_adapter(url)
            html = self._get_html(session=session, url=url)
            content = self._parse_html(html=html)
            if len(content) != 0:
                self.result.append((item["title"], content))
        return self.result
