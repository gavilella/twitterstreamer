import tweepy
from tkinter import *
from textblob import TextBlob
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import auth_codes
import pandas as pd
import numpy as np
import json
import re
import time

# Authentication #
auth = tweepy.OAuthHandler(auth_codes.consumer_token, auth_codes.consumer_secret)
auth.set_access_token(auth_codes.access_token, auth_codes.access_secret)

# Listas utilizadas #
tweet_list = []
date_list = []
username_list = []
followers_list = []
sentiment_list = []
risk_list = []
positivo_list = []
negativo_list = []
neutro_list = []
numTweets_list = []
positivo_perc_list = []
negativo_perc_list = []
neutro_perc_list = []
searchKey = []


class StreamListener(tweepy.StreamListener):
    """
    Classe geral
    """
    def __init__(self):
        self.api = tweepy.API(auth)
        self.numTweets = 0
        self.numTweets_react = 0
        self.positivo = 0
        self.negativo = 0
        self.neutro = 0
        self.polaridade = 0
        self.risco = 0
        self.tweet = ''
        self.sentimento = ''
        self.username = ''
        self.df = pd.DataFrame()

    # Salvar tweets em arquivo #
    # def on_data(self, raw_data):
    #     with open('tweets.json', 'a') as f:
    #         f.write(raw_data)

    def on_status(self, status, tweet_mode='extended'):
        self.numTweets += 1
        self.flag = 0
        numTweets_list.append(float(self.numTweets))

        # Tweeter API has changed, now it allows more than 280 char.
        # Only tweets with more than 140 char will have the full_text element.
        if hasattr(status, 'retweeted_status'):
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except:
                tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text

        tweet = clean_tweet(tweet)

        # Tradução do sentimento #
        sentiment = sentiment_analysis(tweet)
        if sentiment == 0:
            self.neutro += 1
            neutro_list.append(self.neutro)
            positivo_list.append(self.positivo)
            negativo_list.append(self.negativo)
            sentimento = 'Neutro'
        elif sentiment < 0:
            self.negativo += 1
            neutro_list.append(self.neutro)
            positivo_list.append(self.positivo)
            negativo_list.append(self.negativo)
            self.flag = 1
            sentimento = 'Negativo'
        elif sentiment > 0:
            self.positivo += 1
            neutro_list.append(self.neutro)
            positivo_list.append(self.positivo)
            negativo_list.append(self.negativo)
            sentimento = 'Positivo'

        # Criação das listas de dados #
        tweet_list.append(tweet)
        date_list.append(status.created_at)
        username_list.append(status.user.screen_name)
        followers_list.append(status.user.followers_count)
        sentiment_list.append(sentimento)

        # Análise do risco #
        if status.user.followers_count > 200 and self.flag == 1:
            self.risco += 1
            # risk_list.append(1)
        else:
            pass
            # risk_list.append(0)

        self.df = self.df.append(pd.DataFrame(data=[[tweet, sentimento, status.user.screen_name, self.flag]],
                                              columns=['Tweet', 'Sentimento', 'Username', 'Risco']), ignore_index=True)
        print(self.df.tail(1).to_string(header=False))

        # # GRAFICO PIZZA #
        # Calcula porcentagens  #
        # positivo_perc = percentage(self.positivo, self.numTweets)
        # negativo_perc = percentage(self.negativo, self.numTweets)
        # neutro_perc = percentage(self.neutro, self.numTweets)
        # positivo_perc_list.append(positivo_perc)
        # negativo_perc_list.append(negativo_perc)
        # neutro_perc_list.append(neutro_perc)
        # labels = ['Positivo [' + str(positivo_perc) + '%]', 'Negativo [' + str(negativo_perc) + '%]',
        #           'Neutro [' + str(neutro_perc) + '%]']
        # sizes = [positivo_perc, negativo_perc, neutro_perc]
        # colors = ['green', 'red', 'yellow']
        # patches, text = plt.pie(sizes, colors=colors, startangle=90)
        # plt.legend(patches, labels, loc='best')
        # plt.suptitle('Sentimento das pessoas ao termo ' + searchKey + ' em um total de ' + str(self.numTweets) + ' tweets.')
        # plt.title(f'Tweets de risco encontrados: {self.risco}')
        # plt.axis('equal')
        # plt.tight_layout()
        # plt.pause(0.5)

        # GRAFICO STACKED PORCENTAGEM #
        # Calcula porcentagens  #
        # positivo_perc = percentage(self.positivo, self.numTweets)
        # negativo_perc = percentage(self.negativo, self.numTweets)
        # neutro_perc = percentage(self.neutro, self.numTweets)
        # positivo_perc_list.append(positivo_perc)
        # negativo_perc_list.append(negativo_perc)
        # neutro_perc_list.append(neutro_perc)
        #
        # labels = ['Positivo [' + str('{0:.4}'.format(float(positivo_perc))) + '%]', 'Negativo [' + str('{0:.4}'.format(float(negativo_perc))) + '%]', 'Neutro [' + str('{0:.4}'.format(float(neutro_perc))) + '%]']
        # ax2.clear()
        # ax2.stackplot(numTweets_list, positivo_perc_list, negativo_perc_list, neutro_perc_list, colors=['g', 'r', 'y'], labels=labels)
        # plt.legend(loc='upper left')
        # plt.suptitle('Sentimento das pessoas ao termo ' + searchKey + ' em um total de ' + str(self.numTweets) + ' tweets.')
        # plt.title(f'Tweets de risco encontrados: {self.risco}')
        # plt.xlabel('Tweets')
        # plt.ylabel('Porcentagem')
        # plt.pause(0.5)

        # GRAFICO STACKED PORCENTAGEM SO POS NEG #
        # Calcula porcentagens  #
        self.numTweets_react = self.positivo + self.negativo
        positivo_perc = percentage(self.positivo, self.numTweets_react)
        negativo_perc = percentage(self.negativo, self.numTweets_react)
        positivo_perc_list.append(positivo_perc)
        negativo_perc_list.append(negativo_perc)
        labels = ['Positivo [' + str('{0:.4}'.format(float(positivo_perc))) + '%]', 'Negativo [' + str('{0:.4}'.format(float(negativo_perc))) + '%]']
        ax2.clear()
        ax2.stackplot(numTweets_list, positivo_perc_list, negativo_perc_list, colors=['g', 'r'], labels=labels)
        plt.legend(loc='upper left')
        plt.suptitle('Sentimento das pessoas ao termo ' + searchKey + ' em um total de ' + str(self.numTweets) + ' tweets.')
        plt.title(f'Tweets de risco encontrados: {self.risco}')
        plt.xlabel('Tweets')
        plt.ylabel('Porcentagem')
        plt.pause(0.5)

        # GRAFICO LINHA NUMERO #
        # ax2.clear()
        # ax2.plot(numTweets_list, positivo_list, label='Positivo [' + str(self.positivo) + ']')
        # ax2.plot(numTweets_list, negativo_list, label='Negativo [' + str(self.negativo) + ']')
        # plt.legend(loc='upper left')
        # plt.suptitle(
        #     'Sentimento das pessoas ao termo ' + searchKey + ' em um total de ' + str(self.numTweets) + ' tweets.')
        # plt.xlabel('Tweets')
        # plt.ylabel('Quantidade')
        # plt.title(f'Tweets de risco encontrados: {self.risco}')
        # plt.pause(0.5)


