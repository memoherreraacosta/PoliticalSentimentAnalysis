# !/usr/bin/env python3
import credentials
import tweepy #https://github.com/tweepy/tweepy



class TwitterClient():
    def __init__(self, twitter_user=None):
        auth = tweepy.OAuthHandler(
            credentials.CONSUMER_KEY,
            credentials.CONSUMER_SECRET
        )

        self.auth.set_access_token(
            credentials.ACCESS_TOKEN,
            credentials.ACCESS_TOKEN_SECRET
        ).Authenticate_Twitter_app()

        self.twitter_client = tweepy.API(self.auth)
        self.twitter_user = twitter_user


    def getTwitterClientAPI(self):
        return self.twitter_client


    def getUserTimelineTweets(self, numTweets):
        return [
            tweet
            for tweet in tweepy.Cursor(
                self.twitter_client.user_timeline,
                id = self.twitter_user).items(numTweets)
        ]


    def getFriendList(self, numFriends):
        return [
            friend
            for friend in tweepy.Cursor(
                self.twitter_client.friends,
                id = self.twitter_user).items(numFriends)
        ]


    def getHomeTimeline(self, numTweets):
        return [
            tweet
            for tweet in tweepy.Cursor(
                self.twitter_client.home_timeline,
                id = self.twitter_user).items(numTweets)
        ]