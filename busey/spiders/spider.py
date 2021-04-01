import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BuseyItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class BuseySpider(scrapy.Spider):
	name = 'busey'
	start_urls = ['https://www.busey.com/about-us/news-and-announcements']

	def parse(self, response):
		post_links = response.xpath('//a[@data-link-type-id="page"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = "Not stated in article"
		title = response.xpath('//h1/text()').get()
		content = response.xpath('(//div[@class="col-md-10 offset-md-1"])[1]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=BuseyItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
