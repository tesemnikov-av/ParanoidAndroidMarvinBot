# Use this script to preprocess data and create a database
# !pip -q install pymorphy2

import sqlite3
import pandas as pd
import nltk
from nltk import word_tokenize
import string
from nltk.corpus import stopwords
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


def tokenize_ru(file_text):

  tokens = word_tokenize(file_text)
  tokens = [i for i in tokens if (i not in string.punctuation)]

  my_stop_words = stopwords.words('russian')
  my_stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...'])

  tokens = [token for token in tokens if (token not in my_stop_words)]
  tokens = [token.replace("«", "").replace("»", "") for token in tokens]
  tokens = [ morph.parse(token)[0].normal_form for token in tokens ]
  
  return str(tokens).strip('[]').replace("'","").replace(",","")


# Download FAQ dataset
dialogs = pd.read_excel('dialog_talk_agent.en.ru.xlsx', names=['Context','Text Response'])
dialogs.ffill(axis = 0,inplace=True)

# Here you can expand the base of questions and answers
dialogs = dialogs.append({'Context' : 'Ты повторяешься' , 'Text Response' : 'Да и ты тоже'} , ignore_index=True)
dialogs = dialogs.append({'Context' : 'Пойдем пить пиво' , 'Text Response' : 'Да возьми мне пару баночек'} , ignore_index=True)

dialogs['lemmatized_text'] = dialogs['Context'].map(lambda x: tokenize_ru(str(x)))

# Download TOP250 movie dataset
top250 = pd.read_csv('top250.csv', sep='#' , names=['original_title','year', 'country' , 'score' , 'overview','director','screenplay' , 'actors' , 'url'])
top250['overview_tokenize'] = top250['overview'].map(lambda x: tokenize_ru(str(x)))
top250['original_title_lower'] = top250['original_title'].map(lambda x: x.lower().strip())
top250['creators'] = top250[top250.columns[5:8]].apply(
    lambda x: ','.join( x.dropna().astype(str)),
    axis=1).apply(lambda x: str(x).replace(" ","").replace(","," "))

# Create SQLITE DataBase

conn = sqlite3.connect('marvin.db')  
c = conn.cursor()

dialogs.to_sql('FAQ', conn, if_exists='replace', index = False)
df_top250.to_sql('TOP250', conn, if_exists='replace', index = False)
