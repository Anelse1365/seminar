from flask import Flask, render_template
from pymongo import MongoClient
import random

app = Flask(__name__)

# สร้าง MongoClient
myclient = MongoClient('localhost', 27017)

# เลือกฐานข้อมูล
mydb = myclient["mydb"]

# เลือก collection
situ_col = mydb["situ"]

@app.route('/')
def get_random_situ_data():
    # ดึงข้อมูลทั้งหมดจาก MongoDB
    all_situ_data_cursor = situ_col.find()

    # แปลง Cursor เป็นลิสต์
    all_situ_data = list(all_situ_data_cursor)

    # ตรวจสอบว่ามีข้อมูลใน `situ` หรือไม่
    if not all_situ_data:
        return "No data in situ collection"

    # สุ่มข้อมูลบางตัวจาก situ
    random_situ_data = random.sample(all_situ_data, min(3, len(all_situ_data)))

    # ส่งข้อมูลไปยัง template
    return render_template('index.html', situ_data=random_situ_data)

if __name__ == '__main__':
    app.run(debug=True)
