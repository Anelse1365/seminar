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
quiz_map_col = mydb["quiz_map"]

@app.route('/')
def get_random_name_data():
    try:
        # ดึงข้อมูลทั้งหมดที่มี field "name" จากทั้งสอง collection
        all_quiz_name_data_cursor = quiz_col.find({"name": {"$exists": True}}, {"name": 1, "_id": 0})
        all_quiz_map_name_data_cursor = quiz_map_col.find({"name": {"$exists": True}}, {"name": 1, "_id": 0})

        # แปลง Cursor เป็นลิสต์
        all_quiz_name_data = list(all_quiz_name_data_cursor)
        all_quiz_map_name_data = list(all_quiz_map_name_data_cursor)

        # สุ่มข้อมูลที่มี field "name"
        random_quiz_name_data = random.sample(all_quiz_name_data, min(3, len(all_quiz_name_data)))
        random_quiz_map_name_data = random.sample(all_quiz_map_name_data, min(3, len(all_quiz_map_name_data)))

        # รวมข้อมูล
        combined_name_data = random_quiz_name_data + random_quiz_map_name_data

        # ส่งข้อมูลไปยัง template
        return render_template('index.html', combined_name_data=combined_name_data)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
