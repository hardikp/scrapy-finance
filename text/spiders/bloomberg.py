import os

import scrapy
from scrapy.spiders import CrawlSpider
from w3lib.html import remove_tags, remove_tags_with_content


class BloombergSpider(CrawlSpider):
    name = 'bloomberg'
    handle_httpstatus_list = [200, 404]
    allowed_domains = ['bloomberg.com']
    start_urls = ['https://www.bloomberg.com/markets']

    def parse(self, response):
        """
        Parse the response page
        """
        url = response.url

        if 'bloomberg.com' not in url:
            return

        # Visit urls starting with bloomberg.com/news/articles
        if 'bloomberg.com/news/articles' not in url:
            return self.parse_links(response)

        return self._parse_response(response)

    def _parse_response(self, response):
        """
        Parses various topics
        e.g. https://www.bloomberg.com/news/articles/2017-08-06/asian-stocks-to-gain-on-u-s-data-yen-holds-drop-markets-wrap
        """
        if response.status == 404:
            print(response.headers)

        # Get the title first
        title = response.css('title::text').extract_first()

        # Replace / with a space - creates issues with writing to file
        title = title.replace('/', ' ')

        # Get the first div with class content
        content = response.css('div.content-well')[0]

        text = title + '\n\n'
        for child in content.xpath('//p[not(@class)] | //li[not(@class)]'):
            # Get the text from this child <p></p> tag
            paragraph = child.extract()

            # Remove tags including <p> and <a>
            paragraph = remove_tags(remove_tags_with_content(paragraph, ('script', ))).strip()

            # Replace '&amp;' with '&'
            paragraph = paragraph.replace('&amp;', '&')

            text += paragraph + '\n\n'

        # Create the directory
        tokens = response.url.split('/')
        dirname = self.create_dir(tokens[-2])

        # Save the title and the text both
        filename = '{}/{}'.format(dirname, tokens[-1])
        f = open(filename, 'w')
        f.write(text)
        f.close()

        return self.parse_links(response)

    def create_dir(self, day):
        # Create the directory
        dirname = 'bloomberg'
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        dirname = dirname + '/' + day
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        return dirname

    def parse_links(self, response):

        links = response.css('a::attr(href)').extract()
        for link in links:

            if 'news/articles' not in link:
                continue

            if link.lower().endswith('.png') or link.lower().endswith('.jpg'):
                continue

            tokens = link.split('/')
            if len(tokens) < 2:
                continue
            fname = 'bloomberg/' + tokens[-2] + '/' + tokens[-1]
            if os.path.exists(fname):
                continue

            next_page = response.urljoin(link)
            yield scrapy.Request(next_page, callback=self.parse)