def percentage(part, whole):
    if whole == 0:
        return 0
    else:
        return 100 * float(part) / float(whole)


def sentiment_analysis(tweet):
    tweet = TextBlob(clean_tweet(tweet))
    return tweet.sentiment.polarity


def clean_tweet(raw_text):
    return ' '.join(re.sub("(@)|(\w+:\/\/\S+)", " ", raw_text).split())


def do_stuff():
    searchKey.append(text_input.get())
    root.destroy()


# search_key = input('Digite a palavra ou hashtag para pesquisar: ')

# Builds GUI #
root = Tk()
text_input = StringVar()

question = Label(root, text='Digite a palavra ou hashtag para analisar: ')
text_input_box = Entry(root, textvariable=text_input)

search_btn = Button(root, text='Inciar', command=do_stuff)

question.grid(row=0, column=1, padx=(10, 0), pady=(10, 25))
text_input_box.grid(row=0, column=2, padx=(0, 10), pady=(10, 25))
search_btn.grid(row=1, columnspan=3, padx=(10, 10), pady=(0, 10))

root.title('Analisador de sentimento de Tweets')

root.mainloop()

# Build graph window #
fig = plt.figure()
ax2 = fig.add_subplot(1, 1, 1)

searchKey = searchKey[0]

# Starts streaming tweets #
myStream = tweepy.streaming.Stream(auth, StreamListener())
# Run main class #
go = myStream.filter(languages=['pt'], track=[searchKey])

plt.show()
