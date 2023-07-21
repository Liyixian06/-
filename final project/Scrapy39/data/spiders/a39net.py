import time

import scrapy

from data.items import a39Item


class A39netSpider(scrapy.Spider):
    name = "a39net"
    allowed_domains = ["39.net"]
    start_urls = ["https://jbk.39.net/bw/t1/"]
    url_header = 'https://jbk.39.net'
    custom_settings = {
        'ITEM_PIPELINES': {
            'data.pipelines.a39netDataPipeline': 300,
        }
    }

    # 选择科室
    def parse(self, response):
        time.sleep(5)
        hrefs = response.xpath("//div[@class='lookup_department lookup_cur']/div/ul/li/a/@href").extract()
        for (href) in hrefs:
            href = self.url_header + href
            yield scrapy.Request(
                url=href,
                callback=self.First_classification
            )

    # 选择科室下的细分
    def First_classification(self, response):
        hrefs = response.xpath("//div[@class='lookup_second_box first_line']/ul/li/a/@href").extract()
        for href in hrefs:
            href = self.url_header + href
            yield scrapy.Request(
                url=href,
                callback=self.Second_classification
            )

    # 进入科室下的疾病
    # 该网站多页,在此做翻页
    def Second_classification(self, response):
        hrefs = response.xpath("//div[@class='result_content']/div/div/p[@class='result_item_top_l']/a/@href").extract()
        for href in hrefs:
            yield scrapy.Request(
                url=href,
                callback=self.basic_information
            )
        # 翻页
        next_href = self.url_header + response.xpath("//ul[@class='result_item_dots']/li/span[contains(a/text(),'>')]/a/@href").extract_first()
        if next_href:
            yield scrapy.Request(
                url=next_href,
                callback=self.Second_classification
            )


    # 疾病基础页,不够查询,做跳转
    def basic_information(self, response):

        introduction_url = response.xpath("//p[@class='information_l']/a/@href").extract_first()
        yield scrapy.Request(
            url=introduction_url,
            callback=self.detailed_information,

        )

    


    def detailed_information(self, response):
        item = a39Item()
        name = response.xpath("//div[@class='disease_box'][1]/div/h1/text()").extract_first()
        introduction = response.xpath("//div[@class='list_left']/div[1]/p[2]/text()").extract_first().strip(). \
                      replace('\n', '').replace('\r', '')
        altname = response.xpath("//div[@class='disease_box'][1]/div/h2/text()").extract_first().strip(). \
                      replace('\n', '').replace('\r', '')[1:-1]
        if not altname:
            altname = 'None'
        pathogenic_site = response.xpath(
            "//ul[@class='disease_basic']/li[contains(span[1]/text(),'发病部位：')]/span[2]/a/text()").extract_first()
        department = response.xpath(
            "//ul[@class='disease_basic']/li[contains(span[1]/text(),'就诊科室：')]/span[2]/a/text()").extract()
        department = ",".join(department)
        population = response.xpath(
            "//ul[@class='disease_basic']/li[contains(span/text(),'多发人群：')]/span[2]/text()").extract_first()
        symptom = response.xpath(
            "//ul[@class='disease_basic']/li[contains(span/text(),'相关症状：')]/span[2]/a/text()").extract()
        symptom = ",".join(symptom).strip(). \
            replace('\n', '').replace('\r', '').replace(" ", "")
        inspect = response.xpath(
            "//ul[@class='disease_basic']/li[contains(span/text(),'相关检查：')]/span[2]/a[@class='blue']/text()").extract()
        inspect = ",".join(inspect).strip(). \
            replace('\n', '').replace('\r', '').replace(" ", "")
        complication = response.xpath(
            "//ul[@class='disease_basic']/li[contains(span/text(),'并发疾病：')]/span[2]/a[@class='blue']/text()").extract()
        complication = ",".join(complication).strip(). \
            replace('\n', '').replace('\r', '').replace(" ", "")
        if not complication:
            complication = 'None'
        treatment = response.xpath(
            "//ul[@class='disease_basic']/li[contains(span/text(),'治疗方法：')]/span[2]/a[@class='blue']/text()").extract()
        treatment = ",".join(treatment).strip(). \
            replace('\n', '').replace('\r', '').replace(" ", "")
        medication = response.xpath(
            "//ul[@class='disease_basic']/li[contains(span/text(),'常用药品：')]/span[2]/a/text()").extract()
        medication = ",".join(medication).strip(). \
            replace('\n', '').replace('\r', '').replace(" ", "")
        if not medication:
            medication = 'None'
        
        # cause = (response.xpath(
            # "/html/body/div[5]/div/div[2]/ul/li[1]")).xpath("/html/body/div[6]/div[4]/div[1]/div[2]/p/text()").extract()
        cause = response.xpath("//div[@class='navigation'][2]/ul[@class='navigation_ul']/li[@class=''][2]/a/@href").extract_first()
        # cause_str = [cause] if cause is not None else []

        item['name'] = name
        item['introduction'] = introduction
        item['altname'] = altname
        item['pathogenic_site'] = pathogenic_site
        item['department'] = department
        item['population'] = population
        item['symptom'] = symptom
        item['inspect'] = inspect
        item['complication'] = complication
        item['treatment'] = treatment
        item['medication'] = medication
        item['cause'] = cause
        
        # print(response.request.url)
        # print(introduction)

        # print(item.items())
        yield item

