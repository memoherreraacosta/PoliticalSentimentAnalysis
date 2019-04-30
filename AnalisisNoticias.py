import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from classifier import *

import twitter_credentials
import numpy as np
import pandas as pd

class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().Authenticate_Twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def getTwitterClientAPI(self):
        return self.twitter_client

    def getUserTimelineTweets(self, numTweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(numTweets):
            tweets.append(tweet)
        return tweets

    def getFriendList(self, numFriends):
        friends = []
        for friend in Cursor(self.twitter_client.friends, id = self.twitter_user).items(numFriends):
            friends.append(friend)
        return friends

    def getHomeTimeline(self, numTweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id = self.twitter_user).items(numTweets):
            tweets.append(tweet)
        return tweets

class TwitterAuthenticator():
    def Authenticate_Twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TweetAnalyser():
    #Analisis y categorizado de contenido de Tweets

    def isRelevant(text):
        keyWords = ["amlo", "@lopezobrador_","lópez obrador",
                    "presidente","lopez obrador","ejecutivo","4t",
                    "andrés manuel","andres manuel"]

        trendingTopics = ["mañanera","mexico","méxico","@sre_mx","@m_ebrard"]

        relevantWords = keyWords + trendingTopics
        text = text.lower()
        isrelevant = False
        counterWords = 0

        for i in relevantWords:
            if(i in text):
                counterWords += 1
                if(counterWords > 2):
                    isrelevant = True
                    break
        
        return isrelevant
    
    def getPostura(texto):
    # Metodo adoptara una postura en base a palabras clave por tweet    
        texto = texto.lower()

        clf = SentimentClassifier()
        value = clf.predict(texto)

        if(value > .50):
            return 1
        elif(value > .30):
            return 0
        else:
            return -1

        '''
        favorWords = ["igualdad","éxito","exito","gusto","haciendo","fortuna",
                      "ayudemos","paz","de primera","aliado","respeto","confianza",
                      "excelente","mejor","crece","sustentable","sana","fortalecido",
                      "bienestar","justicia","celebra","tranquilidad","feliz","prian",
                      "buen","ahorro","trabajo"]

        notFavorveWords = ["ridiculez","violento","violencia","desalmados",
                           "mezquinos","despreciable","carajo","incompetentes","torpe",
                           "corrupción","capricho","enemigo","secuestro","asesinada",
                           "lamentable","fracaso","impunidad","secuestrar","secuestros",
                           "asesinado","asesinatos","tortura","patético","criticar",
                           "críticar","compadre","conflicto de interés","dolor","ineptos",
                           "provocador","inepto","vergüenza","inflación"]

        posCount = 0
        negCount = 0

        for i in favorWords:
            if(i in texto):
                posCount += 1
        
        for i in notFavorveWords:
            if(i in texto):
                negCount += 1

        res = posCount - negCount
        
        if(res < 0):
            return -1
        else:
            return 1
        '''

    def posturaFinal(postura):
        # postura is a list
        sum = 0
        for i in postura:
            sum += i

        if(sum == 0 and len(postura)>0):
            return "Neutral"
        
        if(sum > 0):
            return "A favor"
        elif(sum < 0):
            return "En contra"
        else:
            return "No hay suficientes elementos para determinar una postura"


    def tweets_to_data_frame(self,tweets):

        text = []
        id = []
        lon = []
        likes = []
        rt = []
        postura = []

        for tweet in tweets: 
        
            if (not tweet.retweeted and TweetAnalyser.isRelevant(tweet.text)):
                text.append(tweet.text)
                id.append(tweet.id)
                lon.append(len(tweet.text))
                likes.append(tweet.favorite_count)
                rt.append(tweet.retweet_count)
                postura.append(TweetAnalyser.getPostura(tweet.text))

        data = {'id':id,'text':text,'len tweet':lon,'likes':likes,'rt':rt, 'postura':postura}
        df = pd.DataFrame(data)
        # print(df.count())
        # print()

        return df 


if __name__ == "__main__":

    fileToRead = "fuentes.csv"
    finalFile = "resultados.csv"
    dirToSaveName = "DatosFuentes/"


    fileL = open(fileToRead,"r+")

    if fileL.mode == "r+":
        print("Readind file : [ "+fileToRead+" ]")
        content = fileL.read()
        fuentes = content.split("\n")
    
    fileL.close()

    print("File : [ "+fileToRead +" ] is read")

    twitterclient = TwitterClient()
    tweet_analyser = TweetAnalyser()
    api = twitterclient.getTwitterClientAPI()

    print("Minando fuentes ...")

    resultado = []

    for fuente in fuentes:
        #print(fuente)
        if fuente == "":
            break
        try:
            tweets = api.user_timeline(screen_name=fuente, count = 1000)
            df = tweet_analyser.tweets_to_data_frame(tweets)
    
            archivo = dirToSaveName + fuente + ".csv"
            df.to_csv(archivo,encoding='utf-8', index=False)

            resultado.append(fuente+","+TweetAnalyser.posturaFinal(df['postura'])+"\n")

        except tweepy.TweepError as err:
            print("La cuenta [ " + fuente + " ] está protegida, saltando cuenta...")
            #print(str(err))

    print("Tweets almacenados correctamente en la carpeta")
    
    print("Guardando resultados en [ "+finalFile+" ]")
    fFile = open(finalFile,"w+")

    if fFile.mode == "w+":
        for i in resultado:
            fFile.write(i)
    
    fFile.close()
    print("Resultados guardados en [ "+finalFile+" ]")

    print("Computo terminado")
