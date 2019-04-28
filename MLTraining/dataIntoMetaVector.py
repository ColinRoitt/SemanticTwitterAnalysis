import os
import json
import pickle
import re


def getDataJson(filePath, sentiment):
    file = open(filePath, 'r')
    tweets = []
    for i in file:
        tweet = json.loads(i)
        # print(tweet)
        tweetP = {
            'y': sentiment,
            'text': tweet['text'],
            'hashtags': len(tweet['entities']['hashtags']),
            'mentions': len(tweet['entities']['user_mentions']),
            'likes': tweet['favorite_count'],
            'retweets': tweet['retweet_count']
        }
        # print(tweetP)
        tweets.append(tweetP)
    file.close()
    return tweets


total = [0, 0]


def getWordSent(text):
    pos = 0
    neg = 0
    posEm = 0
    negEm = 0
    positiveEmoticons = [':)', ':D', ':3', ';)', ';3', ':-)', ':-D']
    negativeEmoticons = [':\\', ':/', ':0', ':o', ':O', ':(', ':-(']
    textArr = text.split(' ')
    for w in textArr:
        if w in positiveEmoticons:
            posEm += 1
        if w in negativeEmoticons:
            negEm += 1
        if w in wordKeys:
            sent = words[w]
            if sent == [1, 0]:
                pos += 1
            elif sent == [0, 1]:
                neg += 1
        # else:
        #     print('word not found')
    total[0] += pos
    total[1] += neg
    return {'pos': pos, 'neg': neg, 'pos_emote': posEm, 'neg_emote': negEm}


def stripChars(data):
    removeUnicode = re.compile('u[0-9a-fA-F]{4}')  # dont worry about slashes
    removeURLs = re.compile('http:.+')
    removeSymbols = re.compile('[^a-z A-Z 0-9]')
    # removeHandles = re.compile('@[a-zA-Z0-9]+ ?:?')
    for i in data:
        # i['x'] = removeHandles.sub('', i['x'])
        i = removeURLs.sub('', i)
        i = removeUnicode.sub('', i)
        i = removeSymbols.sub('', i)


def getVector(data):
    parsed = []
    total = len(data)
    count = 0
    for t in data:
        # MetaAttributes
        wordSent = getWordSent(t['text'].replace('@', '').replace('#', ''))
        posWords = wordSent['pos']
        negWords = wordSent['neg']
        posEm = wordSent['pos_emote']
        negEm = wordSent['neg_emote']
        hashtags = t['hashtags']
        mentions = t['mentions']
        likes = t['likes']
        retweets = t['retweets']
        wordCount = len(t['text'])
        vector = [posWords, negWords, posEm, negEm, hashtags,
                  mentions, likes, retweets, wordCount]
        tweetObject = {'X': vector, 'y': t['y']}
        parsed.append(tweetObject)
        count += 1
        print(str(round((count / total) * 100))+'%')
    return parsed


data_folder = 'C:\\Users\\coolt\\OneDrive\\AAUni\\third_year\\fyp\\ML_Coding_Playground\\data\\'
# file = data_folder + 'twitter-2013train-A.tsv'
negFile = data_folder + 'negative_tweets.json'
posFile = data_folder + 'positive_tweets.json'
words = pickle.load(open('SentiWord.p', 'rb'))
wordKeys = words.keys()
data = getDataJson(posFile, 1)
data += getDataJson(negFile, -1)

parsed = getVector(data)
print(parsed)
print(total)
outputFile = open('MetaVector.p', 'wb')
pickle.dump(parsed, outputFile)
outputFile.close()
