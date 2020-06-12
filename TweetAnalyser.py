# !/usr/bin/env python3
from tweepy import TweepError
from TwitterClient import TwitterClient
from classifier import SentimentClassifier

import pandas

ACCOUNTS_FILE = "accounts.csv"
RESULTS_FILE = "results.csv"
RESULTS_DIR = "DatosFuentes/"
KEY_WORDS = [
    "amlo",
    "@lopezobrador_",
    "lópez obrador",
    "lopez obrador",
    "4t",
    "andrés manuel",
    "andres manuel",
]



class TweetAnalyser():

    def __init__(self):
        self.twitter_client = TwitterClient()
        self.api = self.twitter_client.getTwitterClientAPI()
        self.accounts = self.read_file()
        self.results = []
        self.accounts_counter = 0


    def read_file(self):
        with open(ACCOUNTS_FILE, "r") as f:
            print("Readind file : [ {0} ]".format(ACCOUNTS_FILE))
            content = f.read()
            print("File : [ {0} ] is read".format(ACCOUNTS_FILE))
            return content.splitlines()


    def write_in_file(self, input_text_list):
        with open(RESULTS_FILE, "w") as f:
            f.write("\n".join(input_text_list))


    def is_relevant(self, text):
        text = text.lower()
        return any(
            key_word
            for key_word in KEY_WORDS
            if key_word in text
        )

    
    def get_position(self, text): 
        text = text.lower()
        text = text.split("http")[0]
        return 0
        """
        clf = SentimentClassifier()
        value = clf.predict(text)

        if value > .55:
            return 1
        elif value < .35 :
            return -1
        else:
            return 0
        """


    def final_position(self, positions):
        if len(positions) == 0:
            return "There are not enough data to analyze the account"

        account_position = sum(positions)/len(positions)
        if account_position > .15 :
            return "Follower"
        elif account_position < -.15:
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
            if not tweet.retweeted and self.is_relevant(tweet.text):
                text.append(tweet.text.split("http")[0])
                id.append(tweet.id)
                tweet_len.append(len(tweet.text))
                likes.append(tweet.favorite_count)
                rt.append(tweet.retweet_count)
                position.append(self.get_position(tweet.text))

        data = {
            "id": id,
            "text": text,
            "len tweet": tweet_len,
            "likes": likes,
            "rt": rt,
            "position": position
        }
        return pandas.DataFrame(data)


    def worker(self):
        for account in self.accounts:
            print("Computing account = {0}".format(account))
            if account == "":
                break
            # Print progress of computing
            self.accounts_counter += 1
            procces_completed = str(
                int(
                    (self.accounts_counter/len(self.accounts))*100
                )
            )
            print(
                "Process completed [ {0}% ]"\
                .format(procces_completed)
            )
            try:
                tweets = self.api.user_timeline(
                    screen_name=account,
                    count = 1000
                )

                df = self.tweets_to_data_frame(tweets)
                account_result_file = "{0}{1}.csv".format(RESULTS_DIR, account)
                df.to_csv(
                    account_result_file,
                    encoding='utf-8',
                    index=False
                )

                self.results.append(
                    "{0},{1}".format(account, self.final_position(df["position"]))
                )
            except TweepError as err:
                print("The account [ {0} ] is private, skipping...".format(account))


    def main(self):
        print("Mining accounts ...")
        self.worker()
        print("Tweets saved in directory")
        print("Saving results in [ {0} ]".format(RESULTS_FILE))
        self.write_in_file(self.results)
        print("Process finished")

if __name__ == '__main__':
    TweetAnalyser().main()