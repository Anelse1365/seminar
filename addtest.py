#สร้าง collection ใหม่
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# สร้าง MongoClient
myclient = MongoClient('localhost', 27017)
# เลือกฐานข้อมูล
mydb = myclient["mydb"]

@app.route('/')
def home():
    return 'Hello, this is the home page.'

@app.route('/create_collection')
def create_collection():
    # เลือก collection หรือสร้างใหม่หากยังไม่มี
    x_collection = mydb['']

    # เพิ่ม document เข้า collection
    x_collection.insert_one({'x1': 'มานี'})

    return 'Collection "x" created and document added.'

if __name__ == '__main__':
    app.run(debug=True)
    #http://localhost:5000/create_collection
    
    
