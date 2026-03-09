from flask import Flask, jsonify, request
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# --- MySQL connection configuration ---
db_config = {
    'host': os.getenv("DB_URL"),
    'user': 'admin',
    'password': os.getenv("PASSWORD"),
    'database': 'school',
    'port': 3306
}

def get_connection():
    return mysql.connector.connect(**db_config)

# Students CRUD
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students)

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, major, year) VALUES (%s, %s, %s)",
        (data['name'], data['major'], data['year'])
    )
    conn.commit()
    student_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"student_id": student_id}), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name=%s, major=%s, year=%s WHERE student_id=%s",
        (data['name'], data['major'], data['year'], student_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Student {student_id} updated."})

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Student {student_id} deleted."})

# Courses CRUD
@app.route('/courses', methods=['GET'])
def get_courses():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(courses)

@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO courses (title, credits) VALUES (%s, %s)",
        (data['title'], data['credits'])
    )
    conn.commit()
    course_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"course_id": course_id}), 201

@app.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE courses SET title=%s, credits=%s WHERE course_id=%s",
        (data['title'], data['credits'], course_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Course {course_id} updated."})

@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM courses WHERE course_id=%s",
        (course_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Course {course_id} deleted."})

if __name__ == '__main__':
    app.run(debug=True)
