# NEWS_TEAM_8
News Recommender System

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
 - NewsBotSpider : 네이버 정치 뉴스 본문, 네이버 정치 뉴스 세부 카테고리, 
                   네이버 정치 뉴스 작성일자, 네이버 정치 뉴스 언론사,
                   네이버 정치 뉴스 사진, 네이버 정치 뉴스 제목,
                   네이버 정치 뉴스 url 총 8개 item 수집
 - NewsCommentsSpider : 네이버 정치 뉴스 댓글, 네이버 정치 뉴스 댓글 유저 고유번호, 
                        네이버 정치 뉴스 댓글 유저 아이디, 네이버 정치 뉴스 url 총 4개 item 수집
                        * 네이버 정치 뉴스 url 기준으로 NewsBotSpider, NewsCommentsSpider의 item 결합
