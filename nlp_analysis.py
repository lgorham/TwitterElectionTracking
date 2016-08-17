import nltk
# from nltk.classify import NaiveBayesClassifier
# from nltk.tokenize import TweetTokenizer
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
import sys
from model import Tweet
 
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def vader_sentiment_analysis():
    """
    Takes in a list of tweets, and uses vaderSentiment() to represent the 
    amount of positive, negative and neutral sentiments expressed in the tweet.
    Returns the compounded sentiment value as a positive or negative number that 
    expresses overall sentiment polarity
    """

    tweets = Tweet.query.all()
    for tweet in tweets:
        sentiment_results = vaderSentiment(tweet.text)
        print "Tweet: {} \n Results: {}".format(tweet.text, str(sentiment_results))



# tweet_list = ["My interview on CNN... Four years of Hillary Clinton is better than one day of Donald Trump as president.", 
#             "So we just learned that Trump dates beautiful women. Big deal! Thank you, NYT, for your 'investigative reporting'! Bunch of morons",
#             "Trump belly flops all over the place about everything and everyone. Hard to pin him down. He's a slippery salesman.",
#             "#Trump is bad because he raised $5.6 mill for vets.  #HillaryClinton's NOT BAD because she misplaced $6.9 billion while Secretary of State.",
#             "@RedState Whats wrong with you people? Trump is the only hope I've had in years to save the Republic. You must live in an alternate universe",
#             "Got to love the cowards that change Trump's user name by a letter or two. Two talk there smack. They are so lame!!!",
#             "@realDonaldTrump This is a brave guy and I give him a lot of credit. Trump haters are mindless hate filled people.",
#             "@HillaryClinton Hillary Clinton is so full of crap, she is a toilet. Bill get your plunger hopefully this can clear her blocked pipes.",
#             "And Donald Trump thinks he's a good presidential candidate. No thanks to both!",
#             "@realDonaldTrump trump u fucking liar &racist people must have sick brain to support you",
#             "Former Ambassador says Hillary Clinton is 'Responsible' for the Benghazi Murders! #TPOL #HilaryLies #Duh",
#             "Heard some fool say Trump's vet donations was a scam.  Yeah right!  Because guy worth 10 billion is gonna publicly steal a few millions."]


vader_sentiment_analysis()