![contributors](https://img.shields.io/github/contributors/tesemnikov-av/pelevin-recomendation-bot) ![last-commit](https://img.shields.io/github/last-commit/tesemnikov-av/Pelevin-recomendation-bot) ![repo-size](https://img.shields.io/github/repo-size/tesemnikov-av/Pelevin-recomendation-bot)

![watch](https://img.shields.io/github/watchers/tesemnikov-av/Pelevin-recomendation-bot?style=social) 


ParanoidAndroidMarvinBot
------------
version 0.1

Try in Telegram:

    @ParanoidAndroidMarvinBot

[comment]: ![Marvin](https://github.com/tesemnikov-av/files-rep/blob/master/marvin_logo.png)

Если Марвину отправить название известного ему фильма (топ250 Кинопоиска), то он порекомендует Вам похожий.
В названии фильма допускаются три опечатки (Расстояние Левенштейна ).
В остальных случаях Марвин выбирает ответ на основе базы вопросов и ответов «Frequently Asked Questions».
Для каждого заданного вопроса расчитывается косинусное растояние и выбирается ответ с максимальным сходством.
Если сходство ниже определенного предела Марвин не отвечает.

# Used libraries:

 - Sklearn (tfidf)
 - Nltk
 - Pymorphy2
 - PyTorch
 - Numpy
 - Pandas
 
```python

        elif command == 'Hi' or command == 'hi' or command == 'HI' or command == 'hI':     #Hi Query
            replyMessage = "Hi "+ user + " "
            greeting = "It is sleeping time you still awake"
            hour = int(datetime.datetime.strftime(datetime.datetime.now(), '%H'))
            #print(hour)
            if(hour >= 4 and hour < 12):
                greeting = "Good Morning"
            elif(hour >= 12 and hour < 16):
                greeting = "Good Afternoon"
            elif(hour >= 16 and hour < 20):
                greeting = "Good Evening"
```
 
 run.py
 ------
 
    Основной файл для запуска
    
 recomendations.py 
 -----------------
 
    Здесь описаны две системы для рекомендации фильм. 
       - На основе создателей фильма (tfidf и косинусная мера)
       - На основе описания фильма (Word2Vec и ??)
