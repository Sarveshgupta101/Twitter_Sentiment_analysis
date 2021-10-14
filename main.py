#import modules 
import pandas as pd
import tweepy  # used to acccess twitter API
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from tweepy import Stream
from termcolor import colored
import csv
import re
import sys
import os
from tweepy.streaming import StreamListener
from textblob import TextBlob  # help us to perform actual sentiment analysis
import time  # control time
import matplotlib.pyplot as plt



#basic time effect
time.sleep(1)
i = 5
while i != 0:
    print(colored((f"LOADING... ~ {i} ~"),'red'))
    time.sleep(1)
    i = i-1

class SentimentAnalysis:


    def __init__(self):
        #we create a list for each header
        self.textList = list()
        self.polarityList = list()
        self.subjectivityList = list()
        self.sentimentList = list()

    def DownloadData(self):

        # we can access the API provided by twitter
        twitter_consumer_key = 'type consumer key here'
        twitter_consumer_secret = 'type consumer secret key here'
        twitter_access_token = 'type access token key here'
        twitter_access_token_secret = 'type secert access token key'

       # method of tweepy with unknown code but functionality is in our control, it takes up 2 arguments
        twitter_authentication = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        twitter_authentication.set_access_token(twitter_access_token, twitter_access_token_secret)
        # set_access_tiken sets the access token we got
        api = tweepy.API(twitter_authentication)

        # print Welcome Message...
        print(colored(("Welcome to our application- Cyber_Garuna_Twitter_Sentiment_Analysis:\n"),'green'))



        # we take the input string(word) upon which we are doing sentimental analysis

        searchTerm = input("Enter keyword/hashtag to search about:  ")

        #loop for checking is giving input is int or not?

        while True:

            try:
                NoOfTerms = input("Enter how many tweets to search: ")
                NoOfTerms = int(NoOfTerms)
                break
            except ValueError:
                print("Sorry, I didn't understand that.Please Enter Any Number! ")
            

        
        self.public_tweets = tweepy.Cursor(api.search, q=searchTerm,
                              lang='en').items(NoOfTerms)


               

        # creating some variables to store info 
        polarity = 0                 # polarity means its a measure of how +ve or -ve a text is 
        positive = 0
        negative = 0
        subjectivity = 0             #subjitivity means measure of how much of an opinion it vs how factual 

        for tweet in self.public_tweets:
            txt = tweet.text
            self.textList.append(self.cleanTweet(txt).encode('utf-8'))
            our_analysis = TextBlob(txt)
            polarity  += our_analysis.sentiment.polarity
            subjectivity += our_analysis.sentiment.subjectivity

            self.polarityList.append(polarity)
            self.subjectivityList.append(subjectivity)
            if (our_analysis.sentiment.polarity < 0):
                self.sentimentList.append('Positive')
                positive += 1
            else:
                self.sentimentList.append('Negative')
                negative += 1


            print(txt)
            print('Polarity: ', polarity, "<======+======>", end="")
            print('Subjectivity:', subjectivity)
            print(" ")
            print(" ")  

        dataFrame = pd.DataFrame({'Tweet': self.textList, 'polarity': self.polarityList,
                         'subjectivity': self.subjectivityList, 'Sentiment': self.sentimentList})
        dataFrame.to_csv('result.csv', mode='a', sep=',', encoding='utf-8')

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)

        #finding average reaction
        polarity = polarity / NoOfTerms

         # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")


        if (polarity < 0):
            print("Positive")
        else:
            print("Negative")
 


        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(negative) + "% people thought it was negative")

        self.plotPieChart(positive,negative, searchTerm, NoOfTerms) #shows formatted pichart


        
        
    def cleanTweet(self, txt):
    # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", txt).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')


    #give neccerary values plotPieChart functions 
    def plotPieChart(self, positive,negative, searchTerm, NoOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]','Negative [' + str(negative) + '%]']
        sizes = [positive, negative]
        colors = ['yellowgreen', 'red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing '+ str(NoOfSearchTerms)+' tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

# now lets run it
if __name__ == "__main__":
    sa = SentimentAnalysis()
    downloaddata = sa.DownloadData()