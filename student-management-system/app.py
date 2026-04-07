from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT,
            email TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()

    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        email = request.form['email']

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (name, age, course, email)
            VALUES (?, ?, ?, ?)
        ''', (name, age, course, email))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        email = request.form['email']

        cursor.execute('''
            UPDATE students
            SET name=?, age=?, course=?, email=?
            WHERE id=?
        ''', (name, age, course, email, id))

        conn.commit()
        conn.close()
        return redirect('/')

    cursor.execute('SELECT * FROM students WHERE id=?', (id,))
    student = cursor.fetchone()
    conn.close()

    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)