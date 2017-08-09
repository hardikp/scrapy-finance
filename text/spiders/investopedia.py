from string import ascii_lowercase
import os

import scrapy
from scrapy.spiders import CrawlSpider
from w3lib.html import remove_tags, remove_tags_with_content


class InvestopediaSpider(CrawlSpider):
    name = 'investopedia'
    start_urls = ['http://www.investopedia.com/terms/%s/' % s for s in ascii_lowercase + '1']

    def parse(self, response):
        """
        Parse the response page
        """
        url = response.url

        # 'terms' has to be there in the URL to proceed further
        if 'terms' not in url:
            return

        # if the url ends with '.asp', then that's a topic page
        if url.endswith('.asp'):
            return self._parse_topic_response(response)

        # Otherwise, assume that this a list page
        return self._parse_topic_list(response)

    def _parse_topic_response(self, response):
        """
        Parses various topics
        e.g. www.investopedia.com/terms/o/oddlottheory.asp
        """
        # Get the title first
        title = response.css('title::text').extract_first()

        # Replace / with a space - creates issues with writing to file
        title = title.replace('/', ' ')

        # Get the first div with class content
        content = response.css('div.content')[0]

        text = ''
        for child in content.xpath('//p'):

            # Get the text from this child <p></p> tag
            paragraph = child.extract()

            # Remove tags including <p> and <a>
            paragraph = remove_tags(remove_tags_with_content(paragraph, ('script', ))).strip()

            # Replace '&amp;' with '&'
            paragraph = paragraph.replace('&amp;', '&')

            # Add to the file
            text += paragraph + '\n'

        # Create the directory
        dirname = 'investopedia'
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        elif not os.path.isdir(dirname):
            os.remove(dirname)
            os.mkdir(dirname)

        # Save the title and the text both
        filename = '{}/{}'.format(dirname, title)
        f = open(filename, 'w')
        f.write(text)
        f.close()

    def _parse_topic_list(self, response):
        """
        Parse the page with the topics listed out
        e.g. www.investopedia.com/terms/o/
        """
        list_element = response.css('ol.list')

        # Iterate through the list of topics
        for l in list_element.css('li'):
            # Extract the URL
            url = l.css('a::attr(href)').extract_first()

            next_page = response.urljoin(url)
            yield scrapy.Request(next_page, callback=self.parse)
