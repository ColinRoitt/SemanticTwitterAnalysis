from flask import Flask, jsonify, Response, request
# from ML import ML
from ML import ML
from DB import DB
from Social import Social
from SessionManager import SessionManager
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
ml = ML()
db = DB()
social = Social([db, ml])
sessMan = SessionManager(db, social)


@app.route('/sessMan/getTweets', methods=['get'])
def runGetTweets():
    PID = request.args.get('key')[1:]
    count = db.getCountPerDay(PID)[0][0]
    print(count)
    return sessMan.getTweets(PID, count), 200


@app.route('/sessMan/isRunning', methods=['get'])
def profileIsRunning():
    PID = request.args.get('key')[1:]
    return str(sessMan.isProfileRunning(PID))


@app.route('/sessMan/stopProfile', methods=['get'])
def stopProfile():
    PID = request.args.get('key')[1:]
    return str(sessMan.stopProfile(PID))


@app.route('/ml/classify/', methods=['GET'])
def getClassify():
    postId = request.args.get("key")[1:]
    if postId is None:
        return "Must provide post id to classify", 400
    return ml.classify(postId), 501  # not yet implemented


# use this path for knn addition
@app.route('/ml/train/', methods=['POST'])
def train():
    id = None
    label = None
    return ml.train(id, label), 501  # not yet implemented


@app.route('/social/getTweets/', methods=['GET'])
def getTweets():
    PID = request.args.get("key")[1:]
    return social.getTweets(PID), 200


@app.route('/db/empty/', methods=['POST'])
def emptyDb():
    profile = None
    return db.empty(profile), 501  # not yet implemented


@app.route('/db/getTweet/', methods=['GET'])
def getTweet():
    query = None
    return db.getTweets(query), 501  # not yet implemented


@app.route('/db/connect/', methods=['GET'])
def connect():
    return db.connect(), 200


@app.route('/db/addProfile/', methods=['GET'])
def addProfile():
    name = request.args.get("name")
    search = request.args.get("search")
    social = request.args.get("social")
    start = request.args.get("start")
    countPerDay = request.args.get("countPerDay")
    return db.addProfile(name, search, social, start, countPerDay), 200


@app.route('/db/getProfiles', methods=['GET'])
def getProfiles():
    return db.getProfiles(), 200


@app.route('/db/addTask/', methods=['GET'])
def addTask():
    PID = request.args.get("key")[1:]
    name = request.args.get("name")
    classO = request.args.get("class")
    comparator = request.args.get("comparator")
    bound = request.args.get("bound")
    return db.addTask(PID, name, classO, comparator, bound), 200


@app.route('/db/addTweet/', methods=['GET'])
def addTweet():
    TwID = request.args.get("TwID")
    PID = request.args.get("key")
    content = request.args.get("content")
    sentiment = request.args.get("sentiment")
    certainty = request.args.get("certainty")
    dateGot = request.args.get('dateGot')
    return db.addTweet(TwID, PID, content, sentiment, certainty, dateGot), 200


@app.route('/db/getProfileTweets', methods=['GET'])
def getProfileTweets():
    PID = request.args.get('key')[1:]
    return db.getProfileTweets(PID), 200


@app.route('/db/updateProfile', methods=['GET'])
def updateProfile():
    PID = request.args.get('key')[1:]
    name = request.args.get("name")
    search = request.args.get("search")
    social = request.args.get("social")
    start = request.args.get("start")
    countPerDay = request.args.get("countPerDay")
    return db.updateProfile(PID, name, search, social, start, countPerDay), 200


@app.route('/db/deleteProfile', methods=['GET'])
def deleteProfile():
    PID = request.args.get('key')[1:]
    return db.deleteProfile(PID), 200


@app.route('/db/getTasks', methods=['get'])
def getTasks():
    PID = request.args.get('key')[1:]
    return db.getTasks(PID), 200


@app.route('/db/deleteTask', methods=['get'])
def deleteTask():
    PID = request.args.get('key')[1:]
    TID = request.args.get('TID')
    return db.deleteTask(PID, TID), 200


@app.route('/social/saveTweet/', methods=['POST'])
def saveTweet():
    tweetID = None
    return db.saveTweet(tweetID), 501  # not yet implemented


if __name__ == '__main__':
    app.run(debug=True, threaded=True)


#

# CREATE TABLE `colinroi_fyp`.`Profiles` ( `PID` INT NOT NULL AUTO_INCREMENT , `name` VARCHAR(50) NOT NULL , `search` VARCHAR(250) NOT NULL , `social` VARCHAR(20) NOT NULL , `start` DATE NOT NULL , `countPerDay` INT(100) NOT NULL , PRIMARY KEY (`PID`)) ENGINE = InnoDB;

# CREATE TABLE `colinroi_fyp`.`Tasks` ( `TaID` INT NOT NULL AUTO_INCREMENT , `PID` INT NOT NULL , `name` VARCHAR(20) NOT NULL , `class` VARCHAR(1) NOT NULL , `compariator` VARCHAR(1) NOT NULL , `bound` INT NOT NULL , PRIMARY KEY (`TaID`, `PID`)) ENGINE = InnoDB;

# CREATE TABLE `colinroi_fyp`.`Tweets` ( `TwID` INT NOT NULL AUTO_INCREMENT , `PID` INT NOT NULL , `content` VARCHAR(300) NOT NULL , `sentiment` INT NOT NULL , `certainty` INT(100) NULL , PRIMARY KEY (`TwID`, `PID`)) ENGINE = InnoDB;
