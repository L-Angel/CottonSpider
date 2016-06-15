from scrapy.selector import HtmlXPathSelector
from scrapy.spider import Spider
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from cotton.items import CottonItem
from scrapy import Request



class ChinaCoottonSpider(Spider):
    name="chinacotton"
    start_urls = [
        "http://www.china-cotton.org/warning/newContent"
    ]
    allowed_domains=["china-cotton.org"]
    def   __init__(self):
        self.f=open('out.txt','wb')
    def parse(self, response):
        #hxs=HtmlXPathSelector(response)
        caches=response.xpath('//div[@class="border special"]/div')
        for e in caches:
            item = CottonItem()
            url=e.xpath('a/@href').extract()[0]
            if str(url).startswith('/.//'):
                url=response.url[0:27]+url[3:]
                print url
                yield Request(url=url,callback=self.parse_item)
        next_page_url=response.xpath('//h1/span/a[last()-1]/@href').extract()
        next_page_url = response.url[0:27]+next_page_url[0]
        print "crawl url : ",next_page_url
        if next_page_url:
            req = Request(url=next_page_url,callback=self.parse)
            yield req



    def parse_item(self,response):
        hxs=HtmlXPathSelector(response)
        t=hxs.select('//div[@class="border article"]/h1/text()').extract()[0]
        c=hxs.select('//div[@class="txt"]').extract()[0]
        self.f.write(response.url+'   ')
        self.f.write(t+'   ')
        #self.f.write(c+'   ')
        self.f.write('\r\n')
        yield CottonItem(URL=response.url,title=t,content=c)
