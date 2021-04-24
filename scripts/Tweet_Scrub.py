# This is a sample Python script.
import pandas as pd
import numpy as np
from textblob import TextBlob
import nltk
import regex as re

#nltk.download("stopwords")
#nltk.download("wordnet")
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

def add_to_dict(dict,text):
    first, *middle, last = text.split()
    #endx = sum(end)
    recombined = middle+[last]
    ending=""
    for word in recombined:
        ending=ending+word + " "
    #print(first,'added as',ending)
    dict[first]=ending

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def sent_analysis(Tweet):
    tweet = Tweet.lower()
    tokenized_text = tokenizer.tokenize(tweet)
    words = [lemmatizer.lemmatize(w) for w in tokenized_text if w not in stop_words]
    stem_text = " ".join([stemmer.stem(i) for i in words])
    analysis = TextBlob(stem_text)
    Grade = analysis.sentiment.polarity
    return Grade

def regex_tweet(tweet):
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", tweet).split())
    tweet = ' '.join(re.sub("(\w+:\/\/\S+)", " ", tweet).split())
    tweet = ' '.join(re.sub("[\.\,\!\?\:\;\-\=]", " ", tweet).split())
    tweet = ' '.join(re.sub("[\[\]]", " ", tweet).split())
    return tweet

def scrub_tweet(tweet,emojipedia):
    tweet_reborn = ""
    tweet_split = tweet.split()
    for word in tweet_split:
        if word in emojipedia.keys():
            word = emojipedia[word]
        tweet_reborn = tweet_reborn + word + " "
    return tweet_reborn



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    emojipedia = {}
    f = open("emojipedia.txt", encoding="utf8")
    Lines = f.readlines()
    for line in Lines:
        add_to_dict(emojipedia, line.strip())

    tokenizer = RegexpTokenizer('\s+', gaps=True)
    stop_words = stopwords.words("english")
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    lemmatizer = WordNetLemmatizer()
    df = pd.read_csv('bitcoin.csv',dtype={'conversation_id':str,
                                          'timezone':str,
                                          'photos':str,
                                          'user_id':str,
                                          'replies_count':str,
                                          'retweets_count':str,
                                          'likes_count':str,
                                          'video':str,
                                          'near':str,
                                          'geo':str,
                                          'source':str,
                                          'user_rt_id':str,
                                          'user_rt':str,
                                          'retweet_id':str,
                                          'reply_to':str,
                                          'trans_src':str,
                                          'trans_dest':str,
                                          'retweet_date':str,
                                          'translate':str})
    df=df.drop(['name','place','quote_url','near','geo','user_rt','retweet_id','retweet_date','translate','trans_src','trans_dest','source','thumbnail','user_rt_id'],axis=1)
    index_names = df[df['language'] != 'en'].index
    df.drop(index_names, inplace=True)
    df = df.drop(['conversation_id','timezone','language','mentions','urls','photos','replies_count','retweets_count','likes_count','retweet','video','reply_to'], axis=1)
    df['regex_tweet'] = df.apply(lambda row: regex_tweet(row['tweet']), axis=1)
    df['scrubbed_tweet']=df.apply(lambda row: scrub_tweet(row['regex_tweet'],emojipedia),axis=1)
    df['sentiment'] = df.apply(lambda row: sent_analysis(row['scrubbed_tweet']),axis = 1)
    compression_opts = dict(method='zip',
                            archive_name='out3.csv')
    df.to_csv('out3.zip',index=False, compression=compression_opts)
    print(df.count())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
