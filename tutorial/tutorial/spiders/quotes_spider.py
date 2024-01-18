from pathlib import Path

import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    def start_requests(self):
        urls = [
            "https://torah.nirc.edu/speakers.json",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jsonresponse = response.json()
        for speaker in jsonresponse["speakers"]:
            speaker_info = jsonresponse["speakers"][speaker]
            
            next_page = speaker_info["speaker_url"]
            if next_page is not None:
                next_page = response.urljoin(next_page).replace(".html", ".json")
    
                yield scrapy.Request(url=next_page, callback=self.parse_layer_two)
    
    def parse_layer_two(self, response):
        jsonresponse = response.json()
        
        for shiur in jsonresponse["shiurim"]["list"]:
            
            speakers = []
            for presenter in shiur["speakers"]:
                speakers.append(presenter["name"])

            with open("quotes-test.txt", 'a', encoding="utf-8") as output_file:
                output_file.write(f'Shiur Title: {shiur["title"]}  Presenter(s): {str(speakers)}\n')
            
            self.log(f"Saved file quotes-test.txt")
        
        next_page = jsonresponse["shiurim"]["next_page"]
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse_layer_two)
    