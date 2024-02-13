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
def get_combined_data():
    try:
        # ดึงข้อมูลจาก MongoDB
        all_quiz_data_cursor = quiz_col.find()
        all_quiz_map_data_cursor = quiz_map_col.find()

        # แปลง Cursor เป็นลิสต์
        all_quiz_data = list(all_quiz_data_cursor)
        all_quiz_map_data = list(all_quiz_map_data_cursor)

        # สุ่มข้อมูล x และ y
        random_quiz_data = random.sample(all_quiz_data, min(3, len(all_quiz_data)))
        random_quiz_map_data = random.sample(all_quiz_map_data, min(3, len(all_quiz_map_data)))

        # รวมข้อมูล
        combined_data = random_quiz_data + random_quiz_map_data

        # ส่งข้อมูลไปยัง template
        return render_template('index.html', combined_data=combined_data)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
