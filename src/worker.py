import json
import xml.etree.ElementTree as ET
from typing import List
from urllib.parse import urlparse, urljoin, urlencode

from js import fetch, Headers, Response


BASE_RSS_URL = "https://hnrss.org"


async def on_fetch(request, env):
    # Parse the incoming request URL
    url_parts = urlparse(request.url)

    url = BASE_RSS_URL + url_parts.path + "?" + url_parts.query

    resp = await fetch(url, method="GET")
    body = await resp.text()

    if resp.status != 200 or "xml" not in resp.headers.get("content-type", ""):
        return Response.new(body, status=resp.status, headers=resp.headers)

    # 解析rss类容并翻译标题
    translator = RssTranslator(
        env.TRANSLATE_API_KEY,
        env.TRANSLATE_API_REGION,
        env.TRANSLATE_LANGUAGE,
    )
    content = await translator.translate(body)

    headers = Headers.new({"content-type": resp.headers["content-type"]}.items())
    return Response.new(content, headers=headers)


class RssTranslator:
    endpoint = "https://api.cognitive.microsofttranslator.com/translate"

    def __init__(
        self, translate_api_key: str, translate_api_region: str, to_language: str
    ):
        self.translate_api_key = translate_api_key
        self.translate_api_region = translate_api_region
        self.to_language = to_language

    async def translate(self, text: str) -> str:
        root = ET.fromstring(text)

        titles = []
        for item in root.iter("item"):
            title_element = item.find("title")
            if title_element is not None:
                titles.append(title_element.text)

        # 翻译标题
        translate_titles = await self.translate_titles(titles)

        for item in root.iter("item"):
            title_element = item.find("title")
            if title_element is not None:
                title_element.text = translate_titles.pop(0)

        return ET.tostring(root, encoding="unicode")

    async def translate_titles(self, titles: List[str]) -> List[str]:
        headers = {
            "Ocp-Apim-Subscription-Key": self.translate_api_key,
            "Ocp-Apim-Subscription-Region": self.translate_api_region,
            "Content-type": "application/json",
        }
        params = {"api-version": "3.0", "from": "en", "to": self.to_language}
        body = [{"text": title} for title in titles]

        response = await fetch(
            urljoin(self.endpoint, "?" + urlencode(params)),
            method="POST",
            body=json.dumps(body),
            headers=Headers.new(headers.items()),
        )

        if response.status != 200:
            return titles

        content = await response.text()
        return [item["translations"][0]["text"] for item in json.loads(content)]
