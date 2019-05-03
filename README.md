# Sentiment Analysis : An approval analysis of current President of Mexico based on Tweets

**Political Analysis**

This project consists in make an analysis of the political posture of an account in [Twitter](https://twitter.com/) based on tweets relationated to the target [Andrés Manuel López Obrador](https://twitter.com/lopezobrador_), current president of Mexico. This analysis is for tweets in Spanish language. 

In the repository we'll see how we :

1. Do the connection to an API to mine tweets from a set of accounts
2. Filter those tweets in relevant content
3. For each tweet ponderate with a value based on how probably is that the tweet has a positive, negative or neutral opinion to the target (Andrés Manuel)
4. For each account, analize their approval opinion based on the results of their tweets
5. Give a result of the approval opinion to the account's set

-----

# Requirements

- [Python3](https://www.python.org/) 
- [Tweepy](http://www.tweepy.org/)
- [pandas](https://pandas.pydata.org/)
- [numpy](https://www.numpy.org/)
- [nltk](https://www.nltk.org/), if you have troubles in the instalation, check [this](https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed) solution.
- [sklearn](https://scikit-learn.org/stable/)
- [marisa-trie](https://marisa-trie.readthedocs.io/en/latest/)
- [scipy](https://www.scipy.org/)
- [senti-py analizer](https://github.com/aylliote/senti-py)


# Data

- [Fuentes](fuentes.csv) is a csv file that represents the set account to mine, each Twitter Account will be separated by a linebreake
- [DatosFuentes](DatosFuentes/) is a directory where it stores the result of data mined in a csv file
- File of 'DatosFuentes', example of [Víctor Trujillo](DatosFuentes/V_TrujilloM.csv). Each file has a set of tweets filtered by relevance of the project; Those tweets has an 'ID', 'Text', 'len tweet', # of 'likes', # of retweets 'rt', posture of the tweet 'postura'. 
- [Resultados](resultados.csv) is a csv file where stores the result of the posture of the account's set ([Fuentes](fuentes.csv)). This file has the 'account id' and 'posture' for each account processed.  


# Algorithm's Process and Result

+ Data Mining : All the tweets are obtained by [Tweepy API](http://www.tweepy.org/), this process is well explained in [LucidProgramming tutorials](https://www.youtube.com/playlist?list=PL5tcWHG-UPH2zBfOz40HSzcGUPAVOOnu1) and adapted to our context in [AnalisisNoticias.py](AnalisisNoticias.py).

+ Data Filtering : To filter all the tweets mined in relevant ones, we choose only those which has words related to the target ([Andrés Manuel López Obrador](https://twitter.com/lopezobrador_)), those words are : `"amlo", "@lopezobrador_","lópez obrador","presidente","lopez obrador","ejecutivo","4t","andrés manuel","andres manuel"`. This process is `isRelevant()` method inside the `TweetAnalyser` anonymous class inside the [AnalisisNoticias.py](AnalisisNoticias.py) class.
Those filtered tweets are stored in [DatosFuentes](DatosFuentes/) for each account in csv format. 

+ Data Processing : To process the tweets and rate them if has positive, negative or neutral content we use the [senti-py analizer](https://github.com/aylliote/senti-py), this computing is shown in `getPostura()` method inside the `TweetAnalyser` anonymous class inside the [AnalisisNoticias.py](AnalisisNoticias.py) class. The tweet's data is stored in the [DatosFuentes](DatosFuentes/) directory, the data's format is a csv file where it describes the `id, text itself, len of the text, # of likes, # of retweets and posture of the tweet`. here is an example of [Víctor Trujillo](DatosFuentes/V_TrujilloM.csv).

+ Data Analysis : Once we have the posture for each tweet, we rate them all and compute the account's posture based on the proportion of positive, negative or neutral tweets that the account has. This process is in `posturaFinal()` method inside the `TweetAnalyser` anonymous class inside the [AnalisisNoticias.py](AnalisisNoticias.py) class. This information is saved in a csv file named [Resultados](resultados.csv) where stores the result of the posture of the account's set ([Fuentes](fuentes.csv)).


# Conclusion

We conclude that not all the results are accurate, one of the main problems of the analysis is the sarcasm. Is hard to analyze wether a comment has a positive or negative reference when they write in a sarcastic way. This style can be described as a [Black Swan effect](https://en.wikipedia.org/wiki/Black_swan_theory) in the Data Analysis stage. We also know that the project is in development, so there are methods and implementantions that can be improved so the algorithm can be more accurate when it define a posture.


# How to run it ?

* To run the program follow the next steps in your terminal :

1. Be sure to have installed the libraries mentioned in the [Requirements] section in this README file.

2. Download the repository :

`````
    $ git clone https://github.com/memoherreraacosta/PoliticalSentimentAnalysis.git
`````

3. Get in the directory PoliticalSentimentAnalysis just downloaded :

`````
    $ cd PoliticalSentimentAnalysis
`````

4. To run the Python3 program that does the magic, follow this command :

`````
    $ python3 AnalisisNoticias.py
`````

* Remember that you can change the accounts that you want to analize in the [fuentes.csv](fuentes.csv) file follwing the format of linebreak per account. 

* To remove the [resultados.csv](resultados.csv) file from your repository and all the files of the accounts analized in [DatosFuentes](DatosFuentes/) directory, run this command on your terminal being on the `PoliticalSentimentAnalysis` directory: 

`````
    $ rm resultados.csv && cd DatosFuentes/ && rm *.csv && cd ..
`````