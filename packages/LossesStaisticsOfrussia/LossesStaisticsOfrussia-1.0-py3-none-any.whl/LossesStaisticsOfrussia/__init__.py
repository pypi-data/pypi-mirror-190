import requests
from bs4 import BeautifulSoup

url = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
response = requests.get(url)
bs = BeautifulSoup(response.text, 'html.parser')

russian_items = bs.find('div', class_ = 'casualties').find_all('li')
personnel = russian_items[12].text
tanks = russian_items[0].text
bbm = russian_items[1].text
planes = russian_items[5].text
helicopters = russian_items[6].text
guns = russian_items[2].text
ppo_means = russian_items[4].text
drones = russian_items[8].text
cars = russian_items[10].text
rockets = russian_items[8].text

url2 = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
response = requests.get(url2)
bs2 = BeautifulSoup(response.text, 'html.parser')

dmy = bs2.find('span', class_ = 'black')
date = dmy.text
