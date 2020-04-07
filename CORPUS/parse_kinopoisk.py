# import modules
from bs4 import BeautifulSoup as bs
import requests
from fake_useragent import UserAgent
import pandas as pd

# variables for UserAgent (pretend to be a man, not a parser)
ua = UserAgent()
headers = {'accept': '*/*', 'user-agent': ua.firefox}

# page 250 Top Movies
page = requests.get("https://www.kinopoisk.ru/top/")

# a BeautifulSoup object is created. Data is passed to the constructor. The second option refines the parsing object.
soup = bs(page.content, 'html.parser')

def get_info(url):
  response = requests.get(url, headers=headers)
  soup = bs(response.text, 'html.parser')
  info = []
  for i in soup.find_all('table', {'class': 'info'}):
    for j in i.findAll('a')[1]:
      info.append(j)
  for i in soup.find_all('span', {'class': 'rating_ball'}):
      info.append(i.text)
  for i in soup.find_all('div', {'class': 'brand_words film-synopsys'}):
    info.append(i.text)
  for i in soup.find_all('td', {'itemprop': 'director'}):
    info.append(i.text)
  tmp = []
  for i in soup.find_all('table', {'class': 'info'}):
    for b in i.find_all('tr'):
      tmp.append((b.text))
    info.append(str(tmp[4]).replace("сценарий" , ""))
  #actors
  tmp = []
  for i in soup.find_all('li', {'itemprop': 'actors'})[0:5]:
    for b in i.find_all('a'):
      #tmp.append((b.text))
      tmp.append(b.text)
  info.append(tmp)
    #info.append(str(tmp).strip('[]').replace("'", ""))
  tmp=[]
  for i in soup.find_all('a', {'class': 'popupBigImage'}):
    for b in i.find_all('img'):
      #print(b)
      tmp.append((b['src']))
  info.append(str(tmp).strip('[]'))
  return info

# сreate an empty list
b = []
count=0

# here i find the name, year and country of the film
for ultag in soup.find_all('table', {'class': 'js-rum-hero'} ):
  for i in ultag.find_all('td' , {'style': 'height: 27px; vertical-align: middle; padding: 6px 30px 6px 0'} ):
    for j in i.find_all('a'):
      a = ((j.text).replace(')', '').split('('))
      my_list = get_info(str('https://www.kinopoisk.ru' + j['href']))
      for i in my_list:
        a.append(i)
      b.append(a)
      count=count+1
      print(count)

# convert my list to Pandas DataFrame
df = pd.DataFrame(b)
df.to_csv('top250.csv', sep='#' , header=False)

print(df)
