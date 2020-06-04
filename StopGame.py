import requests
from bs4 import BeautifulSoup

link = 'https://stopgame.ru/articles/new'
html = requests.get(link)

soup = BeautifulSoup(html.text,'html.parser')

no_check = open('nocheck.txt','r').read().split()

_base_url_ = 'https://stopgame.ru'

_get_title_ = soup.find_all('div', attrs = {'class': 'caption caption-bold'})
_get_link_for_desc_ = soup.find_all('a',href = True)

new = []
desc = []
#make filtering

for i in range(len(_get_link_for_desc_)):
    
    if _get_link_for_desc_[i]['href'] in no_check:
        continue

    elif _get_link_for_desc_[i]['href'] == _get_link_for_desc_[i-1]['href']:
        continue

    else:
        new.append(_base_url_ + _get_link_for_desc_[i]['href'])


for i in new:
    link = requests.get(i)
    soup = BeautifulSoup(link.text,'html.parser')

    description = soup.find('section',attrs = {'class':'article article-show'})
    try:
        desc.append(description.get_text()[:500] + '(...)')

    except:
        continue

for m in range(len(new)):
    try:
        print('title: {}'.format(_get_title_[m].get_text()))
        print('')
        print('url: {}'.format(new[m]))
        print('')
        print('short description: \n{}'.format(desc[m]))
        print('')
    except:
        continue