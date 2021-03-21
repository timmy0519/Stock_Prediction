import scrapy
import os 
from os import listdir
import csv
import sys
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess

global abs_path
global path
global year


year = 0
month = 0
month1 = 1
month2 = 1

if len(sys.argv) == 4:
    year = sys.argv[1]
    month1 = sys.argv[2]
    month = month1
    month2 = sys.argv[3]

abs_path = 'file:///c:/Users/Jake/Desktop/Stock_Prediction-main/htmlData/raw/{}/{}/profiles/Yahoo/US/01/p/'.format(year,month)
path = r"c:\Users\Jake\Desktop\Stock_Prediction-main\htmlData\raw\{}\{}\profiles\Yahoo\US\01\p\\".format(year,month)


class StockSpider(scrapy.Spider):
    name = "stock"
    global month
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'htmlData/raw/{} - {}.csv'.format(year,month)
    }
    
    def start_requests(self):
        global abs_path
        global path
        urls = []
        alphabet = "z"#"abcdefghijklmnopqrstuvwxyz"
        for i in alphabet:
            folder = path +  i
            files = listdir(folder)
            for file in files:
                urls.append(abs_path  + i + "/" + file)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
        def convert(x):
            if 'K' in x:
                if len(x) > 1:
                    return float(x.replace('K', '')) * 1000
                return 1000.0
            if 'M' in x:
                if len(x) > 1:
                    return float(x.replace('M', '')) * 1000000
                return 1000000.0
            if 'B' in x:
                return float(x.replace('B', '')) * 1000000000
            return 0.0
        market_cap = response.xpath("//*[contains(text(), 'Market Cap:')]/..//td/span//text()").get()
        price = response.xpath("//*[contains(text(), 'Last Trade:')]/..//td/big/b/span//text()").get()
        total_shares = convert(response.xpath("//*[contains(text(), 'Shares Outstanding')]/../td[@class='yfnc_tabledata1']/text()").get())

        price_sale = response.xpath("//*[contains(text(), 'Price/Sales (ttm):')]/..//td")[1].xpath('text()').get()
        price_book = response.xpath("//*[contains(text(), 'Price/Book (mrq):')]/..//td")[1].xpath('text()').get()
        return_on_assets = response.xpath("//*[contains(text(), 'Return on Assets (ttm):')]/..//td")[1].xpath('text()').get()
        return_on_equity = response.xpath("//*[contains(text(), 'Return on Equity (ttm):')]/..//td")[1].xpath('text()').get()
        revenue_per_share = response.xpath("//*[contains(text(), 'Revenue Per Share (ttm):')]/..//td")[1].xpath('text()').get()
        quarterly_revenue_growth = response.xpath("//*[contains(text(), 'Qtrly Revenue Growth (yoy):')]/..//td")[1].xpath('text()').get()
        
        total_cash_per_share = response.xpath("//*[contains(text(), 'Total Cash Per Share (mrq):')]/..//td")[1].xpath('text()').get()
        debt_to_equity = response.xpath("//*[contains(text(), 'Total Debt/Equity (mrq):')]/..//td")[1].xpath('text()').get()
        book_per_share = response.xpath("//*[contains(text(), 'Book Value Per Share (mrq):')]/..//td")[1].xpath('text()').get()
        operating_cash = response.xpath("//*[contains(text(), 'Operating Cash Flow (ttm):')]/..//td")[1].xpath('text()').get()
        volume = response.xpath("//*[contains(text(), 'Volume:')]/..//td//text()").get()
        Price_per_Earnings_ratio =  response.xpath('//table[@id="table2"]//tr//th[contains(text(), "P/E ")]/..//td[@class="yfnc_tabledata1"]//text()').get()
        earnings_per_share = response.xpath('//table[@id="table2"]//tr//th[contains(text(), "EPS ")]/..//td[@class="yfnc_tabledata1"]//text()').get()
        sector = response.xpath('//*[contains(text(), "Sector:")]/../td/a/text()').get()
        industry = response.xpath('//*[contains(text(), "Industry:")]/../td/a/text()').get()
        revenue_per_dollar = int(float(revenue_per_share) * total_shares / float(price))
        total_cash_per_dollar = int(float(total_cash_per_share) * total_shares / float(price))
        book_per_dollar = int(float(book_per_share) * total_shares / float(price))
        earnings_per_dollar = int(float(earnings_per_share) * total_shares / float (price))

        operating_cash_flow = response.xpath("//*[contains(text(),'Total Cash Flow From Operating Activities')]/../../td[@align='right']/strong/text()")
        capital_expenditures = response.xpath("//*[contains(text(),'Capital Expenditures')]/../td[@align='right']/text()")
        free_cash_flow = 0

        for i in range(len(operating_cash_flow)):
            free_cash_flow += int(operating_cash_flow[i].get().strip("()").replace(",",""))
            free_cash_flow -= int(capital_expenditures[i].get().strip("()").replace(",",""))
        free_cash_flow = 0 if free_cash_flow == 0 else free_cash_flow
        free_cash_flow *= 1000
        Enterprise_value = convert(response.xpath("//*[contains(text(), 'Enterprise Value ')]/..//td[@class='yfnc_tabledata1']/text()").get())
        FCF_yield = free_cash_flow / Enterprise_value
        Enterprise_value_to_FCF = Enterprise_value / free_cash_flow

        price_to_free_cash_flow = convert(market_cap) / free_cash_flow
        sp_change = response.xpath('//*[contains(text(), "S&P500 52-Week Change")]/../td[@class="yfnc_tabledata1"]/text()').get()
        stock_year_change = response.xpath('//*[contains(text(), "52-Week Change")]/../td[@class="yfnc_tabledata1"]/text()')[0].get()


        page = response.url.split("/")[-1].split(".")
        if len(page) == 2:
            page = page[0]
        else:
            page = page[0] + "." + page[1]


        yield {
            "Stock code":page,"market cap":market_cap,"price per sale":price_sale, \
                "current price":price, "price per book": price_book, "return on assets":return_on_assets,\
                "return on equity":return_on_equity,"revenue per share":revenue_per_share,\
                "quarterly revenue growth":quarterly_revenue_growth,\
                "total cash per share":total_cash_per_share,"debt equity ratio":debt_to_equity,\
                "book value per share":book_per_share, "operating cash flow":operating_cash,\
                "volume": volume, "Price per Earnings ratio" :Price_per_Earnings_ratio,\
                "earnings per shares": earnings_per_share, "sector": sector, "industry": industry,\
                "total cash per dollar": total_cash_per_dollar, "book value per dollar": book_per_dollar,\
                "earnings per dollar": earnings_per_dollar,"revenue per dollar":revenue_per_dollar,\
                "free cash flow": free_cash_flow ,"price to free cash flow": price_to_free_cash_flow,\
                "s&p 52 week change": sp_change, "stock 52 week change": stock_year_change,\
                "FCF yield": FCF_yield, "EV / FCF": Enterprise_value_to_FCF

        }



configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    global abs_path
    global path
    global month
    yield runner.crawl(StockSpider)
    StockSpider.custom_settings["FEED_URI"] = 'htmlData/raw/{} - {}.csv'.format(year,month2)
    abs_path = 'file:///c:/Users/Jake/Desktop/Stock_Prediction-main/htmlData/raw/{}/{}/profiles/Yahoo/US/01/p/'.format(year,month2)
    path = r"c:\Users\Jake\Desktop\Stock_Prediction-main\htmlData\raw\{}\{}\profiles\Yahoo\US\01\p\\".format(year,month2)
    yield runner.crawl(StockSpider)
    reactor.stop()

crawl()
reactor.run()