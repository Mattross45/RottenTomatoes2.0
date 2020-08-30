#coding: utf-8
import re
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
tok = WordPunctTokenizer()

def tweet_cleaner(text):
    '''Permet de nettoyer les textes des tweets (enlève les sites web, les @, les rt)
    :input: le texte du tweet
    :output: le texte filtré'''
    pat1 = r'@[A-Za-z0-9_]+'        # remove @ mentions from tweets
    pat2 = r'https?://[^ ]+'        # remove URL's from tweets
    combined_pat = r'|'.join((pat1, pat2)) #addition of pat1 and pat2
    www_pat = r'www.[^ ]+'         # remove URL's from tweets
    contracted_words_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",   # converting words like isn't to is not
                    "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                    "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                    "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                    "mustn't":"must not", "it's":"it is", "i'm":"i am", "you're":"you are", "he's":"he is", "we're":"we are", "they're":"they are", "would've":"would have"}
    contrac_pattern = re.compile(r'\b(' + '|'.join(contracted_words_dic.keys()) + r')\b')

    stripped = re.sub(combined_pat, '', text) # calling combined_pat
    stripped = re.sub(www_pat, '', stripped) #remove URL's
    lower_case = stripped.lower()      # converting all into lower case
    neg_handled = contrac_pattern.sub(lambda x: contracted_words_dic[x.group()], lower_case) # converting word's like isn't to is not
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)       # will replace # by space
    words = [x for x in tok.tokenize(letters_only) if x not in ['s', 're']]
    return (" ".join(words)).strip() # join the words
