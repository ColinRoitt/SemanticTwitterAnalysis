import twitter
import time
import json


class Social:
    def __init__(self, para):
        self.dbObj = para[0]
        self.ml = para[1]
        self.api = twitter.Api(
            consumer_key='Mhza8IeYqeLY0ysePOy3gqG0R',
            consumer_secret='8XBsGVhkCgeOBEe9sRveHFPYZ0aU84aQokfJbFCLUV24SqAira',
            access_token_key='342769171-yWwNZ4Cdkfs5txJHjNVLJXNMB92N2Pt61ushltAP',
            access_token_secret='pmf7kHW2fmzA27cuHiWxBChgjei36P36MqPYwDfY0aBqn'
        )

    # GET
    def getTweets(self, PID):
        search = self.dbObj.getSearch(PID)[0][0].decode('utf-8')
        # count = 10
        data = self.api.GetSearch(
            raw_query='q=' + search + '&'
            'lang=en&'
            'tweet_mode=extended&'
            'result_type=recent'
        )
        # print(data)
        if len(data) > 0:
            tweet = data[0]
            returnData = []
            # print()
            if(not self.dbObj.tweetIsSaved(tweet.id_str)):
                full_text = ''
                if(tweet.retweeted_status == None):
                    full_text = tweet.full_text
                else:
                    full_text = tweet.retweeted_status.full_text
                tweetP = {
                    'text': full_text,
                    'hashtags': len(tweet.hashtags),
                    'mentions': len(tweet.user_mentions),
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count
                }
                # print(full_text)
                sentiment = self.ml.classify(tweetP)
                certainty = round(sentiment * 100, 0)
                date = time.strftime('%Y-%m-%d')
                self.dbObj.addTweet(
                    tweet.id_str, PID, full_text, str(sentiment), certainty, date)
                returnData = [str(tweet.id_str), str(PID), str(full_text),
                              str(sentiment), str(certainty), str(date)]
                return json.dumps(returnData)
            else:
                return 'No New Tweets Found'
        else:
            return 'No Tweets Found'
