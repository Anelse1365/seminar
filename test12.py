from flask import Flask, render_template, request
from pymongo import MongoClient
import random

app = Flask(__name__)

# สร้าง MongoClient
myclient = MongoClient('localhost', 27017)

# เลือกฐานข้อมูล
mydb = myclient["mydb"]

# เลือก collection
quiz_col = mydb["quiz"]
quiz_person = mydb["person"]

# กำหนดตัวแปร global และกำหนดค่าเริ่มต้น
question = ""
correct_answer = 0

# สร้างฟังก์ชันสำหรับสุ่มคำถาม
def generate_question():
    global question, correct_answer
    
    person_name_cursor =quiz_person.find({}, {"name": 1, "_id": 0})
    person_names = [person['name'] for person in person_name_cursor]
    # ดึงข้อมูลจาก MongoDB และสุ่มชื่อสัตว์
    animal_names_cursor = quiz_col.find({}, {"name": 1, "_id": 0})
    animal_names = [animal['name'] for animal in animal_names_cursor]

    # สุ่มข้อมูลสัตว์
    p1 = random.choice(person_names)
    x = random.choice(animal_names)
    n = random.randint(1, 10)
    y = random.choice(["ตัว", "ตัวละ", "ตัวนี้"])
    m = random.randint(5, 15)
    z = "บาท"

    # สร้างคำถามและคำตอบ
    question = f"{p1}มี {x} {n} {y} ถ้า {x} 1 {y} ราคา {m}{z} ดังนั้นราคา {x} {y}ทั้งหมดของมานีเป็นเท่าไร"
    correct_answer = n * m

# สร้างคำถามแรก
generate_question()

@app.route('/', methods=['GET', 'POST'])
def quiz():
    try:
        if request.method == 'POST':
            # รับคำตอบจากฟอร์ม
            user_answer = int(request.form['answer'])
            
            # ตรวจสอบคำตอบ
            if user_answer == correct_answer:
                result = "คำตอบถูกต้อง!"

                # สร้างคำถามใหม่เมื่อคำตอบถูกต้อง
                generate_question()
            else:
                result = f"คำตอบผิด! คำตอบที่ถูกต้องคือ {correct_answer}"

            return render_template('index.html', question=question, result=result)
        else:
            return render_template('index.html', question=question)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
