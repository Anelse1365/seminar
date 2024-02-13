from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

myclient = MongoClient('localhost', 27017)
mydb = myclient["mydb"]
mycol = mydb["quiz"]
myquiz = { "name": "ห่าน" }
x = mycol.insert_one(myquiz)




@app.route('/')
def index():
    # mongo.db.quiz.insert_one({"name":"หมา"})
    return "<h1>Hello World</h1>"