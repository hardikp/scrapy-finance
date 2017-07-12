# scrapy-finance
scrapy spiders to crawl the financial data pertinent to train word vectors.

### List of sources
* `qplum` - Investment articles from https://www.qplum.co/investing-library
* `investopedia` - Definitions of finance terms from investopedia.com
* `wikipedia` - Finance pages from wikipedia - all wiki pages reachable from https://en.wikipedia.org/wiki/Outline_of_finance with at most 2 hops.

### How to use this
```
$ scrapy crawl qplum
```

### Notes
* The text data is written in the lower case at the moment in all spiders.

### Contributing
Please feel free to submit a pull request to add relevant spiders.
