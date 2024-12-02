from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)

# Secret key for session management (required for flash messages)
app.secret_key = 'your_secret_key'

# MySQL connection setup
def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1', 
        user='root',  
        password='',  
        database='student_db' 
    )

# Home route to display all students
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Route to add a new student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Extract data from the form
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        department = request.form['department']
        
        # Insert the student into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, gender, email, department) VALUES (%s, %s, %s, %s, %s)", 
                       (name, age, gender, email, department))
        conn.commit()
        conn.close()
        
        flash("Student added successfully!", "success")
        return redirect(url_for('index'))
    
    return render_template('add.html')

# Route to edit student information
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", [id])
    student = cursor.fetchone()
    
    if request.method == 'POST':
        # Extract data from the form
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        department = request.form['department']
        
        # Update the student's details
        cursor.execute("""
            UPDATE students
            SET name = %s, age = %s, gender = %s, email = %s, department = %s
            WHERE id = %s
        """, (name, age, gender, email, department, id))
        conn.commit()
        conn.close()
        
        flash("Student updated successfully!", "success")
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', student=student)

# Route to delete student information
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully!", "danger")
    return redirect(url_for('index'))

# Route to search students by name
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE name LIKE %s", ('%' + query + '%',))
        students = cursor.fetchall()
        conn.close()
        return render_template('index.html', students=students)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
