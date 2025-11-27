import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

# Initialize Flask app
app = Flask(__name__)

# Database setup
DB_PATH = os.path.join('data', 'pizzas.db')

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

def get_db_connection():
    """Get a connection to the database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create database tables if they don't exist"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create Pizza table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pizza (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        
        # Create Order table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "Order" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pizza_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                promo_code_id INTEGER NULL,
                FOREIGN KEY (pizza_id) REFERENCES Pizza (id),
                FOREIGN KEY (promo_code_id) REFERENCES PromoCode (id)
            )
        ''')
        
        # Create PromoCode table
        cursor.execute('DROP TABLE IF EXISTS PromoCode')
        cursor.execute('''
            CREATE TABLE PromoCode (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                discount_percent REAL NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                usage_limit INTEGER NULL,
                times_used INTEGER NOT NULL DEFAULT 0
            )
        ''')
        
        # Add sample pizzas if table is empty
        cursor.execute('SELECT COUNT(*) FROM Pizza')
        if cursor.fetchone()[0] == 0:
            sample_pizzas = [
                ('Margherita', 14.99),
                ('Pepperoni', 13.99),
                ('Hawaiian', 13.49),
                ('Vegetarian', 12.99),
                ('Supreme', 15.49),
                ('BBQ Chicken', 13.99),
                ('Meat Lovers', 15.99),
                ('Buffalo', 16.99)
            ]
            cursor.executemany('INSERT INTO Pizza (name, price) VALUES (?, ?)', sample_pizzas)
            conn.commit()
        
        # Add sample promo codes if table is empty
        cursor.execute('SELECT COUNT(*) FROM PromoCode')
        if cursor.fetchone()[0] == 0:
            sample_promos = [
                ('WELCOME10', 0.10, '2024-01-01T00:00:00', '2025-12-31T23:59:59', None, 0),
                ('MIDWEEK15', 0.15, '2024-01-01T00:00:00', '2025-12-31T23:59:59', 200, 0),
                ('FAMILY20', 0.20, '2024-01-01T00:00:00', '2025-12-31T23:59:59', 150, 0)
            ]
            cursor.executemany('INSERT INTO PromoCode (code, discount_percent, start_date, end_date, usage_limit, times_used) VALUES (?, ?, ?, ?, ?, ?)', sample_promos)
            conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def get_all_pizzas():
    """Get all pizzas from the database"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, price FROM Pizza ORDER BY id')
        return cursor.fetchall()
    finally:
        conn.close()

def save_order(pizza_id, quantity, customer_name, promo_code_id=None):
    """Save order to database and return order ID"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Generate ISO 8601 timestamp
        current_time = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO "Order" (pizza_id, quantity, customer_name, timestamp, promo_code_id) VALUES (?, ?, ?, ?, ?)',
            (pizza_id, quantity, customer_name, current_time, promo_code_id)
        )
        order_id = cursor.lastrowid
        conn.commit()
        return order_id
    finally:
        conn.close()

def validate_promo_code(code):
    """Validate promo code and return promo code info or None"""
    if not code:
        return None
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, discount_percent, usage_limit, times_used, start_date, end_date
            FROM PromoCode 
            WHERE code = ?
        ''', (code.upper(),))
        promo = cursor.fetchone()
        
        if not promo:
            return None
            
        promo_id, discount_percent, usage_limit, times_used, start_date, end_date = promo
        
        # Check if promo is still valid
        from datetime import datetime
        now = datetime.now().isoformat()
        if now < start_date or now > end_date:
            return None
            
        # Check usage limit
        if usage_limit is not None and times_used >= usage_limit:
            return None
            
        return {
            'id': promo_id,
            'discount_percent': discount_percent,
            'code': code.upper()
        }
    finally:
        conn.close()

def increment_promo_usage(promo_id):
    """Increment the times_used counter for a promo code"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE PromoCode SET times_used = times_used + 1 WHERE id = ?', (promo_id,))
        conn.commit()
    finally:
        conn.close()

def get_order_details(order_id):
    """Get order details from database"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.id, p.name, p.price, o.quantity, o.customer_name, o.timestamp, pc.code, pc.discount_percent
            FROM "Order" o
            JOIN Pizza p ON o.pizza_id = p.id
            LEFT JOIN PromoCode pc ON o.promo_code_id = pc.id
            WHERE o.id = ?
        ''', (order_id,))
        return cursor.fetchone()
    finally:
        conn.close()

# Routes
def pizza_image_filename(pizza_name):
    """Get the correct image filename for a pizza name"""
    image_mapping = {
        'Margherita': 'margharita.avif',
        'Pepperoni': 'pepperoni.avif',
        'Hawaiian': 'hawaiian.avif',
        'Vegetarian': 'vegetarian.avif',
        'Supreme': 'Supreme.jpg',
        'BBQ Chicken': 'bbq_chicken.avif',
        'Meat Lovers': 'meat lovers.avif',
        'Buffalo': 'buffalo.avif'
    }
    return image_mapping.get(pizza_name, 'default.jpg')

@app.route('/')
def menu():
    """Show the pizza menu and order form"""
    pizzas = get_all_pizzas()
    return render_template('menu.html', pizzas=pizzas, pizza_image_filename=pizza_image_filename)

@app.route('/order', methods=['POST'])
def create_order():
    """Process the pizza order"""
    pizza_id = request.form.get('pizza_id')
    quantity = request.form.get('quantity')
    customer_name = request.form.get('customer_name')
    promo_code = request.form.get('promo_code', '').strip()
    
    if not pizza_id or not quantity or not customer_name:
        return redirect(url_for('menu'))
    
    # Validate promo code - must be empty or valid
    if promo_code:
        promo_info = validate_promo_code(promo_code)
        if not promo_info:
            # Invalid promo code - redirect back to menu with error
            return redirect(url_for('menu'))
        promo_code_id = promo_info['id']
    else:
        promo_info = None
        promo_code_id = None
    
    order_id = save_order(pizza_id, quantity, customer_name, promo_code_id)
    
    # Increment promo usage if valid
    if promo_info:
        increment_promo_usage(promo_info['id'])
        
    return redirect(url_for('confirmation', order_id=order_id))

@app.route('/confirmation')
def confirmation():
    """Show order confirmation"""
    order_id = request.args.get('order_id')
    if not order_id:
        return redirect(url_for('menu'))
        
    order = get_order_details(order_id)
    if not order:
        return redirect(url_for('menu'))
    
    # Extract order details
    order_id_val, pizza_name, price, quantity, customer_name, timestamp, promo_code, discount_percent = order
    
    # Calculate totals and discounts
    subtotal = price * quantity
    discount_amount = 0
    if promo_code and discount_percent:
        discount_amount = subtotal * discount_percent
    
    total = subtotal - discount_amount
    
    order_data = {
        'order_id': order_id_val,
        'pizza_name': pizza_name,
        'price': price,
        'quantity': quantity,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'total': total,
        'promo_code': promo_code,
        'discount_percent': discount_percent,
        'customer_name': customer_name
    }
    
    return render_template('confirmation.html', 
                         order=order_data, 
                         display_date=datetime.now().isoformat())

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
