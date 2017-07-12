import scrapy
from scrapy.spiders import CrawlSpider
from w3lib.html import remove_tags, remove_tags_with_content


class WikipediaSpider(CrawlSpider):
    name = 'wikipedia'
    start_urls = ['https://en.wikipedia.org/wiki/Outline_of_finance']

    def parse(self, response):
        """
        Parse the response page
        """
        url = response.url

        if url in WikipediaSpider.start_urls:
            return self._parse_topic_list(response)

        else:
            self.parse_topic_response(response)
            return self._parse_links(response)

    def parse_topic_response(self, response):
        """
        Parse the content
        """

        # Get the title first
        title = response.css('title::text').extract_first()

        # Replace / with a space - creates issues with writing to file
        title = title.replace('/', ' ')

        content = response.css('div#mw-content-text')

        # Just extract all the '<p></p>' children from this
        text = ''
        for child in content.xpath('//p'):

            # Get the text from this child <p></p> tag
            paragraph = child.extract()

            # Remove <script>, <sup>, <math> tags with the content
            paragraph = remove_tags_with_content(paragraph, which_ones=('script', 'sup', 'math'))
            # Remove the rest of the tags without removing the content
            paragraph = remove_tags(paragraph)

            # Replace '&amp;' with '&'
            paragraph = paragraph.replace('&amp;', '&')

            # Replace 'U.S.' with 'US':
            paragraph = paragraph.replace('U.S.', 'US')

            # Some more replacements to improve the default tokenization
            for c in '();.,[]"\'-:/%$+@?':
                paragraph = paragraph.replace(c, ' {} '.format(c))

            # Add to the file
            text += paragraph.lower() + '\n'

        filename = 'wiki_data.txt'
        f = open(filename, 'a')
        f.write(text)
        f.close()

    def _parse_links(self, response):
        """
        Parses the links from the first level of pages
        """
        content = response.css('div#mw-content-text')

        for child in content.xpath('//p'):
            # Extract the URLs
            urls = child.css('a::attr(href)').extract()

            for url in urls:
                if url is None or 'wiki' not in url:
                    continue

                next_page = response.urljoin(url)
                yield scrapy.Request(next_page, callback=self.parse_topic_response)

    def _parse_topic_list(self, response):
        """
        Parse various topics from the list of topics
        """

        # All of the links on this pages are in the bullet points
        # Therefore, extract the 'ul' tags to get the list
        content = response.css('div#mw-content-text')
        lists = content.css('ul')

        # Iterate through each list
        for ul in lists:

            # Iterate through each list item
            for l in ul.css('li'):
                # Extract the URL
                url = l.css('a::attr(href)').extract_first()

                # Skip external links as well as the links to the same page (e.g. TOC)
                if url is None or 'wiki' not in url:
                    continue

                next_page = response.urljoin(url)
                yield scrapy.Request(next_page, callback=self.parse)
