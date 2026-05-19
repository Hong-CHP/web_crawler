## Web Crawler
This is an internet bot that systematically browsers the world wide web.

## robots.txt
The protocol for web crawling. 
Viste: https://xxx.xxx/robots.txt to check crawling authorization and the sources that allowed or forbidden for crawling.
- ***user-agent***: authorizes certains types of crawlers
- ***Disallow***: forbidden sources
- ***Allow***: allowed sources
- ***Sitmap***: map of website, supported urls
- ***Crawl-delay***: frequence of crawling

## Start

### 1. Send http request
Send a request to the target url

### 2. Extract data from web
Use lxml and xpath to extract all target information

### 3. Clean data source
Fix missing data, remove duplicate data, parse exceptional data and format the results

### 4. Stock data
Stock the content in a local .csv file
