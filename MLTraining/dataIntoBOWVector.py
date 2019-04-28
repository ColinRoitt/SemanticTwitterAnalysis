import json
import os
import pickle
import re
import nltk
from nltk.stem import WordNetLemmatizer
from collections import Counter


def getDataSemEval(filePath):
    dl = []
    f = open(filePath).readlines()
    for line in f:
        entry = line.split('\t')
        sent = 0
        if(entry[1] == 'positive'):
            sent = 1
        if(entry[1] == 'negative'):
            sent = -1
        dl.append({'y': sent, 'x': entry[2]})
    return dl


def getData(filePath, sentiment):
    dl = []
    f = open(filePath).readlines()
    for line in f:
        dl.append({'y': sentiment, 'x': json.loads(line)['text']})
    return dl


def stripChars(data):
    removeUnicode = re.compile('u[0-9a-fA-F]{4}') #dont worry about slashes
    removeURLs = re.compile('http:.+')
    removeSymbols = re.compile('[^a-z A-Z 0-9]')
    # removeHandles = re.compile('@[a-zA-Z0-9]+ ?:?')
    for i in data:
        # i['x'] = removeHandles.sub('', i['x'])
        i['x'] = removeURLs.sub('', i['x'])
        i['x'] = removeUnicode.sub('', i['x'])
        i['x'] = removeSymbols.sub('', i['x'])


def buildLexicon(data):
    lex1 = []
    for i in data:
        lex1 += (i['x'].lower().split(' '))
    lex1 = [lem.lemmatize(i) for i in lex1]
    countOfWord = Counter(lex1)
    lex2 = []
    # print(countOfWord)
    for w in countOfWord:
        if(1000 > countOfWord[w] >= 13):
            lex2.append(w)
#    print(lex2)
    return lex1


def buildBigramLexicon(data):
    bigrams = []
    words = []
    for i in data:
        bigrams += getBigrams(i['x'])

    # print(b/igrams)
    countOfWord = Counter(bigrams)
    bigrams2 = []
    # print(countOfWord)
    for w in countOfWord:
        if(countOfWord[w] >= 2):
            bigrams2.append(w)
    # print(bigrams)
    return bigrams2


def getBigrams(text):
    bigrams = []
    words = text.lower().split(' ')
    words = [lem.lemmatize(i) for i in words]
    # print(words)
    for j in range(0, len(words)-2):
        bigrams.append(' '.join(words[j:j+2]))
    # print(bigrams)
    return bigrams


def parse(data, lex):
    result = []
    for tweet in data:
        parsedData = []
        grams = getBigrams(tweet['x'])
        for word in lex:
            if word in grams:
                parsedData.append(1)
            else:
                parsedData.append(0)
        result.append({'y': tweet['y'], 'x': parsedData})
    return result


lem = WordNetLemmatizer()
# nltk.download('wordnet')

dir_path = os.path.dirname(os.path.realpath(__file__))

data_folder = dir_path + "\\data\\"

posFile = data_folder + 'positive_tweets.json'
negFile = data_folder + 'negative_tweets.json'
unlabeledFile = data_folder + 'tweets.20150430-223406.json'
print('loading data...')
# posDataList = getDataSemEval(data_folder + 'twitter-2015train-A.tsv')
posDataList = getDataSemEval(data_folder + 'twitter-2013train-A.tsv')
# posDataList += getDataSemEval(data_folder + 'twitter-2014test-A.tsv')
# posDataList = getData(posFile, 1)
# negDataList = getData(negFile, 0)
# unlabeledDataList = getData(unlabeledFile, None)

print('pos count: ' + str(len(posDataList)))
# print('neg count: ' + str(len(negDataList)))
# print('unlabeled count: ' + str(len(unlabeledDataList)))

# strip @ symbols, strip emoticons, build a lexicon, write convertion algorithm
# allData = posDataList + negDataList
allData = posDataList
print('stripping chars...')
stripChars(allData)
print('total count: '+str(len(allData)))
print('building lexicon...')
lex = buildLexicon(allData)
# print(lex)
print('lexicon size: '+str(len(lex)))
#print('parsing data...')
# positiveParsed = parse(posDataList, lex)
#allData_p = parse(allData, lex)

#pickle.dump(allData_p, open(data_folder + "dataParsedLabled.p", "wb"))
# print(positiveParsed)
pickle.dump(lex, open(data_folder+'lexicon.p', 'wb'))
# print(lex)
