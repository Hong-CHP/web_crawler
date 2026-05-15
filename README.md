## Web Crawler
This is an internet bot that systematically browsers the world wide web.

## robots.txt
The protocol for web crawling. 
Viste: https://xxx.xxx/robots.txt to make sure the authorization to craw and the sources allowed or forbidden for crawling.
- ***user-agent***: authorize certains types of crawler
- ***Disallow***: Forbidden sources
- ***Allow***: Allow sources
- ***Sitmap***: map of site, url supports
- ***Crawl-delay***: frequence of crawling

## Start

### 1. Send http request
Send a request to target url

### 2. Extract data from web
Use lxml and xpath to extract all target informations

### 3. Clean data source

### 4. Stock data
Stock content in a local .csv file
