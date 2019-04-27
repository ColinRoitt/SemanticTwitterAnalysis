import random
from sklearn.neighbors import KNeighborsClassifier
import pickle
import os


class ML:
    def __init__(self, ):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file = open(dir_path + '\\models\\KNNClassierWithMetaVector.p', 'rb')
        self.model = pickle.load(file)
        self.words = pickle.load(
            open(dir_path + '\\models\\SentiWord.p', 'rb'))
        self.wordKeys = self.words.keys()

    # GET
    def classify(self, twt):
        vec = [self.getVector([twt])[0]['X']]
        result = self.model.predict(vec)
        print(result)
        return result[0]

    # POST
    def train(self, id, label):
        return 'not yet implemented'

    def buildALexicon(self, PID):
        return 'not yet implemented'

    def preprocess(self, TwId):
        return 'not yet implemented'

    def getWordSent(self, text):
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
            if w in self.wordKeys:
                sent = self.words[w]
                if sent == [1, 0]:
                    pos += 1
                elif sent == [0, 1]:
                    neg += 1
            # else:
            #     print('word not found')
        # total[0] += pos
        # total[1] += neg
        return {'pos': pos, 'neg': neg, 'pos_emote': posEm, 'neg_emote': negEm}

    def stripChars(self, data):
        # dont worry about slashes
        removeUnicode = re.compile('u[0-9a-fA-F]{4}')
        removeURLs = re.compile('http:.+')
        removeSymbols = re.compile('[^a-z A-Z 0-9]')
        # removeHandles = re.compile('@[a-zA-Z0-9]+ ?:?')
        for i in data:
            # i['x'] = removeHandles.sub('', i['x'])
            i = removeURLs.sub('', i)
            i = removeUnicode.sub('', i)
            i = removeSymbols.sub('', i)

    def getVector(self, data):
        parsed = []
        total = len(data)
        count = 0
        for t in data:
            # MetaAttributes
            wordSent = self.getWordSent(
                t['text'].replace('@', '').replace('#', ''))
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
            tweetObject = {'X': vector}
            parsed.append(tweetObject)
            count += 1
            # print(str(round((count / total) * 100))+'%')
        return parsed
