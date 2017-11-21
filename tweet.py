#!/usr/lib/python2.7

import re
from segmenter import Analyzer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from spellChecker import correct

class Tweet:

    def __init__(self, ftweet, label = None):
        """
        Initialize the tweet with it's complete text and class label if given.
        self.text - the original full text of the tweet
        self.label - class label of tweet
        self.processed - processed tweet text
        self.tokens - tokenized processed text
        self.hashtags - segmented hashtags present in the tweet
        self.fvec - [f1,f2,f3,f4,....] - feature vector for the tweet
        
        NOTE: Total number of features used are 11, i.e. f1 -> f11 where:
        f1: 
        f2:
        ...
        """
        self.text = ftweet
        self.label = label
        self.processed = ftweet
        self.tokens = []
        self.hashtags = []
        self.fvec = []

    def __tknize(self):
        """
        Tokenize the tweet text using TweetTokenizer.
        
        'strip_handles' removes Twitter username handles from text if set to True.
        'reduce_len' replaces repeated character sequences of length 3 or greater with sequences of length 3 if set to True.
        """
        ttkzr = TweetTokenizer(strip_handles=True, reduce_len=True)
        self.tokens = ttkzr.tokenize(self.processed)

    def __removeURL(self):
        newText = re.sub('http\\S+', '', self.processed, flags=re.MULTILINE)
        self.processed = newText

    def __removeNum(self):
        newText = re.sub('\\d+', '', self.processed)
        self.processed = newText

    def __removeSwords(self):
        stop_words = set(stopwords.words('english'))
        stop_words.update(['.',
         ',',
         '"',
         "'",
         '?',
         '!',
         ':',
         ';',
         '(',
         ')',
         '[',
         ']',
         '{',
         '}'])
        newtokens = [ word for word in self.tokens if word.lower() not in stop_words ]
        self.tokens = newtokens

    def __corrSpellings(self):
        for i, token in enumerate(self.tokens):
            self.tokens[i] = correct(token)

    def __findHashtags(self, segment = True):
        for i, token in enumerate(self.tokens):
            if token[0] == '#':
                self.hashtags.append(token)

        if segment == True:
            segTool = Analyzer('en')
            for i, tag in enumerate(self.hashtags):
                text = tag.lstrip('#')
                segmented = segTool.segment(text)
                self.hashtags[i] = segmented

    def processTweet(self, remove_nums = True, remove_swords = True, remove_url = True, seg_hashtags = True, corrections = True):
        if remove_url == True:
            self.__removeURL()
        if remove_nums == True:
            self.__removeNum()
        self.__tknize()
        self.__corrSpellings()
        self.__findHashtags(segment=seg_hashtags)
        if remove_swords == True:
            self.__removeSwords()

    def printer(self):
        print 'Full tweet:\n{!r} \n'.format(self.text)
        print "Tweet after removing URL's and numbers:\n{!r} \n".format(self.processed)
        print 'Final tokens obtained from tweet:\n{!r} \n'.format(self.tokens)
        print 'Segmented Hashtags:\n{!r} \n'.format(self.hashtags)
        print 'Feature vector for the tweet:\n{!r} \n'.format(self.fvec)
        print 'Class label of tweet:\n{} \n'.format(self.label)