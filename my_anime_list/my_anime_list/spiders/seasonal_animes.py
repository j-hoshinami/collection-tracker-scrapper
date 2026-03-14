import time
from collections.abc import AsyncIterator
from typing import Any, AsyncIterator

import scrapy
from scrapy.http import Response

from my_anime_list.items import MyAnimeListItem


class SeasonalAnimeSpider(scrapy.Spider):
    name = "seasonal_anime"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    async def start(self) -> AsyncIterator[Any]:
        url = "https://myanimelist.net/anime/season"
        
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            callback=self.parse_seasons,
        )

    def parse_seasons(self, response: Response):
        urls = response.xpath('//div[@class="horiznav_nav"]/ul/li/a[@href]/@href').getall()

        sections_to_ignore = ["manga", "archive"]

        for url in urls:
            if any(section for section in sections_to_ignore if section in url):
                continue

            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse_anime_urls
            )

        print("*" * 50)
        print(urls)
        print("*" * 50)

    def parse_anime_urls(self, response: Response):
        urls = response.xpath('//h2[@class="h2_anime_title"]/a[@href]/@href').getall()

        urls = ['https://myanimelist.net/anime/57658/Jujutsu_Kaisen__Shimetsu_Kaiyuu_-_Zenpen']
        for url in urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse_anime_details
            )

    def parse_anime_details(self, response: Response):
        name = response.xpath('//h1[@class="title-name h1_bold_none"]/strong/text()').get()
        
        score = response.xpath('//span[@itemprop="ratingValue"]/text()').get()
        if score:
            score = float(score)

        print('URL -> ', response.url)
        print('SCORE -> ', score)
        print(f"NAME: {name} - {score}")

        episode_quant = response.xpath('//span[@class="dark_text" and contains(text(),"Episodes:")]/parent::div/text()').get()
        episode_quant = episode_quant.strip() if episode_quant else None
        # initial_date = response.xpath()
        # end_date = response.xpath()
        # available_on = response.xpath()
        # genres = response.xpath()
        # studio = response.xpath()
        # premiered = response.xpath()

        item = MyAnimeListItem()
        item["name"] = name
        item["score"] = score
        item["episode_quant"] = episode_quant
        yield item
