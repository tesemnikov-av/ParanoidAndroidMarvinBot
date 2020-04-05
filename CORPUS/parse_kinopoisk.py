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

def get_country(url):
  """
        This feature gets the movie producer country.
        This function takes one arguments (url page movie) and returns one values: name country.
    Example Output:
        США
  """
  response = requests.get(url, headers=headers)
  soup = bs(response.text, 'html.parser')
  for i in soup.find_all('table', {'class': 'info'}):
    for j in i.findAll('a')[1]:
      return(j)

def get_rating_ball(url):
  response = requests.get(url, headers=headers)
  soup = bs(response.text, 'html.parser')
  for i in soup.find_all('span', {'class': 'rating_ball'}):
      return(i.text)

def get_overview(url):
  response = requests.get(url, headers=headers)
  soup = bs(response.text, 'html.parser')
  for i in soup.find_all('div', {'class': 'brand_words film-synopsys'}):
      return(i.text)

def get_director(url):
  response = requests.get(url, headers=headers)
  soup = bs(response.text, 'html.parser')
  for i in soup.find_all('td', {'itemprop': 'director'}):
      return(i.text)

def get_screeplay(url):
  tmp = []
  response = requests.get(url, headers=headers)
  soup = bs(response.text, 'html.parser')
  for i in soup.find_all('table', {'class': 'info'}):
    for b in i.find_all('tr'):
      tmp.append((b.text))
  return(str(tmp[4]).replace("сценарий" , ""))

def get_actor(url):
  tmp = []
  response = requests.get(url, headers=headers)
  soup = bs(response.text, 'html.parser')
  for i in soup.find_all('li', {'itemprop': 'actors'})[0:5]:
    for b in i.find_all('a'):
      tmp.append((b.text))
  return(str(tmp).strip('[]').replace("'", ""))

# сreate an empty list
b = []

# here i find the name, year and country of the film
for ultag in soup.find_all('table', {'class': 'js-rum-hero'} ):
  for i in ultag.find_all('td' , {'style': 'height: 27px; vertical-align: middle; padding: 6px 30px 6px 0'} ): #[0:1:1]:
    for j in i.find_all('a'):
      a = ((j.text).replace(')', '').split('('))
      a.append(get_country(str('https://www.kinopoisk.ru' + j['href'])))
      a.append(get_rating_ball(str('https://www.kinopoisk.ru' + j['href'])))
      a.append(get_overview(str('https://www.kinopoisk.ru' + j['href'])))
      a.append(get_director(str('https://www.kinopoisk.ru' + j['href'])))
      a.append(get_screeplay(str('https://www.kinopoisk.ru' + j['href'])))
      a.append(get_actor(str('https://www.kinopoisk.ru' + j['href'])))
      b.append(a)

# convert my list to Pandas DataFrame
df = pd.DataFrame(b)
df.to_csv('top250.csv', sep='#' , header=False)

print(df)
