from flask import Flask, render_template
from pymongo import MongoClient
import random

app = Flask(__name__)

# สร้าง MongoClient
myclient = MongoClient('localhost', 27017)

# เลือกฐานข้อมูล
mydb = myclient["mydb"]

# เลือก collection
quiz_col = mydb["quiz"]
situ_col = mydb["situ"]

@app.route('/')
def get_random_combined_data():
    # ดึงข้อมูลทั้งหมดจาก MongoDB
    all_quiz_data_cursor = quiz_col.find()
    all_situ_data_cursor = situ_col.find()

    # แปลง Cursor เป็นลิสต์
    all_quiz_data = list(all_quiz_data_cursor)
    all_situ_data = list(all_situ_data_cursor)

    # สุ่มข้อมูลบางตัวจากทั้งสอง collection
    random_quiz_data = random.sample(all_quiz_data, min(3, len(all_quiz_data)))
    random_situ_data = random.sample(all_situ_data, min(3, len(all_situ_data)))

    # รวมข้อมูล
    combined_data = random_quiz_data + random_situ_data

    # ส่งข้อมูลไปยัง template
    return render_template('index.html', quiz_data=combined_data)

if __name__ == '__main__':
    app.run(debug=True)
