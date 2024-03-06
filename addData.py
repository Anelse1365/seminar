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

@app.route('/insert_documents')
def insert_documents():
    # เลือก collection
    x_collection = mydb['person']

    # ข้อมูลที่ต้องการเพิ่ม
    new_data = [
        {'p1': 'สมปอง'},
        {'p1': 'อดัม'}
    ]

    # เพิ่มข้อมูลใน collection "x"
    result = x_collection.insert_many(new_data)

    # ตรวจสอบว่ามีการเพิ่มข้อมูลหรือไม่
    if result.inserted_ids:
        return 'Documents added to collection "x".'
    else:
        return 'Failed to add documents to collection "x".'

if __name__ == '__main__':
    app.run(debug=True)
