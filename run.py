# -*- coding: utf-8 -*-
import pandas as pd
import telebot
from docxtpl import DocxTemplate
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('movie.csv')

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['common'])
from sklearn.metrics.pairwise import linear_kernel
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df.index, index=df['original_title']).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df['original_title'].iloc[movie_indices]

bot = telebot.TeleBot('1175849304:AAFJDNgX66_NXfys1wZzWTz4feAxsPdmvoA')
#keyboard1 = telebot.types.ReplyKeyboardMarkup()
#keyboard1.row('Привет', 'Пока')




@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'For find in Wikipedia \n Example: "wiki deaths" for full output or "w deaths" for short output' ) # , reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower().split(' ')[0] == 'rec':
        #telebot.
        #user = update.message.from_user
        bot.send_message(message.chat.id,  str(get_recommendations('The Hateful Eight').values).strip('[]').replace("' '" , '\n').replace("'" , "").strip()     ) #    str(get_recommendations('The Hateful Eight')) )
        #print('You talk with user {} and his user ID: {} '.format(user['username'], user['id']))
    elif message.text.lower().split(' ')[0] == 'r':
        bot.send_message(message.chat.id, str(get_recommendations(str(message.text.split(' ')[1]))))
    elif message.text.lower().split(' ')[0] == 'w':
        try:
          content = str(wikipedia.summary(message.text.lower().split(' ')[1:]))
          summary = summarize(content, split=True, word_count=50)
        except BaseException as e:
          summary = "Попробуй еще"
        bot.send_message(message.chat.id, str(summary) )
    elif message.text.lower().split(' ')[0] == 'wiki':
        #content = str()
        #summary = summarize(content, split=True, word_count=100)
        try:
          content = wikipedia.summary(message.text.split(' ')[1:])
        except BaseException as e:
          content = "Попробуй еще"        
        bot.send_message(message.chat.id, content )
    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    elif message.text.lower().split(' ')[0] == 'пропуск':
        try:
          name = str(message.text.lower().split(' ')[1])
          serial_number = str(message.text.lower().split(' ')[2])
          ZNI = str(message.text.lower().split(' ')[3])
          date = str(message.text.lower().split(' ')[4])
          context = { 'NAME' : name , 'SERIAL_NUMPER' : serial_number, 'ZNI':ZNI, 'DATE':date}
        
          doc = DocxTemplate("Шаблон_python.docx")
        
          doc.render(context)
          doc.save("внос_Сколково_" + date + ".docx")
        #files.download('шаблон-final.docx')
          docum = open("внос_Сколково_" + date + ".docx", 'rb')
        #docum = open('sample_data/README.md', encoding="utf-8")
          bot.send_document(message.chat.id,docum  )
          bot.send_message(message.chat.id, 'Лови файл')
        except BaseException as e:
          bot.send_message(message.chat.id, 'пример: пропуск VRM 00FF540 --- 23.03.2020')
    else : 
        #bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
        bot.send_message(message.chat.id, 'пример: пропуск VRM 00FF540 --- 23.03.2020')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)

bot.polling()
