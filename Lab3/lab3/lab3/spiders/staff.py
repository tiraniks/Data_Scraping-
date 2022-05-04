import scrapy
from lab3.items import FacultyItem, DepartmentItem

class StaffSpider(scrapy.Spider):
    name = "staff"
    BASE_URL = "https://kubg.edu.ua/"
    start_urls = ["https://kubg.edu.ua/структура/instytuty-ta-fakultety"]

    def parse(self, response):
        for a in response.css(".item-795 deeper parent li a"):
            url =f"{self.BASE_URL}{a.css('::attr(href)').get()}"
            res = FacultyItem(
                url=url,
                name=a.css("a::text").get()
            )
            yield res
            yield scrapy.Request(
                url=url,
                callback=self.parse_dep,
                meta={
                    "faculty": res["name"]
                }
            )

    def parse_dep(self, response):
        for div in response.css(".spEntriesListTitle div"):
            url =f"{self.BASE_URL}{div.css('::attr(href)').get()}"
            res = DepartmentItem(
                url=url,
                name=div.css("a::text").get(),
                faculty=response.meta["faculty"]
            )
            yield res