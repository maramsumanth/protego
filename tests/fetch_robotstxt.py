import os
import sys
import argparse
from urllib.parse import urlparse
import scrapy
from scrapy.crawler import CrawlerProcess

parser = argparse.ArgumentParser(description='Download robots.txt of given websites.')
parser.add_argument('-l', '--list', action='append', dest='websites', help='Adds to the list of websites.')
parser.add_argument('-d', '--destination', action='store', dest='directory',
                    help='Directory to save robots.txt files.')
args = parser.parse_args()

if not args.directory or not args.websites:
    print("Insufficient or invalid argument(s) provided.")
    sys.exit()


class RobotstxtSpider(scrapy.Spider):
    name = "robotstxt_spider"

    def start_requests(self):
        for w in args.websites:
            if os.path.isfile(w):
                with open(w, 'r') as f:
                    for domain in f:
                        domain = domain.strip()
                        yield scrapy.Request(url="http://{}/robots.txt".format(domain), callback=self.parse)

    def parse(self, response):
        filename = urlparse(response.url).netloc
        if not os.path.exists(args.directory):
            os.mkdir(args.directory)
        with open(os.path.join(args.directory, filename), 'wb') as f:
            f.write(response.body)


process = CrawlerProcess(settings={'ROBOTSTXT_OBEY': False})
process.crawl(RobotstxtSpider)
process.start()