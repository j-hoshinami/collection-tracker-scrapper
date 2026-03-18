from collections.abc import AsyncIterator
from typing import Any, AsyncIterator

import scrapy
from scrapy.http import Response

from my_anime_list.items import MyAnimeListItem


class SeasonalAnimeSpider(scrapy.Spider):
    name = "seasonal_anime"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'cookie': 'MALSESSIONID=388843f53307e3e57d99c09594e860e6; usprivacy=1---; euconsent-v2=CQhG6EAQhG6EAAKA9AENCWFsAP_gAEPgABJ4MKtR_G__bWlr-bb3abtkeYxP9_hr7sQxBgbJk24FzLPW7JwHx2E5NAzatqIKmRIAu3TBIQNlHJDURUCgKIgFryDMaE2U4TNKJ6BkiFMZA2tYCFxvm4tjWQCY4vr_5lc1mB-t7dr82dzyy6hHn3a5fmS1UJCdIYetDfv8ZBOT-9IEd-x8v4v4_EbpEm-eS1n_pGtp4jd6YnM_dBmxt-Tyff7Pn__rl_e7X_ve_n3zv8oXH77v____f_-7___2b_-___b-_-DCQAJhoVEEZZECAQKAhBAgAUFYQAUCAIAAEgaICAEwYEOQMAF1hMgBACgAGCAEAAIMAAQAACQAIRABAAQCAECAQKAAMACAICABgYAAwAWIgEAAIDoGKYEEAgWACRGVQaYEoACQQEtlQglAwIK4QhFjgEECImCgAABAAKAABAfCwEJJQSsSCALiC6AAAgAACiBEgRSFmAIKgzRaCsCTgMjTAMHzBMkp0GQBMEJGQZEJqgmHimKIUEOQGxSzAHTxBQAi7WSEAAAA.IAAA.YAAAAAAAAAAA; IABGPP_HDR_GppString=DBABMA~CQhG6EAQhG6EAAKA9AENCWFsAP_gAEPgABJ4MKtR_G__bWlr-bb3abtkeYxP9_hr7sQxBgbJk24FzLPW7JwHx2E5NAzatqIKmRIAu3TBIQNlHJDURUCgKIgFryDMaE2U4TNKJ6BkiFMZA2tYCFxvm4tjWQCY4vr_5lc1mB-t7dr82dzyy6hHn3a5fmS1UJCdIYetDfv8ZBOT-9IEd-x8v4v4_EbpEm-eS1n_pGtp4jd6YnM_dBmxt-Tyff7Pn__rl_e7X_ve_n3zv8oXH77v____f_-7___2b_-___b-_-DCQAJhoVEEZZECAQKAhBAgAUFYQAUCAIAAEgaICAEwYEOQMAF1hMgBACgAGCAEAAIMAAQAACQAIRABAAQCAECAQKAAMACAICABgYAAwAWIgEAAIDoGKYEEAgWACRGVQaYEoACQQEtlQglAwIK4QhFjgEECImCgAABAAKAABAfCwEJJQSsSCALiC6AAAgAACiBEgRSFmAIKgzRaCsCTgMjTAMHzBMkp0GQBMEJGQZEJqgmHimKIUEOQGxSzAHTxBQAi7WSEAAAA.IAAA.YAAAAAAAAAAA; MALHLOGSESSID=a7e53454d61c8cddc4e783981f5b0e32; _sharedid=77d09c3a-f1ce-4f2d-8f62-c8dda30eeda3; _sharedid_cst=VCztLKosYA%3D%3D; aws-waf-token=4508347c-4ec3-423e-82e7-ed121aa3cc3b:FAoAdP4Pu9A/AAAA:/uyqjzhO3mMGnaqswZmrgmM0LNxOeqeExXIWACEEKxmerP0xcOykN/tYxvkIwIqVZ5xEWica0a33aZYKNkvx+HE49Tx5tukNk3F2RKfWuLUPIQ9WOleH8PYtwj0RmZa4uRHml71Ekas/Yrfc6Rve3iNUdGPfh8/TLBwAMepmdg1Py4EmnCHhN1Pj+u+g+PqGtBpQNjeSEO4EDNoRfpSvhZIIXXOsCE5azy+3xLDTJ5AWINGFkx5ol2hed6rGSRkeJw==; _gcl_au=1.1.862520486.1773628113; _ga=GA1.1.2028159841.1773628113; _rdt_uuid=1773628112858.771abf26-c5bc-4014-bc86-6ce277b7f254; _ga_26FEP9527K=GS2.1.s1773718354$o2$g1$t1773720451$j48$l0$h0; cto_bundle=Bkye6l81YXBwSVNyUiUyRmo2NUR1eWI0cyUyRkpVaFhJTDFFMWVGJTJGQUhoaWpNU2xWa3hQam1lJTJGMFRiemVBWkxZZEN3djk0eVAlMkJuNHBOZ1hEUEhSeEJhdm9NVm96blp6MGVoTlFLbElyZFZkTEZPc1V6MzlCaiUyQnFIRHpZdU84SUhJQWJNMTV4NEFyRGFBc1NQJTJCR0V4S2VTSGFYTG04USUzRCUzRA; cto_bidid=ycgmq19wYzBhdXdVc2pZQ3prZ0pMQmYyamhPeVhNcW5iUHklMkZsSDVTeCUyQjlvZmlBaTRsSWtZSnRUcGpzS2RCQmYxQTNxJTJGWEUzWllJTlNRS2xkY2x6ZWJzJTJGN280dkJnNUVsZW9KOEttMWRoWE50VGIlMkZ6Y0cybnoxUGklMkZRME9rUVU3NWZOUQ',
    }
    
    async def start(self) -> AsyncIterator[Any]:
        url = "https://myanimelist.net/anime/season/2026/winter"
        
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            callback=self.parse_seasons,
            meta={'dont_merge_cookies': True},
        )

    def parse_seasons(self, response: Response):
        urls = response.xpath('//div[@class="horiznav_nav"]/ul/li/a[@href]/@href').getall()

        for url in urls:
            if not '2026' in url:
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
        cards = response.xpath('//div[@class="title"]')

        urls = []
        for card in cards:
            name = card.xpath('.//h2/a/text()').get()

            img_src = card.xpath('./../../div[@class="image"]//img/@src').get()
            available = img_src is not None

            print(f'NAME: {name} - AVAILABLE {available}')

            if not name:
                continue

            if available:
                url = card.xpath('.//h2/a/@href').get()
                if url:
                    urls.append(url)

        for url in urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                dont_filter=True,
                callback=self.parse_anime_details,
                meta={
                    'dont_merge_cookies': True,
                    'origin_url': response.url
                },
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
        if 'add some' in studios:
            studios = []

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
        item["origin_url"] = response.meta.get('origin_url')
        yield item
