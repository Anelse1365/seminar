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

@app.route('/')
def get_combined_data():
    try:
        # ดึงข้อมูลจาก MongoDB และสร้างข้อมูล name + (สุ่มตัวเลข) + unit
        all_quiz_data_cursor = quiz_col.find({}, {"name": 1, "unit": 1, "_id": 0})

        # แปลง Cursor เป็นลิสต์
        all_quiz_data = list(all_quiz_data_cursor)

        # สร้างข้อมูลและนับจำนวนสัตว์
        animal_count = {}
        for quiz_item in all_quiz_data:
            random_number = random.randint(1, 100)  # สุ่มตัวเลข
            combined_item = f"{quiz_item['name']}{random_number}{quiz_item['unit']}"

            # นับจำนวนสัตว์แต่ละชนิด
            animal_type = quiz_item['name']
            if animal_type not in animal_count:
                animal_count[animal_type] = 1
            else:
                animal_count[animal_type] += 1

        # ส่งข้อมูลไปยัง template
        return render_template('index.html', combined_data=animal_count)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
