from selenium import webdriver    #open webdriver for specific browser
from selenium.webdriver.common.keys import Keys   # for necessary browser action
from selenium.webdriver.common.by import By    # For selecting html code

import time
import pandas as pd
import numpy as np
import re

import scrapy
from scrapy.spiders import CrawlSpider


from fg2000.items import Fg2000Item

#simulate browser to get links
driver = webdriver.Firefox(executable_path=r'geckodriver.exe') #webdriver.Chrome(executable_path=r'chromedriver.exe')
driver.get("https://www.forbes.com/global2000/list/")
time.sleep(5)
driver.find_element_by_class_name('continue-button').click()
time.sleep(15)

#Expecting Internet speed to be good(atleast 5Mbps) 250 is maximum number of clicks required to see Complete G2000 list
for i in range(0,250): 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    if i<2:
        time.sleep(15)
data = {
    'Link' : []
}

link = driver.find_elements_by_xpath("id('list-table-body')//td[3]/a")
data['Link']=[(link[i].get_attribute("href")) for i in range(len(link))]

time.sleep(3)
df=pd.DataFrame(data)

driver.quit()

#df = pd.read_csv("forbes2017_links.csv", header=None)

links = []
for i in df.values:
    links.append(i[0])

class fg2000Spider(CrawlSpider):
    name = "fg2000"
    allowed_domains = ["www.forbes.com"]
    start_urls = links
    #start_urls = ["https://www.forbes.com/companies/icbc/"]
    #def start_requests(self):
    #    url = "https://www.forbes.com/companies/icbc/" #links
    #    yield scrapy.Request(url, self.parse)
    
    def parse(self, response):
        #pagesource = Selector(response)
        names = header = values = num_header = num_values = rnk = cn = tick = ind = fndd = cntry = ceo = ws = emp = sales = hq = ceo_pay = rvnu = assts = prft = prfl = ''
        names = response.xpath("id('left_rail')/div[1]/div[1]/h1/text()").extract()
        header = response.xpath("id('left_rail')/div[1]/div[1]/dl/dt/text()|id('left_rail')/div[1]/div[1]/dl/dt/a/text()").extract()
        values = response.xpath("id('left_rail')/div[1]/div[1]/dl/dd/text()|id('left_rail')/div[1]/div[1]/dl/dd/a/text()").extract()
        num_header = response.xpath("id('right_rail')/div[5]/div/dl/dt/text()").extract()
        num_values = response.xpath("id('right_rail')/div[5]/div/dl/dd/text()").extract()
        forbes_link = response.url
        m = re.split("\s", names[0], 1)
        rnk = m[0]
        cn = m[1]
        
        try:
            profile_1 = response.xpath("id('left_rail')/div[2]/text()").extract()
            profile_2 = response.xpath("id('left_rail')/div[2]/span/text()").extract()
            prfl = profile_1[0] + profile_2[0]
        except:
            prfl = profile_1[0]
        
        
        for j in range(len(header)):
            if header[j] == "Ticker":
                tick = values[j]
            if header[j]=="Industry":
                ind = values[j]
            if header[j] == "Founded":
                fndd = values[j]                
            if header[j] == "Country":
                cntry = values[j]
            if header[j] == "CEO" or header[j] == "Chief Executive Officer":
                ceo = values[j]
            if header[j] == "Website":
                ws = values[j]
            if header[j] == "Employees":
                emp = values[j]
            if header[j] == "Sales":
                sales = values[j]
            if header[j] == "Headquarters":
                hq = values[j]                
            if header[j] == "CEO Compensation":
                ceo_pay = values[j]
        
        for i in range(len(num_header)):
            if num_header[i] == "Revenue":
                rvnu = num_values[i]
            if num_header[i] == "Assets":
                assts = num_values[i]
            if num_header[i] == "Profits":
                prft = num_values[i]


        yield{
            'Rank' : str(rnk).strip(" \#\r\t\n"),
            'Company' : str(cn).strip(" \r\t\n"),
            'Ticker' : str(tick).strip(" \r\t\n"),
            'Industry' : str(ind).strip(" \r\t\n"),
            'Founded' : str(fndd).strip(" \r\t\n"),
            'Country' : str(cntry).strip(" \r\t\n"),
            'CEO' : str(ceo).strip(" \r\t\n"),
            'Website' : str(ws).strip(" \r\t\n"),
            'Employees' : str(emp).strip(" \r\t\n"),
            'Sales' : str(sales).strip(" \r\t\n"),
            'Headquarters' : str(hq).strip(" \r\t\n"),
            #'CEO Compensation' : str(ceo_pay).strip(" \r\t\n"),
            'Revenue' : str(rvnu).strip(" \r\t\n").strip(" \r\t\n"),
            'Assets' : str(assts).strip(" \r\t\n"),
            'Profit' : str(prft).strip(" \r\t\n"),
            'Profile' : str(prfl).strip(" \r\t\n"),
            'Forbes Link' : str(forbes_link),
            'header' : str(header).strip(" \r\t\n"),
            'values' : str(values).strip(" \r\t\n"),
        }


        #url = response.xpath("id('right_rail')/div[2]/a/@href").extract()
        #if url is not None:
        #    try:
        #        url = response.urljoin(url[0])
        #        yield scrapy.Request(url, callback=self.parse)
        #    except:
        #        pass