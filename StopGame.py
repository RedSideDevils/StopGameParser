from os import write
import requests
from bs4 import BeautifulSoup
import csv

class Parser:
    def __init__(self):
        self.url = 'https://stopgame.ru/articles/new'
        self._base_url_ = 'https://stopgame.ru'
        self.no_check = open('nocheck.txt', 'r').read().split()

    def parse(self):
        html = requests.get(self.url)
        soup = BeautifulSoup(html.text, 'html.parser')
        _get_title_ = soup.find_all(
            'div', attrs={'class': 'caption caption-bold'})
        _get_link_for_desc_ = soup.find_all('a', href=True)
        new = []
        desc = []

        for i in range(len(_get_link_for_desc_)):

            if _get_link_for_desc_[i]['href'] in self.no_check:
                continue

            elif _get_link_for_desc_[i]['href'] == _get_link_for_desc_[i-1]['href']:
                continue

            else:
                new.append(self._base_url_ + _get_link_for_desc_[i]['href'])
                
        for i in new:
            link = requests.get(i)
            soup = BeautifulSoup(link.text,'html.parser')

            description = soup.find('section',attrs = {'class':'article article-show'})
            try:
                desc.append(description.get_text()[:500] + '(...)')

            except:
                continue
        
        return new, _get_title_, desc
               
    def to_csv(self, file):
        all_data = self.parse()
        
        with open(str(file), 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "URL", "Description"])        
            
            try:
                for i in range(len(all_data[0])):
                    writer.writerow([all_data[1][i].get_text(), all_data[0][i], all_data[2][i]])
            except:
                print("Program Ended Work!")
                

myclass = Parser()
myclass.to_csv('data.csv')
        
        
