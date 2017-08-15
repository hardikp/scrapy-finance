# scrapy-finance
scrapy spiders to crawl the financial data pertinent to train word vectors.

## List of sources
* `bloomberg` - Bloomberg news articles
* `investopedia` - Definitions of finance terms from investopedia.com
* `wikipedia` - Finance pages from wikipedia - all wiki pages reachable from https://en.wikipedia.org/wiki/Outline_of_finance with at most 2 hops.
* `qplum` - Investment articles from https://www.qplum.co/investing-library

## How to use this
```
(py3) hardik@shire:~/scrapy-finance$ scrapy crawl bloomberg
```

## How to modify spiders for your use
Please look at the specific spider files like `wikipedia.py`. They are relatively easy to follow and modify.
```
.
├── LICENSE
├── README.md
├── scrapy.cfg
└── text
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders
        ├── bloomberg.py
        ├── __init__.py
        ├── investopedia.py
        ├── qplum.py
        └── wikipedia.py
```

## Notes
* The text data is written in the lower case at the moment in all spiders.
* This is not checked with python2.

## Contributing
Please feel free to submit a pull request to add relevant spiders.

## LICENSE
MIT
