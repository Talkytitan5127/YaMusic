#!/usr/bin/python3

from bs4 import BeautifulSoup

import requests
import re

from multiprocessing import Pool, Process

def get_html(url):
    
    r = requests.get(url)
    return r.text


def get_links(html):
    
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find_all('a', class_='promo__title')

    links = []
    for td in tds:
        lk = td.get('href').split('/')
        links.append(lk[2])

    return links


def get_list_names(soup):
    
    tds = soup.find_all('div', class_='playlist__title')
    
    list_name = []
    for td in tds:
        name = td.find('a').text
        list_name.append(name)

    return list_name


def get_list_likes(soup):

    tds = soup.find_all('div', class_='playlist__info')

    list_likes = []
    for td in tds:
        like = td.find('span', class_=re.compile('d-like__digits.*hard')).text
        list_likes.append(get_int(like))

    return list_likes


def get_info_dict(links, url):

    musicDict = {}
    
    for link in links:
        print("Process: %s" % link)
        html = get_html(url + link)

        soup = BeautifulSoup(html, 'lxml')

        names = get_list_names(soup)
        likes = get_list_likes(soup)

        for i in range(len(names)):
            numLike = (likes[i])
            musicDict[numLike] = musicDict.get(numLike, names[i])
    
    return musicDict


def get_int(string):
    try:
        res = ''.join(list(filter(lambda x: x.isdigit(), string)))
    except:
        print("Nonetype")
        return 0
    if not res:
        print("Nulltype")
        return 0
    return int(res)


if __name__ == "__main__":

    url = 'https://music.yandex.ru/mix/'    

    html = get_html(url + 'all')
    
    links = get_links(html)

    info = get_info_dict(links, url)
    
    with open('YaOutput.txt', 'w') as f:
        f.write("Top 100 of Yandex playlists:\n\n\n")

        i = 1
        for k, v in sorted(info.items(), reverse=True):
            if i == 101:
                break

            print(i, ')', sep='', end=' ', file=f)
            print('\"\"', v, '\"\"', 'It\'s rating is', k, sep=' ', file=f)
            
            i += 1
