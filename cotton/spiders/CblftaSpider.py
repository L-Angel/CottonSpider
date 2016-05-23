import sys

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import Spider
from scrapy import Request
reload(sys)
sys.setdefaultencoding("utf-8")


class CblftaSpider(Spider):
    name="cblfta"
    start_urls=[
        "http://www.cblfta.org.cn/NewsList.asp"
    ]
    allowed_domains=["china-cotton.org"]
    def parse(self, response):
        #hxs = HtmlXPathSelector(response)
        items = response.xpath('//td[@class="ListTitle"]/a')
        for item in items:
            #print item
            item_url=item.xpath("@href").extract()[0]
            item_url=response.url[0:25]+item_url
            yield Request(url=item_url,callback=self.parse_item)
        page_count=response.xpath('//td[@align="right"]').extract()
        if page_count :
            page_count=page_count[0]
            print page_count

    def parse_item(self,response):
        print '---------------------debug info------------------------'
        print response.url
        print response.body
