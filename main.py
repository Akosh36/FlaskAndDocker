from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'todo.db'

# Function to initialize the database if it doesn't exist
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

# Home route - display all tasks
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, done FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    content = request.form['content']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (content, done) VALUES (?, ?)", (content, 0))
    conn.commit()
    conn.close()
    return redirect('/')

# Route to mark task as done
@app.route('/done/<int:task_id>')
def mark_done(task_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Entry point
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
