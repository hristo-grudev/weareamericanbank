import scrapy

from scrapy.loader import ItemLoader

from ..items import WeareamericanbankItem
from itemloaders.processors import TakeFirst


class WeareamericanbankSpider(scrapy.Spider):
	name = 'weareamericanbank'
	start_urls = ['https://www.weareamerican.bank/news']

	def parse(self, response):
		post_links = response.xpath('//div[@class="interior-main with-sidebar"]/div[@class="content"]')
		for post in post_links:

			title = post.xpath('.//h1//text()').get()
			description = post.xpath('.//p[position()>1]//text()[normalize-space()]').getall()
			description = [p.strip() for p in description if '{' not in p]
			description = ' '.join(description).strip()
			date = post.xpath('.//p/strong/text()').get()

			item = ItemLoader(item=WeareamericanbankItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
