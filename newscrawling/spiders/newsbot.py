import scrapy
from newscrawling.items import NewscrawlingItem
import csv
import requests
import json

class NewsBotSpider(scrapy.Spider):
    name = 'NewsBot'
    base_url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=100&sid2="
    headers = {"user-agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
    pol_sections = list(range(264, 270))
    pages = list(range(1, 400))

    def start_requests(self):
        for sec in self.pol_sections:
            for date in range(20221101, 20221131):
                for page in self.pages:
                    params = f'{sec}&date={date}&page={page}'
                    yield scrapy.Request(url= self.base_url + params, headers= self.headers, callback= self.parse_link)

    def parse_link(self, response):
        categories = response.xpath('//*[@id="main_content"]/div[1]/h3/text()').extract()
        urls = response.xpath(f'//*[@id="main_content"]/div[2]/ul/li/dl/dt/a/@href').extract()
        for url in urls:
            print(url)
            yield scrapy.Request(url, callback= self.parse_articles, headers= self.headers, meta={'categories':categories})

    def parse_articles(self, response):
        item = NewscrawlingItem()
        articles = response.css('#dic_area::text').extract()
        item['articles'] = ''.join(article.strip() for article in articles)
        item['categories'] = response.meta.get('categories')
        item['dates'] = response.xpath('//*[@id="ct"]/div[1]/div[3]/div[1]/div/span/@data-date-time').extract()
        item['media'] = response.xpath('//*[@id="ct"]/div[1]/div[1]/a/img[1]/@alt').extract()
        item['photo_urls'] = response.xpath('//*[@id="img1"]').get().split('src=')[1].split(' ')[0]
        item['titles'] = response.xpath('//*[@id="title_area"]/span/text()').extract()
        item['urls'] = response.url
        yield item

class NewsCommentsSpider(scrapy.Spider):
    name = 'NewsComments'

    def start_requests(self):
        with open('newsUrl.csv', 'r', encoding='utf-8') as f:
            dic = csv.DictReader(f)
            for row in dic:
                comment_url = row['urls'].split('article/')[0] + 'article/comment/' + row['urls'].split('article/')[1]
                yield scrapy.Request(url=comment_url, headers = {"user-agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}, callback=self.parse_comments,
                                     cb_kwargs=dict(url=row['urls']))

    def parse_comments(self, response, url):
        current_url = response.url
        params = current_url.split('comment/')[1].split('?sid=')[0].replace('/', ',')

        request_url = f"https://cbox5.apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_politics_m3&pool=cbox5&lang=ko&objectId=news{params}&categoryId=&pageSize=100&indexSize=10&pageType=more&page=1"
        header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Mobile Safari/537.36',
            'accept': "*/*",
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': response.url}

        raw_html = requests.get(request_url, headers=header)
        raw_json = raw_html.text.replace('_callback(', '').replace(');', '')
        json_data = json.loads(raw_json)

        item = NewscrawlingItem()
        for comment in json_data['result']['commentList']:
            item['comments'] = comment['contents']
            item['users'] = comment['maskedUserName']
            item['userIDs'] = comment['userIdNo']
            item['comment_urls'] = [url]
            yield item