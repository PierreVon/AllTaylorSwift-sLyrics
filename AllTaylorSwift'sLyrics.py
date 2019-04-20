import requests
from bs4 import BeautifulSoup
import re
import os

albums = ['taylor-swift',
          'speak-now',
          'fearless',
          'red',
          '1989',
          'reputation']

basic_url = 'http://www.songlyrics.com/taylor-swift/'
path = 'f:/taylorswift/'


def mkdir(path):
    flag = os.path.exists(path)
    if not flag:
        os.makedirs(path)


def req(url):
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text


def all_songs(r):
    soup = BeautifulSoup(r, "html.parser")
    match = ''
    songs_name = []
    b = soup.find('tbody')
    songs_url = re.findall(r'http.+?s/', str(b))
    for i in range(len(songs_url)):
        name = songs_url[i]
        name = name.split('/')[-2]
        songs_name.append(name)
    return songs_url,songs_name


def lyrics(r, name, subpath):
    soup = BeautifulSoup(r, "html.parser")
    match = ''
    for link in soup.find_all('p', 'songLyricsV14'):
        match = re.sub(r'<.+?>', '', str(link))

    txt = subpath + name + '.txt'
    with open(txt, 'w+') as f:
        f.write(match)


def scrape():
    mkdir(path)
    for i in range(6):
        url = basic_url + albums[i] + '/'
        html = req(url)
        subpath = path + albums[i] + '/'
        mkdir(subpath)
        songs_url, songs_name = all_songs(html)
        for j in range(len(songs_url)):
            try:
                ly_html = req(songs_url[j])
                lyrics(ly_html, songs_name[j], subpath)
                print(songs_name[j], 'downloaded!')
            except:
                continue


scrape()
