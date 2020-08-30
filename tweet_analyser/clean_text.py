#coding: utf-8
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob as tb
from textblob.blob import Word
import re
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
tok = WordPunctTokenizer()

def clean_tweets_stop_word_list_light(text, stop_words = ["ht", "amp", "dp", "toyota", "lexus", "inasoft", "d", "h", "t", "f", "xh", "m", "bd", "rt", "marvel", "endgame", "spiderman", "x-men", "mib", "aladdin", "jasmine", "jafar", "marvelcomics", "mibinternational", "meninblack", "teammibinternational"]):
    '''Permet de nettoyer les textes des tweets en enlevant les mots relatifs aux films
    :input: le texte du tweet, les stop_words à ajouter (les références aux films)
    :output: le texte filtré'''
    contracted_words_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",   # converting words like isn't to is not
                    "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                    "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                    "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                    "mustn't":"must not", "it's":"it is", "i'm":"i am", "you're":"you are", "he's":"he is", "we're":"we are", "they're":"they are", "would've":"would have"}
    contrac_pattern = re.compile(r'\b(' + '|'.join(contracted_words_dic.keys()) + r')\b')

    lower_case = text.lower()      # converting all into lower case
    neg_handled = contrac_pattern.sub(lambda x: contracted_words_dic[x.group()], lower_case) # converting word's like isn't to is not
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)       # will replace # by space
    stopwords_set = set(stop_words)
    words = [x for x in tok.tokenize(letters_only) if x not in stopwords_set]
    return (" ".join(words)).strip() # join the words

def clean_tweets_stop_word_list(text, new_stop_words = ["ht", "amp", "dp", "toyota", "lexus", "inasoft", "xh", "m", "bd", "rt", "marvel", "endgame", "spiderman", "x-men", "mib", "aladdin", "jasmine", "jafar", "marvelcomics", "mibinternational", "meninblack", "teammibinternational"]):
    '''Permet de nettoyer les textes des tweets en enlevant les mots fréquents et inutiles, ainsi que les références aux films
    :input: le texte du tweet, les stop_words à ajouter (les références aux films)
    :output: le texte filtré'''
    contracted_words_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",   # converting words like isn't to is not
                    "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                    "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                    "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                    "mustn't":"must not", "it's":"it is", "i'm":"i am", "you're":"you are", "he's":"he is", "we're":"we are", "they're":"they are", "would've":"would have"}
    contrac_pattern = re.compile(r'\b(' + '|'.join(contracted_words_dic.keys()) + r')\b')

    lower_case = text.lower()      # converting all into lower case
    neg_handled = contrac_pattern.sub(lambda x: contracted_words_dic[x.group()], lower_case) # converting word's like isn't to is not
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)       # will replace # by space
    stopwords_set = set(['about', 'your', 'are', 'they', 're', 'them', 'with', 'which', 'having', 'both', 'she', 'at', 'over', 'and', 'or', 'down', 'all', 'same', 'do', 'what', 'm', 'when', 'once', 'how', 'were', 'by', 'you', 'its', 'on', 'below', 'there', 'out', 'an', 'ma', 'these', 'from', 'up', 'that', 'above', 'have','me', 'before', 'we', 'again', 'has', 'why', 'am', 'him', 'the', 'for', 'll', 'been', 'any', 'being', 'in', 'y', 'whom', 'this', 'while', 'who', 'did', "it's", 'than', 'as', 'each',  'o', 'some',  't', 'd', 've', 'i', 'had', 'be', 'a', 'where', 'into', "she's", 'our', 'he', 'off', 'doing', 'does', 'it', 'only', 'ain', 'further', 'to', 'until', 'own', 'other', 'his', 'of', 's', 'just', 'then', 'no', 'those', 'is', 'was', 'between', 's'])
    stopwords_set.update(new_stop_words)
    words = [x for x in tok.tokenize(letters_only) if (x not in stopwords_set and len(x) > 1)]
    return (" ".join(words)).strip() # join the words

def clean_tweets_stop_word_list_heavy(text, new_stop_words = ["ht", "amp", "dp", "toyota", "lexus", "inasoft", "d", "h", "t", "f", "xh", "m", "bd", "rt", "marvel", "endgame", "spiderman", "x-men", "mib", "aladdin", "jasmine", "jafar", "marvelcomics", "mibinternational", "meninblack", "teammibinternational"]):
    '''Permet de nettoyer les textes des tweets en enlevant tous les mots fréquents, ainsi que les références aux films
    :input: le texte du tweet, les stop_words à ajouter (les références aux films)
    :output: le texte filtré'''
    contracted_words_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",   # converting words like isn't to is not
                    "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                    "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                    "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                    "mustn't":"must not", "it's":"it is", "i'm":"i am", "you're":"you are", "he's":"he is", "we're":"we are", "they're":"they are", "would've":"would have"}
    contrac_pattern = re.compile(r'\b(' + '|'.join(contracted_words_dic.keys()) + r')\b')

    lower_case = text.lower()      # converting all into lower case
    neg_handled = contrac_pattern.sub(lambda x: contracted_words_dic[x.group()], lower_case) # converting word's like isn't to is not
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)       # will replace # by space
    stopwords_set = set(stopwords.words("english"))
    stopwords_set.update(new_stop_words)
    words = [x for x in tok.tokenize(letters_only) if x not in stopwords_set]
    return (" ".join(words)).strip() # join the words

def clean_tweets_lemmatize(texte, new_stop_words = ["ht", "amp", "dp", "toyota", "lexus", "inasoft", "d", "h", "t", "f", "xh", "m", "bd", "rt", "marvel", "endgame", "spiderman", "x-men", "mib", "aladdin", "jasmine", "jafar", "marvelcomics", "mibinternational", "meninblack", "teammibinternational"]):
    '''Permet de nettoyer les textes des tweets en enlevant tous les mots fréquents, ainsi que les références aux films puis lemmatise
    :input: le texte du tweet, les stop_words à ajouter (les références aux films)
    :output: le texte filtré'''
    lemmatizer = WordNetLemmatizer()
    result=[]
    texte = clean_tweets_stop_word_list_heavy(texte, new_stop_words)
    words = texte.split(" ")
    for word in words:
        word = lemmatizer.lemmatize(word)
        result.append(word)
    return " ".join(result)

#print(clean_tweets_lemmatize("I love my parents. But not my cat:/ ?? woah"))

