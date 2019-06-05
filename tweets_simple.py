from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
import re
import auth_codes
import pandas as pd
import numpy as np


def percentage(part, whole):
    return 100 * float(part)/float(whole)


def clean_tweet(raw_text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", raw_text).split())


def color_risk(val):
    if val > 0:
        color = 'red'
    else:
        pass
    return 'color: %s' % color


auth = tweepy.OAuthHandler(auth_codes.consumer_token, auth_codes.consumer_secret)
auth.set_access_token(auth_codes.access_token, auth_codes.access_secret)

api = tweepy.API(auth)

searchKey = input('Digite a palavra ou hashtag para pesquisar: ')
numTweets = int(input('Digite a quantidade de tweets a serem analisados: '))

tweets = tweepy.Cursor(api.search, lang='pt', q=searchKey).items(numTweets)

positivo = 0
negativo = 0
neutro = 0
polaridade = 0
risco = 0
tweet_list = []
date_list = []
username_list = []
followers_list = []
sentiment_list = []
risk_list = []


for tweet in tweets:
    # Análise do sentimento #
    analysis = TextBlob(clean_tweet(tweet.text))
    polaridade += analysis.sentiment.polarity

    flag = 0

    # Tradução do sentimento #
    if (analysis.sentiment.polarity == 0):
        neutro += 1
        sentimento = 'Neutro'
    elif (analysis.sentiment.polarity < 0):
        negativo += 1
        flag = 1
        sentimento = 'Negativo'
    elif (analysis.sentiment.polarity > 0):
        positivo += 1
        sentimento = 'Positivo'

    # Criação das listas de dados #
    tweet_list.append(tweet.text)
    date_list.append(tweet.created_at)
    username_list.append(tweet.user.screen_name)
    followers_list.append(tweet.user.followers_count)
    sentiment_list.append(sentimento)

    # Análise do risco #
    if (tweet.user.followers_count > 100 and flag == 1):
        risco += 1
        risk_list.append(1)
    else:
        risk_list.append(0)

data = [tweet_list, date_list, username_list, followers_list, sentiment_list, risk_list]
df = pd.DataFrame(np.column_stack(data), columns=['Tweet', 'Data', 'Username', 'Seguidores', 'Sentimento', 'Risco'])

positivo_perc = format(percentage(positivo, numTweets), '.2f')
negativo_perc = format(percentage(negativo, numTweets), '.2f')
neutro_perc = format(percentage(neutro, numTweets), '.2f')

labels = ['Positivo ['+str(positivo_perc)+'%]', 'Negativo ['+str(negativo_perc)+'%]', 'Neutro ['+str(neutro_perc)+'%]']
sizes = [positivo_perc, negativo_perc, neutro_perc]
colors = ['green', 'red', 'yellow']
patches, text = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc='best')
plt.title('Sentimento das pessoas ao termo '+searchKey+' em um total de '+str(numTweets)+' tweets.')
plt.axis('equal')
plt.tight_layout()
plt.show()

print(df.to_string())
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(df)
# df.style.applymap(color_risk, subset=['Risco'])

print('\n')
print(f'Quantidade de tweets de risco: {risco}.')
