import tweepy  # to gather tweeter data
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
plt.style.use('fivethirtyeight')

# Twitter API Credentials
APIkey = "3OMBrpi6hg5kvQ3Zb1LMFwaEQ"
APISecretKey = "f9fEg3dmaEtqaoZW90MqvElUBV7LvKHOg2zbOPDpmPBvD8BYFt"
accessToken = "1529864260473409545-9wzTxuhcOAc5xwvtpeHYw51NpsQby3"
accessTokenSecreat = "ffiOk1LMVMggUkFvMQKTVtroqQOMhJVfGc1605Iv23Tqy"
# create the object for authentication
Auth = tweepy.OAuthHandler(APIkey, APISecretKey)
Auth.set_access_token(accessToken, accessTokenSecreat)
api = tweepy.API(Auth)
# display
posts = api.user_timeline(
    screen_name='Trump', count=100, tweet_mode='extended')
i = 1
# print(posts)
for tweet in posts[:10]:  # just want to see the top 10 from 100
    print(str(i) + ') ' + tweet.full_text + '\n')
    i = i+1

# Creating dataframe with a column called tweets
df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
print(df)

# make a function to clean tweets


def cleanTxt(text):
    text = re.sub('@[A-Za-z0-9]+', '', text)  # removing mentions
    text = re.sub("#", '', text)  # removing #
    text = re.sub('RT[\s]+', '', text)  # removing Retweets
    text = re.sub('https?:\/\/\S+', '', text)  # removing links
    return text


df['Tweets'] = df['Tweets'].apply(cleanTxt)
print(df)

# sentiments
analysis = TextBlob("Today was the best day ")
analysis.sentiment
# create a function to get the subjectivity of all the tweets


def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# create a function to get the Polarity of all the tweets


def get_polarity(text):
    return TextBlob(text).sentiment.polarity


# create 2 columns 'Subjectivity' and 'Polarity'
df['Subjectivity'] = df['Tweets'].apply(get_subjectivity)
df['Polarity'] = df['Tweets'].apply(get_polarity)
print(df)

# Lets do Analysis

# Word Cloud Visualization
allwords = ' '.join([i for i in df['Tweets']])
Cloud = WordCloud(width=500, height=300, random_state=0,
                  max_font_size=100).generate(allwords)

plt.imshow(Cloud)
plt.show()

# Create a function to compute negative neutral and positive


def getAnalysis(ranking):
    if ranking < 0:
        return 'Negative'
    elif ranking == 0:
        return 'Neutral'
    else:
        return 'Positive'


df['Analysis'] = df['Polarity'].apply(getAnalysis)
print(df)

df[df['Analysis'] == 'Neutral']

df['Analysis'].value_counts()


print(df.shape)

# plotting scatter plot
plt.figure(figsize=(8, 6))
for i in range(0, df.shape[0]):
    plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='Blue')

plt.title("Sentiment Analysis")
plt.xlim(-1, 1)
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()

# Only 3 neutral it is showing because it is overlapping

df['Analysis'].value_counts().plot(kind='bar')
plt.title("Sentiment Analysis")
plt.xlabel('Polarity')
plt.ylabel('Count')
plt.show()

# Lets get positive tweets only
i = 1
sortedDF = df.sort_values(by=['Polarity'], ascending=False)
for j in range(0, sortedDF.shape[0]):
    if (sortedDF['Analysis'][j] == 'Positive'):
        print(str(i) + ') ' + sortedDF['Tweets'][j])
        print()
        i = i+1

# Lets get negative tweets only
i = 1
sortedDF = df.sort_values(by=['Polarity'], ascending=False)
for j in range(0, sortedDF.shape[0]):
    if (sortedDF['Analysis'][j] == 'Negative'):
        print(str(i) + ') ' + sortedDF['Tweets'][j])
        print()
        i = i+1


# Lets get neutral tweets only
i = 1
sortedDF = df.sort_values(by=['Polarity'], ascending=False)
for j in range(0, sortedDF.shape[0]):
    if (sortedDF['Analysis'][j] == 'Neutral'):
        print(str(i) + ') ' + sortedDF['Tweets'][j])
        print()
        i = i+1