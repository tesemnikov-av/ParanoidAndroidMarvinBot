![contributors](https://img.shields.io/github/contributors/tesemnikov-av/pelevin-recomendation-bot) ![last-commit](https://img.shields.io/github/last-commit/tesemnikov-av/Pelevin-recomendation-bot) ![repo-size](https://img.shields.io/github/repo-size/tesemnikov-av/Pelevin-recomendation-bot)

![watch](https://img.shields.io/github/watchers/tesemnikov-av/Pelevin-recomendation-bot?style=social) 


ParanoidAndroidMarvinBot
------------
version 0.1

Try in Telegram:

    @ParanoidAndroidMarvinBot

[comment]: ![Marvin](https://github.com/tesemnikov-av/files-rep/blob/master/marvin_logo.png)

Если Марвину отправить название известного ему фильма (топ250 Кинопоиска), то он порекомендует Вам похожий (На основе общих создателей).
В названии фильма допускаются три опечатки (Расстояние Левенштейна ).
В остальных случаях Марвин выбирает ответ на основе базы вопросов и ответов «Frequently Asked Questions».
Для определения ответа и фильма расчитывается косинусное растояние и выбирается ответ с максимальным сходством.
Если сходство ниже определенного предела Марвин не отвечает.

Пример 1            |  Пример 2
:-------------------------:|:-------------------------:
![Yes](https://github.com/tesemnikov-av/files-rep/blob/master/marvin1.jpg)  |  ![No](https://github.com/tesemnikov-av/files-rep/blob/master/marvin2.jpg)

# Used libraries:

 - Sklearn (Tf-Idf)
 - Nltk
 - Pymorphy2
 - PyTorch
 - Numpy
 - Pandas

