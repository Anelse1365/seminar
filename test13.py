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

# กำหนดตัวแปร global
question1 = ""
question2 = ""
question3 = ""
correct_answer1 = 0
correct_answer2 = 0
correct_answer3 = 0
answered_question = None

# สร้างฟังก์ชันสำหรับสุ่มคำถาม
def generate_question1():
    global question1, correct_answer1
    person_name_cursor = quiz_person.find({}, {"name": 1, "_id": 0})
    person_names = [person['name'] for person in person_name_cursor]
    # ดึงข้อมูลจาก MongoDB และสุ่มชื่อสัตว์
    animal_names_cursor = quiz_col.find({}, {"name": 1, "_id": 0})
    animal_names = [animal['name'] for animal in animal_names_cursor]

    # สุ่มข้อมูลสัตว์
    p1 = random.choice(person_names)
    x = random.choice(animal_names)
    n = random.randint(1, 10)

    # Ensure that n2 is not greater than n
    y = random.choice(["ตัว", "ตัวละ", "ตัวนี้"])
    m = random.randint(5, 15)
    z = "บาท"

    # สร้างคำถามและคำตอบ
    question1 = f"{p1} มี {x} {n} {y} ถ้า {x} 1 {y} ราคา {m}{z} ดังนั้นราคา {x} {y}ทั้งหมดของ{p1}เป็นเท่าไร"
    correct_answer1 = n * m

def generate_question2():
    global question2, correct_answer2
    person_name_cursor = quiz_person.find({}, {"name": 1, "_id": 0})
    person_names = [person['name'] for person in person_name_cursor]

    # สุ่มข้อมูลสัตว์
    p2 = random.choice(person_names)
    n = random.randint(1, 10)
    n2 = random.randint(1, n)  # n2 should be between 1 and n

    # สร้างคำถามและคำตอบ
    question2 = f"{p2} มีแฟน {n} คน โดน {p2} แย่งแฟนไป {n2} คน {p2} จะเหลือแฟนกี่คน"
    correct_answer2 = n - n2

# สร้างฟังก์ชันสำหรับสุ่มคำถาม
def generate_question3():
    global question3, correct_answer3
    person_name_cursor = quiz_person.find({}, {"name": 1, "_id": 0})
    person_names = [person['name'] for person in person_name_cursor]

    # สุ่มข้อมูลสัตว์
    p3 = random.choice(person_names)
    n = random.randint(1, 10)
    n3 = random.randint(1, 10)
    # สร้างคำถามและคำตอบ
    question3 = f"{p3} มีเพื่อน {n} คน เพื่อนแต่ละคนของ {p3} ค่อยๆหายไปจนเหลือแค่ {n-n3} คน {p3} ต้องการเพื่อนคืนมาต้องหาเพิ่มกี่คน"
    correct_answer3 = n + n3

# สร้างคำถามแรก
generate_question1()

# สร้างคำถามเมื่อเริ่มรันแอปพลิเคชันครั้งแรก
@app.before_request
def before_request():
    global question1, question2, question3, correct_answer1, correct_answer2, correct_answer3, answered_question

    if not hasattr(app, 'questions_generated'):
        app.questions_generated = True
        generate_question1()
        generate_question2()
        generate_question3()

@app.route('/', methods=['GET', 'POST'])
def quiz():
    global question1, question2, question3, correct_answer1, correct_answer2, correct_answer3, answered_question

    try:
        if request.method == 'POST':
            # รับคำตอบจากฟอร์ม
            user_answer1 = int(request.form.get('answer1', -1))
            user_answer2 = int(request.form.get('answer2', -1))
            user_answer3 = int(request.form.get('answer3', -1))

            # ตรวจสอบคำตอบ
            result1 = ""
            result2 = ""
            result3 = ""

            
            

            # If a question has been answered correctly, generate a new question for that specific question
            if answered_question:
                if answered_question == "question1":
                    generate_question1()
                elif answered_question == "question2":
                    generate_question2()
                elif answered_question == "question3":
                    generate_question3()

            return render_template('index.html', question1=question1, question2=question2, question3=question3,
                                   result1=result1, result2=result2, result3=result3)
        else:
            return render_template('index.html', question1=question1, question2=question2, question3=question3)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
