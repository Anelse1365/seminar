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
correct_answer1 = 0
correct_answer2 = 0
answered_question = None

# สร้างฟังก์ชันสำหรับสุ่มคำถาม
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




