# NEWS_TEAM_8
News Recommender System

## Technologies
![python3](https://img.shields.io/badge/python-3.7-blue)
![Crawling](https://img.shields.io/badge/Crawling-SCRAPY-important)

## Structure

```bash
newscrawling:.
|   .gitignore
|   README.md
|   scrapy.cfg
|
\---newscrawling
    |   items.py
    |   middlewares.py
    |   pipelines.py
    |   settings.py
    |   __init__.py
    |
    \---spiders
           newsbot.py
           prepreocessing.py
``` 

## Features
 - NewsBotSpider : 네이버 정치 뉴스 본문, 네이버 정치 뉴스 세부 카테고리, 네이버 정치 뉴스 작성일자, 네이버 정치 뉴스 언론사,  
    네이버 정치 뉴스 사진, 네이버 정치 뉴스 제목, 네이버 정치 뉴스 url **총 8개 item으로 약 7만건 데이터 수집** 
    
 - NewsCommentsSpider : 네이버 정치 뉴스 댓글, 네이버 정치 뉴스 댓글 유저 고유번호, 네이버 정치 뉴스 댓글 유저 아이디,   
    네이버 정치 뉴스 url **총 4개 item으로  36만건 데이터 수집**
    * 네이버 정치 뉴스 url 기준으로 NewsBotSpider와 NewsCommentsSpider의 item 결합
