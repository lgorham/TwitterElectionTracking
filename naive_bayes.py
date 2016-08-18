import numpy
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import BernoulliNB
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
import re


def load_training_data():
    """
    Load and clean training tweets for classification

    Pre-classified tweets are a random sample from the scraped tweets
    relating to the 2016 presidential candidates, so that the classifier is trained
    on words found in the political opinion domain.

    Returns two lists: one with the text from the tweet, and the other with the
    correspondence valence of the tweet
    """

    tweet_text = []
    tweet_sentiment = []
    positive_tweets = open("seed_data/positive_training_tweets.txt")
    negative_tweets = open("seed_data/negative_training_tweets.txt")
    tweets = [positive_tweets, negative_tweets]
    for tweet in tweets:
        for t in tweet:
            t = t.lower().rstrip()
            t = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL', t)

            #replacing candidate names so as not to have candidate names affect classifier
            t = t.replace('trump', 'CANDIDATE')
            t = t.replace('clinton', 'CANDIDATE')
            tweet_text.append(t)
            if tweet == positive_tweets:
                tweet_sentiment.append('pos')
            if tweet == negative_tweets:
                tweet_sentiment.append('neg')



    return tweet_text, tweet_sentiment


def preprocess_training():
    """
    Create a frequency matrix for the review data set

    Converts tweet text into a matrix of token counts, and then uses a term
    frequency transformer in order to reduce the impact of commonly used tokens
    (such as 'and', 'the') that are less informative than tokens that only appear
    rarely in the training corpus

    Returns a matrix that has had the frenquent tokens removed
    """

    text, sentiment = load_training_data()
    count_vectorizer = CountVectorizer(binary=True)
    text = count_vectorizer.fit_transform(text)
    tf_data = TfidfTransformer(use_idf=False).fit_transform(text)

    return tf_data, sentiment


def train_model(data, target):
    """
    Splits the data into a training set and test set

    Instatiating a Bernoulli Naive Bayes classifier, train on the training set,
    and then evaluate the model based upon the test set
    """

    #random_state generates a pseudo-random
    train_tweets, test_tweets, train_sentiment, test_sentiment = cross_validation.train_test_split(data, 
                                                                                                target,
                                                                                                test_size=0.4)
    classifier = BernoulliNB().fit(train_tweets, train_sentiment)
    predicted = classifier.predict(test_tweets)
    evaluate_model(test_sentiment, predicted)

def evaluate_model(true_sentiment, predicted_sentiment):
    print classification_report(true_sentiment, predicted_sentiment)
    print "The accuracy of the model is: {:.2%}".format(accuracy_score(true_sentiment,predicted_sentiment))




if __name__ == "__main__":
    tf_data, sentiment = preprocess_training()
    train_model(tf_data, sentiment)

