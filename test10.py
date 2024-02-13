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
quiz_col2 = mydb["x"]

@app.route('/')
def get_combined_data():
    try:
        # ดึงข้อมูลจาก MongoDB และสร้างข้อมูล name + (สุ่มตัวเลข) + unit
        all_quiz_data_cursor = quiz_col.find({}, {"name": 1, "unit": 1, "_id": 0})

        # ดึงข้อมูลจาก collection "x"
        all_x_data_cursor = quiz_col2.find({}, {"x1": 1, "_id": 0})

        # แปลง Cursor เป็นลิสต์
        all_quiz_data = list(all_quiz_data_cursor)
        all_x_data = list(all_x_data_cursor)

        # สร้างข้อมูล name + (สุ่มตัวเลข) + unit ของตัวเอง
        combined_data = []
        total_random_numbers = 0

        for _ in range(2):
            quiz_item = random.choice(all_quiz_data)
            random_number = random.randint(1, 100)

            x_item = random.choice(all_x_data)
            combined_item = f"{x_item['x1']} {quiz_item['name']} {random_number} {quiz_item['unit']}"

            combined_data.append(combined_item)
            total_random_numbers += random_number

        # ส่งข้อมูลไปยัง template
        sampled_data = random.sample(combined_data, min(2, len(combined_data)))
        return render_template('index.html', sampled_data=sampled_data, total_random_numbers=total_random_numbers)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
