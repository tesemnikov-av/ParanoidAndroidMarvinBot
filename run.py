from datetime import datetime
import Levenshtein
import pandas as pd
import nltk 
import numpy as np
import re
from nltk.stem import wordnet # to perform lemmitization
from sklearn.feature_extraction.text import CountVectorizer # to perform bow
from sklearn.feature_extraction.text import TfidfVectorizer # to perform tfidf
from nltk import pos_tag # for parts of speech
from sklearn.metrics import pairwise_distances # to perfrom cosine similarity
from nltk import word_tokenize # to create tokens
from nltk.corpus import stopwords # for stop words
import telebot
import random
import time
from sklearn.metrics.pairwise import linear_kernel
import pymorphy2
import string

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

morph = pymorphy2.MorphAnalyzer()
tfidf = TfidfVectorizer()

LEV_DIST = 4

bot = telebot.TeleBot('1171053774:AAEKARUcqloBdKpZyT9_g4jnIKDcOUJYOKU')

def random_movie():
    return df_top250['original_title'][random.randint(0,len(df_top250['original_title'])-1)]

def get_bet_elem():
    return random_movie().capitalize()
  
def get_button():
    keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
    return keyboard1.row(get_bet_elem(),get_bet_elem(),get_bet_elem())
    del keyboard1

def get_elem(elem):
    return elem[random.randint(0, len(elem)-1)]

def greating():
    hour = int(datetime.strftime(datetime.now()  , '%H')) + 3

    if(hour >= 4 and hour < 12):
       greeting = "Доброе утро!"
    elif (hour >= 12 and hour < 16):
       greeting = "Добрый день!"
    elif (hour >= 16 and hour < 23):
       greeting = "Добрый вечер!"
    return greeting

def chat_tfidf(text):
    lemma=tokenize_ru(text) # calling the function to perform text normalization
    tf=tfidf.transform([lemma]).toarray() # applying tf-idf
    cos=1-pairwise_distances(df_tfidf,tf,metric='cosine') # applying cosine similarity
    index_value=cos.argmax() # getting index value 
    return df_dialogs['Text Response'].loc[index_value]

def get_recommendations(title, cosine_sim=cosine_sim_creators ):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    a = df_top250['url'].iloc[movie_indices]
    return str(a.values[random.randint(0,9)].capitalize())[1:-1] # a.values , sim_scores

def tokenize_ru(file_text):
    tokens = word_tokenize(file_text)
    tokens = [i for i in tokens if (i not in string.punctuation)]
    tokens = [i for i in tokens if (i not in my_stop_words)]
    tokens = [i.replace("«", "").replace("»", "") for i in tokens]
    tokens = [ morph.parse(i)[0].normal_form for i in tokens ]
    return str(tokens).strip('[]').replace("'","").replace(",","")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, greating() )
    bot.send_sticker(message.chat.id, get_elem(stickers_ids) )
    bot.send_message(message.chat.id, get_elem(questions) , parse_mode="markdown" , reply_markup=get_button() ) 

@bot.message_handler(content_types=['text'])
def send_text(message):
    recomended = False

    for film in list(df_top250['original_title_lower']):
      ldis = Levenshtein.distance(message.text.lower(), film)
      if ldis < LEV_DIST:
        recomended = True
        bot.send_photo(message.chat.id, get_recommendations(str(film)))
       
    if recomended != True:
   
        bot.send_message(message.chat.id, chat_tfidf(message.text.lower()) , reply_markup=get_button())

        if bool(random.choices([True, False], weights=[40, 60])[0]):
          bot.send_sticker(message.chat.id, get_elem(stickers_ids) )

bot.polling()
