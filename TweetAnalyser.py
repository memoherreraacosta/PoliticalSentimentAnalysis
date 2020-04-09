# !/usr/bin/env python3
from tweepy.streaming import StreamListener, TweepError
from classifier import SentimentClassifier

import numpy as np
import pandas as pd

import TwitterClient


ACCOUNTS_FILE = "accounts.csv"
RESULTS_FILE = "results.csv"
RESULTS_DIR = "Account_results/"



class TweetAnalyser():

    def read_file(self, file):
        with (file,"r+") as f:
            print("Readind file : [ {0} ]".format(file))
            content = f.read()
            print("File : [ {0} ] is read".format(file))
            return content.splitlines()


    def write_in_file(self, file_to_write, input_text_list):
        with (file_to_write, "w+") as f:
            f.write("\n".join(input_text_list))


    def isRelevant(self, text):
        key_words = [
            "amlo", "@lopezobrador_","lópez obrador",
            "lopez obrador","4t","andrés manuel","andres manuel",
        ]

        text = text.lower()
        is_relevant = False
        counterWords = 0

        for key_word in key_words:
            if key_word in text:
                is_relevant = True
                break

        return is_relevant
    
    
    def getPostura(self, text):
    # Metodo adoptara una postura en base a palabras clave por tweet    
        text = text.lower()
        clf = classifier.SentimentClassifier()
        value = clf.predict(text)

        if(value > .45):
            return 1
        elif(value > .3):
            return 0
        else:
            return -1


    def posturaFinal(self, positions):
        # posturas is a list
        account_position = sum(positions)

        if(len(positions)>0):
            return "There are not enough data to analyze the account"

        if(sum > 0):
            return "Follower"
        elif(sum < 0):
            return "Opposition"
        else:
            return "Neutral"


    def tweets_to_data_frame(self, tweets):

        text = []
        id = []
        tweet_len = []
        likes = []
        rt = []
        position = []

        for tweet in tweets: 
            if not tweet.retweeted and TweetAnalyser.isRelevant(tweet.text):
                text.append(tweet.text)
                id.append(tweet.id)
                tweet_len.append(len(tweet.text))
                likes.append(tweet.favorite_count)
                rt.append(tweet.retweet_count)
                position.append(TweetAnalyser.getPostura(tweet.text))

        data = {
            "id": id,
            "text": text,
            "len tweet": tweet_len,
            "likes": likes,
            "rt": rt,
            "postura": position
        }

        return pd.DataFrame(data)


def __main__(self):
    twitterclient = TwitterClient()
    api = twitterclient.getTwitterClientAPI()    

    accounts = self.read_file(ACCOUNTS_FILE)
    print("Mining accounts ...")
    results = []
    num_accounts = len(accounts)
    accounts_counter = 0

    for account in accounts:
        print("Computing account ={0}\n".format(account))
        if account == "":
            break
        # Print progress of computing
        accounts_counter += 1
        procces_completed = str(int((accounts_counter/num_accounts)*100))
        print(
            "Process completed [ {0}% ] for account '{0}'"\
            .format(procces_completed,accounts)
        )

        try:
            tweets = api.user_timeline(
                screen_name=account,
                count = 1000
            )

            df = self.tweets_to_data_frame(tweets)
            account_result_file = "{0}{0}.csv".format(RESULTS_DIR, account)
            df.to_csv(
                account_result_file,
                encoding='utf-8',
                index=False
            )

            results.append(
                "{0},{0}"\
                .format(account, TweetAnalyser.posturaFinal(df['postura']))
            )

        except TweepError as err:
            print("The account [ {0} ] is private, skipping...".format(account))

    print("Tweets almacenados correctamente en la carpeta")
    print("Guardando resultados en [ {0} ]".format(RESULTS_FILE))
    self.write_in_file(RESULTS_FILE, results)
    print("Resultados guardados en [ {0} ]".format(RESULTS_FILE))
    print("Computo terminado")