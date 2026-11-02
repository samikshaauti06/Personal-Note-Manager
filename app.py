from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="notes_db",
    user="postgres",
    password="root"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    content TEXT
)
""")
conn.commit()

@app.route('/')
def home():
    cur.execute("SELECT * FROM notes")
    data = cur.fetchall()
    return render_template("index.html", notes=data)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    content = request.form['content']

    cur.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s)",
        (title, content)
    )
    conn.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    cur.execute("DELETE FROM notes WHERE id=%s", (id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)