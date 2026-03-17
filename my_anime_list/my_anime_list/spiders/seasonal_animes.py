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
        url = "https://myanimelist.net/anime/season/2026/winter"
        
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            # callback=self.parse_seasons,
            callback=self.parse_anime_urls,
            meta={'dont_merge_cookies': True},
        )

    def parse_seasons(self, response: Response):
        urls = response.xpath('//div[@class="horiznav_nav"]/ul/li/a[@href]/@href').getall()

        sections_to_ignore = ["manga", "archive", "schedule", "later", "adapted", "...", "Fall 2025", "Spring 2026",
                              "Summer 2026"]

        for url in urls:
            if any(section for section in sections_to_ignore if section in url):
                continue

            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse_anime_urls,
                meta={'dont_merge_cookies': True},
            )

        print("*" * 50)
        print(urls)
        print("*" * 50)

    def parse_anime_urls(self, response: Response):
        urls = response.xpath('//h2[@class="h2_anime_title"]/a[@href]/@href').getall()

        for url in urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse_anime_details,
                meta={'dont_merge_cookies': True},
            )

    def parse_anime_details(self, response: Response):
        name = response.xpath('//h1[@class="title-name h1_bold_none"]/strong/text()').get()
        
        score = response.xpath('//span[@itemprop="ratingValue"]/text()').get()
        if score:
            score = float(score)

        episode_quant = response.xpath('//span[contains(text(),"Episodes:")]/following-sibling::text()').get()
        episode_quant = episode_quant.strip() if episode_quant else None

        initial_date = None
        end_date = None
        date = response.xpath('//span[contains(text(), "Aired:")]/following-sibling::text()').get()
        if date:
            clean_date = date.strip()
            if " to " in clean_date:
                parts = clean_date.split(" to ", 1)
                initial_date = parts[0].strip()
                end_date = parts[1].strip()
            else:
                initial_date = clean_date
                end_date = None
            
        available_on = response.xpath('//a[contains(@class, "broadcast-item")]/@title').getall()

        genres = response.xpath('//span[@itemprop="genre"]/text()').getall()

        studios = response.xpath('//span[contains(text(), "Studios:")]/../a/text()').getall()

        premiered = response.xpath('//span[contains(text(), "Premiered:")]/../a/text()').get()

        item = MyAnimeListItem()
        item["name"] = name
        item["score"] = score
        item["episode_quant"] = episode_quant
        item["initial_date"] = initial_date
        item["end_date"] = end_date
        item["available_on"] = available_on
        item["genres"] = genres
        item["studios"] = studios
        item["premiered"] = premiered
        yield item
