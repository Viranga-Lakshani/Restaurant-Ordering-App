import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, g

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # In production, use a secure random key!

DATABASE = 'restaurant.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Helper functions for DB initialization and queries ---
def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
        db.commit()

# --- Authentication Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        if user:
            session['user'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Try again!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# --- Dashboard ---
@app.route('/')
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    menu_count = db.execute('SELECT COUNT(*) FROM menu').fetchone()[0]
    reservation_count = db.execute('SELECT COUNT(*) FROM reservations').fetchone()[0]
    order_count = db.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
    return render_template('dashboard.html', menu_count=menu_count, reservation_count=reservation_count, order_count=order_count)

# --- Menu Management ---
@app.route('/menu')
def menu():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    items = db.execute('SELECT * FROM menu').fetchall()
    return render_template('menu.html', items=items)

@app.route('/menu/add', methods=['POST'])
def add_menu_item():
    if 'user' not in session:
        return redirect(url_for('login'))
    name = request.form['name']
    price = request.form['price']
    db = get_db()
    db.execute('INSERT INTO menu (name, price) VALUES (?, ?)', (name, price))
    db.commit()
    return redirect(url_for('menu'))

@app.route('/menu/delete/<int:item_id>')
def delete_menu_item(item_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM menu WHERE id = ?', (item_id,))
    db.commit()
    return redirect(url_for('menu'))

# --- Reservations ---
@app.route('/reservations')
def reservations():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    reservations = db.execute('SELECT * FROM reservations').fetchall()
    return render_template('reservations.html', reservations=reservations)

@app.route('/reservations/add', methods=['POST'])
def add_reservation():
    if 'user' not in session:
        return redirect(url_for('login'))
    name = request.form['name']
    table_no = request.form['table_no']
    time = request.form['time']
    db = get_db()
    db.execute('INSERT INTO reservations (name, table_no, time) VALUES (?, ?, ?)', (name, table_no, time))
    db.commit()
    return redirect(url_for('reservations'))

@app.route('/reservations/delete/<int:res_id>')
def delete_reservation(res_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM reservations WHERE id = ?', (res_id,))
    db.commit()
    return redirect(url_for('reservations'))

# --- Orders ---
@app.route('/orders')
def orders():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    orders = db.execute('SELECT o.id, o.table_no, o.details, o.status FROM orders o').fetchall()
    return render_template('orders.html', orders=orders)

@app.route('/orders/add', methods=['POST'])
def add_order():
    if 'user' not in session:
        return redirect(url_for('login'))
    table_no = request.form['table_no']
    details = request.form['details']
    status = "Pending"
    db = get_db()
    db.execute('INSERT INTO orders (table_no, details, status) VALUES (?, ?, ?)', (table_no, details, status))
    db.commit()
    return redirect(url_for('orders'))

@app.route('/orders/update/<int:order_id>', methods=['POST'])
def update_order(order_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    status = request.form['status']
    db = get_db()
    db.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    db.commit()
    return redirect(url_for('orders'))

@app.route('/orders/delete/<int:order_id>')
def delete_order(order_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    db.commit()
    return redirect(url_for('orders'))

# --- Run the App ---
if __name__ == '__main__':
    import os
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
