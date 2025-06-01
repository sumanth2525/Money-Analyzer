from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date
import os

app = Flask(__name__)
DATABASE = 'money.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Create the SQLite file and tables if they don't exist
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EnterAmount (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SplitExpense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            people TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DaySpend (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL
        );
    """)
    conn.commit()
    conn.close()


# Initialize the database before handling any requests
init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/enter', methods=('GET', 'POST'))
def enter():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name'].strip()
        amt = float(request.form['amount'])
        dt = request.form['date']
        cat = request.form['category']

        conn.execute(
            'INSERT INTO EnterAmount (name, amount, date, category) VALUES (?, ?, ?, ?)',
            (name, amt, dt, cat)
        )
        conn.commit()
        return redirect(url_for('enter'))

    rows = conn.execute(
        'SELECT id, name, amount, date, category FROM EnterAmount ORDER BY id DESC'
    ).fetchall()
    conn.close()
    return render_template('enter.html', rows=rows, today=date.today().isoformat())


@app.route('/split', methods=('GET', 'POST'))
def split():
    conn = get_db_connection()
    if request.method == 'POST':
        store = request.form['store'].strip()
        amt = float(request.form['amount'])
        dt = request.form['date']
        cat = request.form['category']

        people_list = request.form.getlist('split_with')
        people_str = ', '.join([p.strip() for p in people_list if p.strip()])

        conn.execute(
            'INSERT INTO SplitExpense (store, amount, date, category, people) VALUES (?, ?, ?, ?, ?)',
            (store, amt, dt, cat, people_str)
        )
        conn.commit()
        return redirect(url_for('split'))

    rows = conn.execute(
        'SELECT id, store, amount, date, category, people FROM SplitExpense ORDER BY id DESC'
    ).fetchall()
    conn.close()
    return render_template('split.html', rows=rows, today=date.today().isoformat())


@app.route('/day', methods=('GET', 'POST'))
def day():
    conn = get_db_connection()
    if request.method == 'POST':
        dt = request.form['date']
        amt = float(request.form['total_amount'])

        conn.execute(
            'INSERT INTO DaySpend (date, total_amount) VALUES (?, ?)',
            (dt, amt)
        )
        conn.commit()
        return redirect(url_for('day'))

    rows = conn.execute(
        'SELECT id, date, total_amount FROM DaySpend ORDER BY id DESC'
    ).fetchall()
    conn.close()
    return render_template('day.html', rows=rows, today=date.today().isoformat())


if __name__ == '__main__':
    # Listen on 0.0.0.0 so that other devices on the same network (e.g., your phone)
    # can reach it at http://<YOUR_PC_IP>:5000
    app.run(host='0.0.0.0', port=5000, debug=True)
