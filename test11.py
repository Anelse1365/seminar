import random

def generate_question():
    animals = ["หมู", "วัว", "ไก่", "เป็ด", "กระต่าย"]  # รายชื่อสัตว์
    x = random.choice(animals)  # เลือกสัตว์สุ่ม
    n = random.randint(1, 10)  # สุ่มจำนวน
    y = random.choice(["ตัว", "ตัวละ", "ตัวนี้"])  # เลือกหน่วย
    m = random.randint(5, 15)  # สุ่มราคาต่อหน่วย
    z = "บาท"  # หน่วยเงิน

    question = f"มานีมี {x} {n} {y} ถ้า {x} 1 {y} ราคา {m}{z} ดังนั้นราคา {x} ดังนั้นราคา{y}ทั้งหมดของมานีเป็นเท่าไร"
    answer = n * m

    return question, answer

question, answer = generate_question()
print("คำถาม:", question)
print("คำตอบ:", answer)
