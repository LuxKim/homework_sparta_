import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbhomework  # 'dbsparta'라는 이름의 db를 만듭니다.
if db['songs'].count_documents({}) > 50:        # 테이블 항목 숫자 세기
    print("db update\n")
    db['songs'].delete_many({})                 # 일괄 삭제

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
                     #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
# print(songs)

for song in songs:
    title = song.select_one('td.info > a')                      #제목
    artist = song.select_one('td.info > a.artist.ellipsis')     #가수
    rank = song.select_one('td.number')                         #순위

    if title is not None:
        text_rank = rank.text[0:2].strip().rjust(2, ' ')
        text_title = title.text.strip()
        text_artist = artist.text
        print(text_rank + ". " + text_title + " - " + text_artist)

        doc_data = {
            'rank': text_rank,
            'title': text_title,
            'artist': text_artist
        }
        db.songs.insert_one(doc_data)
