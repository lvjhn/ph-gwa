""" 
    Averaged Gensim Model Vector
""" 
from sklearn.base import BaseEstimator, TransformerMixin
from gensim import downloader as api
from core.helpers.verbose_logging import VerboseLogging
import numpy as np
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, sent_tokenize, pos_tag
from collections import defaultdict
from core.helpers.contractions import decontracted
import re
import random
from functools import lru_cache
from gensim.utils import simple_preprocess
from core.helpers.split_sentences import split_sentences


# tag map (POS tags)
TAG_MAP = defaultdict(lambda : wn.NOUN)
TAG_MAP['J'] = wn.ADJ
TAG_MAP['V'] = wn.VERB
TAG_MAP['R'] = wn.ADV

# cached models 
MODEL_CACHE = {}

# stopwords 
# SOURCE: https://gist.github.com/sebleier/554280
STOPWORDS = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", 
    "you", "your", "yours", "yourself", "yourselves", "he", "him", 
    "his", "himself", "she", "her", "hers", "herself", "it", "its", 
    "itself", "they", "them", "their", "theirs", "themselves", "what", 
    "which", "who", "whom", "this", "that", "these", "those", "am", 
    "is", "are", "was", "were", "be", "been", "being", "have", "has", 
    "had", "having", "do", "does", "did", "doing", "a", "an", "the", 
    "and", "but", "if", "or", "because", "as", "until", "while", "of", 
    "at", "by", "for", "with", "about", "against", "between", "into", 
    "through", "during", "before", "after", "above", "below", "to", 
    "from", "up", "down", "in", "out", "on", "off", "over", "under", 
    "again", "further", "then", "once", "here", "there", "when", 
    "where", "why", "how", "all", "any", "both", "each", "few", "more", 
    "most", "other", "some", "such", "no", "nor", "not", "only", "own", 
    "same", "so", "than", "too", "very", "can", "will", "just", 
    
    # additional #
    "would", "could", "should", "must",
    ".", ",", ":", ";", ",", "-", "+", "/"

])

class AGMV(VerboseLogging):

    def __init__(
        self, 
        
        # model definition 
        model_name  = "glove-twitter-50",
        dims = 50,

        # averaging level (word or sentence)
        averaging = "word",

        # column to apply transformation to
        column = "text",

        # whether to remove stopwords or not
        no_stopwords = False,
        
        # caching
        use_cache   = False, 
        cache_file  = "./data/cache/dataset.cache",
        cache_dict  = {},

        # server offloading
        use_server  = False, 
        server_host = "127.0.0.1", 
        server_port = "8080",

        # use mock model 
        use_mock    = True,

        # verbose and indent (need to manually specify)
        verbose     = True,
        indent      = ""

    ): 
        # use verbose logging 
        VerboseLogging.__init__(self, verbose=verbose, indent=indent)

        # model definition 
        self.model_name = model_name 

        # dimensions 
        self.dims = dims

        # averaging level (word or sentence)
        self.averaging = averaging
        
        # caching 
        self.use_cache = use_cache 
        self.cache_file = cache_file 

        # server offloading 
        self.use_server = use_server 
        self.server_host = server_host 
        self.server_port = server_port 

        # use cache dict 
        self.cache_dict = cache_dict

        # remove stopwords 
        self.no_stopwords = no_stopwords

        # load model 
        if not use_mock:
            self.model = self.load_model() 
        else: 
            self.model = self.load_mock_model()
    
    def load_model(self): 
        if self.use_cache: 
            if self.verbose:
                print("--- AGMV : Using cached vectors -- ")
            return "CACHE"
        elif self.use_server:
            if self.verbose:
                print("--- AGMV : Using server hosted model. --")
            return "SERVER" 
        else: 
            if self.verbose:
                print(
                    f"--- AGMV : Loading model "
                    f"({self.model_name}) "
                    f"into memory. ---"
                )

            if self.model_name in MODEL_CACHE:
                return MODEL_CACHE[self.model_name]

            model = api.load(self.model_name)  
            MODEL_CACHE[self.model_name] = model
            
            return model
    
    def load_mock_model(self):
        if self.verbose: 
            print("--- Loading mock model ---")
        return MockModel(dims=self.dims)
         
    def fit(self):
        return self 
    
    def transform(self, X, y = None): 

        # transform to series if data frame 
        if type(X) is pd.DataFrame:
            X = pd.Series(X[self.column])
        
        # if using cache file
        if self.use_cache: 
            return self.transform_cache(X, y)
        
        # if using server
        elif self.use_server:
            return self.transform_server(X, y)
        
        # if using object directly
        else: 
            return self.transform_direct(X, y)

    def transform_cache(self, X, y = None):
        Xv = []

        for index, text in X.items():
            # use text 
            pass 

        return Xv 

    def transform_server(self, X, y = None):
        Xv = []

        for index, text in X.items():
            # use text 
            pass 

        return Xv 

    def transform_direct(self, X, y = None): 
        Xv = []

        for index, text in X.items():
            print(index, end="\r")
            text_vec = self.apply_on_text(index, text) 
            Xv.append(text_vec)

        Xv = np.array(Xv)
        return Xv

    def apply_on_text(self, index, text): 
        vector = None 

        if self.averaging == "word": 
            # tokens to work with 
            tokens = [] 

            # lowercase sentence 
            text = text.lower()

            # decontract words 
            words  = decontracted(text)

            # sentences
            words  = simple_preprocess(words)

            # if stopword removal is applied
            if self.no_stopwords: 
                words = self.remove_stopwords(words)

            # apply word level or sentence level averaging
            vector = self.averaged_words(words)

        elif self.averaging == "sentence": 
            # tokens to work with 
            tokens = [] 

            # lowercase sentence 
            text = text.lower()

            # decontract words 
            words  = decontracted(text)

            # dissect into sentences
            words  = split_sentences(text)

            # dissect into words
            words  = [simple_preprocess(s) for s in words]

            # if stopword removal is applied
            if self.no_stopwords: 
                words = self.remove_stopwords(words)

            # apply word level or sentence level averaging
            vector = self.averaged_sentences(words)

        return vector
      
    def lemmatize_sentence(self, sentence): 
        lemmatized = []

        for tagged_word in sentence: 
            token = tagged_word[0]
            pos   = TAG_MAP[tagged_word[1][0]]
            lemmatized.append(self.lemma(token, pos))

        return lemmatized

    def remove_stopwords(self, words): 
        words_ = []

        for sent in words:
            sent_ = [] 
            for word in sent:
                if word not in STOPWORDS:
                    sent_.append(word)
            words_.append(sent_)

        return words_


    def get_vector(self, word):
        if word not in self.model: 
            return None 
        else:
            return self.model[word]

    def averaged_words(self, words):
        words_  = [] 
        vectors = []
        
        # flatten array 
        for sent in words: 
            words_ += sent 

        # get vector for each words 
        vectors = []
        for word in words_:
            vector = self.get_vector(word)
            if vector is None:
                continue 
            vectors.append(vector)

        # get mean of vectors 
        vector = np.mean(vectors, axis=0)

        return vector
    
    def averaged_sentences(self, words): 
        words = [self.averaged_words(s) for s in words]
        vector = np.mean(words, axis=0) 
        return vector



class MockModel: 
    def __init__(self, dims = 50): 
        self.dims = dims

    def __getitem__(self, item): 
        return np.random.randn(self.dims)

    def __contains__(self, key):
        pick = random.choices(
            [True, False], 
            weights=[0.95, 0.05], 
            k=1
        )[0]
        return pick