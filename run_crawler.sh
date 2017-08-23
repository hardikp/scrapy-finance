#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "USAGE: $0 {bloomberg/investopedia}"
else
    SPIDER=$1
fi

cd scrapy-finance
source ~/h/bin/activate
scrapy crawl $SPIDER
