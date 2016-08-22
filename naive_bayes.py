import numpy
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score
import re
import pickle



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

    #add bigrams Tfidf vs. Count, Bernoulli vs. Multinomial
    #precision vs. recall

    #tried implementing n-grams - didn't see improvement in precision or recall
    #ngram_range=(2,4)
    vectorizer = TfidfVectorizer()
    text_matrix = vectorizer.fit_transform(text)

    #pickling the vectorizer
    pickle_file = open('vectorizer.pickle', 'wb')
    pickle.dump(vectorizer, pickle_file)
    pickle_file.close()

    print text_matrix
    return text_matrix, sentiment


def train_model(data, target):
    """
    Splits the data into a training set and test set

    Instatiating a Bernoulli Naive Bayes classifier, train on the training set,
    and then evaluate the model based upon the test set
    """

    #stratification for dividing preclassified tweets into homogenous subgroups before
    #sampling in order to improve the representativeness of the sampling
    #
    train_tweets, validation_tweets, train_sentiment, validation_sentiment = cross_validation.train_test_split(data, 
                                                                                                target,
                                                                                                test_size=0.4)
    classifier = BernoulliNB().fit(train_tweets, train_sentiment)
    predicted = classifier.predict(validation_tweets)
    evaluate_model(validation_sentiment, predicted)

    #pickling the classifier
    pickle_file = open('nb_classifier.pickle', 'wb')
    pickle.dump(classifier, pickle_file)
    pickle_file.close()

    return classifier

    #cross-validation


def evaluate_model(true_sentiment, predicted_sentiment):
    """Prints out evaluation statistics from scikits library"""

    print classification_report(true_sentiment, predicted_sentiment)
    print "The accuracy of the model is: {:.2%}".format(accuracy_score(true_sentiment,predicted_sentiment))



def run_classifier(to_classify):
    """for importing into seed file to classify full database"""

    pickle_file = open('nb_classifier.pickle', 'rb')
    classifier = pickle.load(pickle_file)
    pickle_file.close()

    pickle_file = open('vectorizer.pickle', 'rb')
    vectorizer = pickle.load(pickle_file)
    pickle_file.close()


    feature_matrix = vectorizer.transform(to_classify)
    print "Count Vectorizer: {}".format(to_classify)

    sentiment_classification = classifier.predict(feature_matrix)

    print sentiment_classification
    return sentiment_classification





if __name__ == "__main__":

    sample_tweets = ["if you vote or support Hillary Clinton your unamerican and part of the problem", 
    "Happy Anniversary 19th Amendment! In your honor I'm going to go volunteer for the @HillaryClinton campaign tonight. #ImWithHer"]

    tf_data, sentiment = preprocess_training()
    classifier = train_model(tf_data, sentiment)

    run_classifier(sample_tweets)

