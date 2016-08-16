import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import TweetTokenizer
#figure out how to import custom corpus
 

def tokenize(text):
    """Tokenize text with NLTK TweetTokenizer"""

    tokenizer = TweetTokenizer()

    return TweetTokenizer(text)



def word_features(words):
    """Takes in file and returns dictionary of words"""

    return dict([(word, True) for word in words])
 


neg_ids = political_tweets.fileids('neg')
pos_ids = political_tweets.fileids('pos')
 
neg_features = [(word_feats(political_tweets.words(fileids=[f])), 'neg') for f in neg_ids]
pos_features = [(word_feats(political_tweets.words(fileids=[f])), 'pos') for f in pos_ids]
 
neg_cut_off = len(negfeats)*3/4
pos_cut_off = len(posfeats)*3/4
 
train_features = neg_features[:neg_cut_off] + pos_features[:pos_cut_off]
test_features = neg_features[neg_cut_off:] + pos_features[pos_cut+off:]

print 'train on %d instances, test on %d instances' % (len(train_features), len(test_features))
 
classifier = NaiveBayesClassifier.train(trainfeats)

print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
classifier.show_most_informative_features()