from flask import Flask, request, jsonify, render_template, redirect
from pymongo import MongoClient
import os, json, redis
from pymongo.message import update

# App
application = Flask(__name__)

# connect to MongoDB
mongoClient = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_AUTHDB'])
db = mongoClient[os.environ['MONGODB_DATABASE']]

# connect to Redis
redisClient = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=os.environ.get("REDIS_PORT", 6379), db=os.environ.get("REDIS_DB", 0))

@application.route('/')
def game():
    # db.create_collection('guess')
    return render_template('home.html')
    
@application.route('/prepare', methods=['POST','GET'])
def prepare():
    check = db.guess.find_one({"_id": 666})
    if not check:
        db.guess.insert_one({
                "_id" : 666,
                "Question" : ['', '', '', ''],
                "Answer" : ['', '', '', ''],
                "Count" : 0,
                "Win" : False
        })
    return redirect('/Question')

@application.route('/Question',methods=['GET'])
def question():
    get_question = db.guess.find_one({"_id": 666})
    question = " ".join(get_question["Question"])
    return render_template('question.html',question=question)

@application.route('/add_question',methods=['POST'])
def add_question():
    save_question = request.form.get('add')
    db.guess.update_one({"_id":666, "Question":""}, {"$set": {"Question.$":save_question}})
    return redirect('/Question')

@application.route('/play',methods=['GET','POST'])
def play():
    check= db.guess.find_one({"_id": 666})
    if len(check["Question"]) > 0:
        answer = request.form.get('answer')
        if answer == check["Question"][0]:
            if len(check["Question"]) == 1:
                db.guess.update_one({"_id":666, "Win": False}, {"$set" : {"Win": True}})
            fun = {
                "$pop":{"Question":-1},
                "$set": {"Answer.$":answer}
                }
            db.guess.update_one({"_id": 666, "Answer":""}, fun)
        else:
            db.guess.update_one({"_id": 666}, {"$inc": {"Count": 1}})
    return redirect('/play2')

@application.route('/play2', methods=['GET'])
def show():
    check= db.guess.find_one({"_id": 666})
    answer = " ".join(check["Answer"])
    count = check["Count"]
    win = check["Win"]
    return render_template('play.html',answer=answer,count=count,win=win)
    
@application.route('/restart',methods=['DELETE','GET'])
def delete():
    check= db.guess.find_one({"_id": 666})
    db.guess.delete_one(check)
    return redirect('/prepare')

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("FLASK_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("FLASK_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)