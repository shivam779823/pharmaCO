
#*****************************************
#  Maintainer : SHIVAM 
#*****************************************

#Imports
from flask import Flask, render_template, request, redirect, url_for , session ,send_file ,jsonify
import requests
import hashlib
from datetime import datetime
import os
from functools import wraps
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle , Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import mysql.connector
from mysql.connector import pooling
from collections import defaultdict
#prometheus imports
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client.exposition import make_wsgi_app
import time

# Define environment variables for MySQL connection
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "test")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "12345678")
MYSQL_DB = os.environ.get("MYSQL_DB", "pharmaco")
CHATBOT_URL = os.environ.get("CHATBOT_URL", "http://pharmaco-chatbot-service:81/api/get_response" )
# MySQL connection pooling
db_config = {
    "host": MYSQL_HOST,
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "database": MYSQL_DB,
    "pool_size": 5,
}

cnx_pool = pooling.MySQLConnectionPool(**db_config)


# Define Prometheus metrics
REQUEST_COUNTER = Counter(
    'http_request_total',
    'Total number of HTTP requests',
    ['path', 'status_code']  # Added label names for path and status_code
)
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP request latency')

ERROR_COUNTER = Counter(
    'http_request_error_total',
    'Total number of HTTP requests resulting in an error',
    ['path', 'status_code']
)
TRANSACTION_COUNTER = Counter(
    'app_transaction_total',
    'Total number of transactions',
    ['customer_name', 'quantity' , 'Medicine_name']
)
ROUTE_LATENCY = Histogram(
    'app_route_latency_seconds',
    'Response latency of specific routes',
    ['route']
)

app = Flask(__name__)
app.secret_key = os.urandom(24)
CHATBOT_API_URL = CHATBOT_URL



# Middleware to capture metrics for each request
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_LATENCY.observe(request_latency)
    REQUEST_COUNTER.labels(request.path, response.status_code).inc()
    if response.status_code >= 400:
        ERROR_COUNTER.labels(request.path, response.status_code).inc()
    return response



class Medicine:
    def __init__(self, name, price, mrp, quantity, expiry,date ):
        self.name = name
        self.price = price
        self.mrp = mrp
        self.quantity = quantity
        self.expiry = expiry.strftime('%Y-%m-%d')
        self.date = date.strftime('%Y-%m-%d %H:%M:%S')



class Transaction_details:
    def __init__(self,id, customer_name, phone_no, issued_by,name,quantity_sold,total_amount,datestamp):
        self.id = id
        self.customer_name = customer_name
        self.phone_no = phone_no
        self.issued_by = issued_by
        self.name = name
        self.quantity_sold = quantity_sold
        self.total_amount = total_amount
        self.datestamp = datestamp
class PharmacyManagementSystem:
    def __init__(self):
        self.initialize_database()

    def initialize_database(self):
        self.cnx_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            pool_reset_session=True,
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )

        # Create tables if they don't exist
        connection, cursor = self.get_connection_and_cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medicines (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    price FLOAT NOT NULL,
                    mrp FLOAT NOT NULL,
                    quantity INT NOT NULL,
                    expiry DATE NOT NULL,
                    date DATETIME NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transaction_info (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_name VARCHAR(255) NOT NULL,
                    phone_no VARCHAR(15) NOT NULL,
                    issued_by VARCHAR(255) NOT NULL,
                    medicine_name VARCHAR(255) NOT NULL,
                    quantity_sold INT NOT NULL,
                    total_amount FLOAT NOT NULL,
                    datestamp DATETIME NOT NULL
                )
            ''')

            # Commit changes to the database
            connection.commit()
        finally:
            # Close the cursor and connection in a finally block to ensure they are always closed
            cursor.close()
            connection.close()
    def get_connection_and_cursor(self):
        connection = self.cnx_pool.get_connection()
        cursor = connection.cursor()
        return connection, cursor

    def register_user(self, username, password):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return "Username already taken. Please choose a different username."

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        connection.commit()

        cursor.close()
        connection.close()

        return "Registration successful. You can now login."

    def get_users(self):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('SELECT * FROM users')
        user_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return user_data

    def remove_user(self, username):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('DELETE FROM users WHERE id = %s', (username,))
        connection.commit()

        cursor.close()
        connection.close()

        return "User removed successfully"

    def verify_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, hashed_password))
        user_data = cursor.fetchone()

        cursor.close()
        connection.close()

        if user_data:
            return True
        else:
            return False
    
    #datastructure  
    @staticmethod
    def combine_transactions(transactions):
        combined_transactions = defaultdict(list)
    
        for transaction in transactions:
            key = (transaction.customer_name, transaction.datestamp)
            combined_transactions[key].append(transaction)
    
        combined_data = []
        for key, transactions in combined_transactions.items():
            total_amount = sum(transaction.total_amount for transaction in transactions)
            # Convert datestamp to datetime object
            datestamp = datetime.strptime(key[1].strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            combined_transaction = {
                'customer_name': key[0],
                'datestamp': datestamp,
                'total_amount': total_amount,
                'transactions': transactions
            }
            combined_data.append(combined_transaction)
    
        return combined_data

    def add_medicine(self, name, price, mrp, quantity, expiry):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('INSERT INTO medicines (name, price, mrp, quantity, expiry, date) VALUES (%s, %s, %s, %s, %s, %s)',
                       (name, price, mrp, quantity, expiry, date))
        connection.commit()

        cursor.close()
        connection.close()

    def find_medicine(self, name):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('SELECT * FROM medicines WHERE name = %s', (name,))
        medicine_data = cursor.fetchone()

        cursor.close()
        connection.close()

        if medicine_data:
            return Medicine(*medicine_data[1:])
        else:
            return None

    def update_medicine_quantity(self, name, quantity):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('UPDATE medicines SET quantity = quantity + %s WHERE name = %s', (quantity, name))
        connection.commit()

        cursor.close()
        connection.close()

    def sell_medicine(self, name, quantity):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('SELECT quantity FROM medicines WHERE name = %s', (name,))
        current_quantity_row = cursor.fetchone()

        if current_quantity_row is None:
            print(f"Medicine '{name}' does not exist in the inventory.")
            cursor.close()
            connection.close()
            return f"Medicine '{name}' does not exist in the inventory."

        current_quantity = int(current_quantity_row[0])

        cursor.execute('SELECT * FROM medicines WHERE name = %s', (name,))
        medicine_data = cursor.fetchone()

        if medicine_data is None:
            print(f"Medicine '{name}' does not exist in the inventory.")
            cursor.close()
            connection.close()
            return f"Medicine '{name}' does not exist in the inventory."

        if current_quantity and current_quantity >= int(quantity):
            total_amount = medicine_data[3] * int(quantity)

            quantity_left = current_quantity - int(quantity)
            datestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute('UPDATE medicines SET quantity = %s WHERE name = %s', (quantity_left, name))

            connection.commit()
            print(f"Sold {quantity} units of '{name}' for ${total_amount:.2f}")
        else:
            print(f"Not enough stock for '{name}'. Available: {current_quantity if current_quantity else 0}")

        cursor.close()
        connection.close()

    def display_inventory(self):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('SELECT * FROM medicines')
        medicines_data = cursor.fetchall()

        cursor.close()
        connection.close()

        if not medicines_data:
            return []
        else:
            medicines = []
            for medicine_data in medicines_data:
                medicine = Medicine(*medicine_data[1:])
                medicines.append(medicine)
            return medicines

    def generate_pdf_report(self, start_date, end_date):
        connection, cursor = self.get_connection_and_cursor()

        filename = "inventory_report.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        # Add title, generated by, and date
        styles = getSampleStyleSheet()
        title = Paragraph("PharmaCO : Inventory Report", styles['Title'])
        generated_by = Paragraph(f"Generated by : {'Anonymous'}", styles['Normal'])
        current_date = Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        signed_by = Paragraph(f"Signed by : {'Anonymous'}", styles['Normal'])
        elements.extend([title, generated_by, current_date])

        # Generate the table data for the report
        data = [['Medicine Name', 'Price', 'Quantity', 'MRP', 'Expiry', 'Date']]

        # Fetch inventory data
        all_medicines = self.display_inventory()
        inventory_data = [(medicine.name, medicine.price, medicine.quantity, medicine.mrp, medicine.expiry, medicine.date) for medicine in all_medicines]

        # Filter medicines based on start_date and end_date
        filtered_medicines = [medicine for medicine in inventory_data if start_date <= datetime.strptime(medicine[-1], '%Y-%m-%d %H:%M:%S').date() <= end_date]

        data.extend(filtered_medicines)

        # Create the table and add it to the elements list
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        # Build the PDF document
        doc.build(elements)

        cursor.close()
        connection.close()

        print(f"Inventory report generated successfully. File saved as {filename}")

        return filename


    def remove_medicine(self, name):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('DELETE FROM medicines WHERE name = %s', (name,))
        connection.commit()

        cursor.close()
        connection.close()

        return f"Medicine '{name}' removed from the inventory."

    def recently_updated(self):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('SELECT * FROM medicines ORDER BY date DESC LIMIT 12')
        medicines_data = cursor.fetchall()

        cursor.close()
        connection.close()

        if not medicines_data:
            return []
        else:
            medicines = []
            for medicine_data in medicines_data:
                medicine = Medicine(*medicine_data[1:])
                medicines.append(medicine)
            return medicines

    def add_transaction_details(self, customer_name, phone_no, issued_by, medicine_name, quantity_sold, total_amount):
        datestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('INSERT INTO transaction_info (customer_name, phone_no, issued_by, medicine_name, quantity_sold, total_amount, datestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                       (customer_name, phone_no, issued_by, medicine_name, quantity_sold, total_amount, datestamp))
        connection.commit()

        cursor.close()
        connection.close()

    def get_transaction_details(self):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('SELECT id, customer_name, phone_no, issued_by, medicine_name, quantity_sold, total_amount, datestamp FROM transaction_info')
        transaction_data = cursor.fetchall()

        cursor.close()
        connection.close()

        if not transaction_data:
            return []

        transactions = []

        for row in transaction_data:
            id, customer_name, phone_no, issued_by, medicine_name, quantity_sold, total_amount, datestamp = row
            sale = Transaction_details(id, customer_name, phone_no, issued_by, medicine_name, quantity_sold, total_amount, datestamp)
            transactions.append(sale)

        return transactions

    def remove_transaction_details(self, id):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('DELETE FROM transaction_info WHERE id = %s', (id,))
        connection.commit()

        cursor.close()
        connection.close()

    def get_customer_recent(self):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute('SELECT * FROM transaction_info ORDER BY id DESC LIMIT 1')
        customer_data = cursor.fetchone()

        cursor.close()
        connection.close()

        if not customer_data:
            return None
        else:
            customer = Transaction_details(*customer_data)
            return customer
    def close_connection_pool(self):
        self.cnx_pool.closeall()
############################################################################################
   
pharmacy = PharmacyManagementSystem()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



##############################################################################################

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if pharmacy.verify_user(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message='Invalid!! username or password')

    return render_template('login.html')


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    message=None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        result = pharmacy.register_user(username, password)
        return render_template('register.html', result=result ,message=f'{username} User Register Sucessfully!!')

    return render_template('register.html')


# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



######################### METRICS ################################################


@app.route('/health')
def health():
    return jsonify(status="up"
    )

# Define /metrics route to expose metrics
@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY)


######################### METRICS ################################################


@app.route('/chat')  
@login_required
def chat():
    return render_template('chat.html')


@app.route("/ask_bot", methods=["POST"])
def ask_bot():
    user_message = request.form.get("message")
    if not user_message:
        return jsonify(response="Please provide a message.")

    try:
        # Send user message to the bot with correct content type
        headers = {'Content-Type': 'application/json'}
        response = requests.post(CHATBOT_API_URL, json={"message": user_message}, headers=headers, timeout=5)
        response.raise_for_status()
        bot_response = response.json().get("response")
        return jsonify(response=bot_response)  # Return JSON response
    except requests.exceptions.RequestException as e:
        return jsonify(response=f"Error communicating with chatbot: {str(e)}")

#HOME

@app.route('/')  
@login_required
def home():
    all_medicines = pharmacy.display_inventory()
    recently= pharmacy.recently_updated() 
    recently=recently[-10:]
    current_date = datetime.now().date()  # Convert current_date to datetime.date object
    users=pharmacy.get_users()
    expired_medicines = [medicine for medicine in all_medicines if datetime.strptime(medicine.expiry, '%Y-%m-%d').date() < current_date]

    out_of_stock_medicines = [medicine for medicine in all_medicines if medicine.quantity == 0]
    recently_sold=pharmacy.get_transaction_details()
    recently_sold = recently_sold[-10:]
    total_expired=len(expired_medicines)
    total_out_stocks=len(out_of_stock_medicines)
    total_sold=len(recently_sold)

    request_latency = time.time() - request.start_time
    ROUTE_LATENCY.labels(request.path).observe(request_latency)


    return render_template('index.html', medicines=all_medicines, expired_medicines=expired_medicines , recently=recently , outstocks=out_of_stock_medicines ,users=users,sell=recently_sold ,total_expired=total_expired ,OFS=total_out_stocks ,total_sold=total_sold)


@app.route('/remove_user', methods=['GET', 'POST'])  
@login_required
def remove_user():
    message = None
    if request.method == 'POST':
        user_ids = request.form.getlist('user_ids')  # Get list of selected user IDs
        for user_id in user_ids:
            pharmacy.remove_user(user_id)  # Assuming pharmacy.remove_user removes user based on user ID
        message = f"{len(user_ids)} users removed successfully!"
        request_latency = time.time() - request.start_time
        ROUTE_LATENCY.labels(request.path).observe(request_latency)
    users = pharmacy.get_users()  # Assuming pharmacy.get_users() returns updated user list
    return render_template('remove_user.html', message=message, users=users)


#add_medicine

@app.route('/add_medicine', methods=['GET', 'POST'])
@login_required
def add_medicine():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        mrp = float(request.form['mrp'])
        expiry = request.form['expiry']
        
        try:
            expiry = datetime.strptime(expiry, '%Y-%m-%d').date()

        except ValueError:
            return "Invalid Expiry Date Format. Please use yyyy-mm-dd."

        pharmacy.add_medicine(name, price, mrp, quantity, expiry)
        message = "Medicine added successfully!"

        request_latency = time.time() - request.start_time
        ROUTE_LATENCY.labels(request.path).observe(request_latency)
        
        # return redirect(url_for('add_medicine'))

    return render_template('add_medicine.html', message=message , medicines=pharmacy.recently_updated())


#find_medicine

@app.route('/find_medicine', methods=['GET', 'POST'])
@login_required
def find_medicine():
    if request.method == 'POST':
        name = request.form['name']
        medicine = pharmacy.find_medicine(name)
        return render_template('find_medicine.html', medicine=medicine)
    request_latency = time.time() - request.start_time
    ROUTE_LATENCY.labels(request.path).observe(request_latency)
    return render_template('find_medicine.html', medicine=None)

#update_medicine_quantity

@app.route('/update_medicine_quantity', methods=['GET', 'POST'])
@login_required
def update_medicine_quantity_route():
    recent_update=None
    message=None
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        pharmacy.update_medicine_quantity(name, quantity)
        recent_update=pharmacy.recently_updated()
        message="Updated Successfully!"
        # return redirect(url_for('display_inventory'))
        request_latency = time.time() - request.start_time
        ROUTE_LATENCY.labels(request.path).observe(request_latency)
     

    return render_template('update_medicine_quantity.html' ,recently=recent_update,message=message)


@app.route('/remove_medicine', methods=['GET', 'POST'])
@login_required
def remove_medicine():
    message = None
    all_medicines = pharmacy.display_inventory()
    
    if request.method == 'POST':
        selected_medicines = request.form.getlist('medicine_checkbox')

        for medicine_name in selected_medicines:
            pharmacy.remove_medicine(medicine_name)
        message="Medicine's Removed Successfully! "
        request_latency = time.time() - request.start_time
        ROUTE_LATENCY.labels(request.path).observe(request_latency)  
       
    return render_template('remove_medicine.html', medicines=all_medicines ,message=message)


@app.route('/remove_sales_history', methods=['GET', 'POST'])
@login_required
def remove_sales_history():
    message1 = None
    if request.method == 'POST':
        ids = request.form.getlist('ids')  # Get list of selected IDs
        for id in ids:
            pharmacy.remove_transaction_details(id)
        message1 = f"{len(ids)} history records removed successfully!"
        request_latency = time.time() - request.start_time
        ROUTE_LATENCY.labels(request.path).observe(request_latency)
    x = pharmacy.get_transaction_details()
    return render_template('remove_sales.html', message1=message1, medicines=x)


#SeLL medicine
@app.route('/sell_medicine', methods=['GET', 'POST'])
@login_required
def sell_medicine_route():
    message = None
    customer_name = None  # Initialize customer_name
    if request.method == 'POST':
        medicine_names = request.form.getlist('medicine_name')
        quantities = request.form.getlist('quantity')
        customer_name = request.form.get('customer_name') # Get customer name from the form
        phone_no = request.form['phone_no']  # Get phone number from the form
        issued_by = request.form['issued_by']
        message = "Medicine's sold Successfully! , Now Generate Invoice "
        invoice = []  # List to store invoice data
        # Process the data as needed
        for name, quantity in zip(medicine_names, quantities):
            if name and quantity:
                medicine = pharmacy.find_medicine(name)
                if medicine:
                    total_amount = medicine.mrp * int(quantity)
                    invoice.append({
                        'name': medicine.name,
                        'quantity_sold': int(quantity),
                        'price': medicine.mrp,
                        'total_amount': total_amount
                    })
                    # Perform the sell operation using pharmacy.sell_medicine()
                    pharmacy.sell_medicine(name, int(quantity))
                    pharmacy.add_transaction_details(customer_name, phone_no, issued_by, name, int(quantity), total_amount)
                    TRANSACTION_COUNTER.labels(customer_name, quantity , name ).inc()
                    request_latency = time.time() - request.start_time
                    ROUTE_LATENCY.labels(request.path).observe(request_latency)

        total_amount = sum(item['total_amount'] for item in invoice)

        # Store the invoice data in a session variable
        session['invoice'] = {
            'invoice_items': invoice,
            'total_amount': total_amount
        }
        return render_template('sell_medicine.html', medicines=pharmacy.display_inventory(), invoice=invoice, total_amount=total_amount, message=message)

    return render_template('sell_medicine.html', medicines=pharmacy.display_inventory())


#Invoice
@app.route('/invoice', methods=['GET', 'POST'])
@login_required
def invoice():
    customers = pharmacy.get_customer_recent()  # Get the list of customers
    customers = [customers] if customers else []

    invoice_data = session.get('invoice')  # Retrieve the invoice data from the session
    date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template('invoice.html', customers=customers, invoice_data=invoice_data , date=date)


#Display Inventory
@app.route('/display_inventory')
@login_required
def display_inventory():
    return render_template('display_inventory.html', medicines=pharmacy.display_inventory())


#Generate Report
@app.route('/generate_report', methods=['GET', 'POST'])
@login_required
def generate_report():
    if request.method == 'POST':
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        report_filename = pharmacy.generate_pdf_report(start_date, end_date)
        return send_file(report_filename, as_attachment=True)

    return render_template('generate_report.html')

@app.route('/transaction_history')
@login_required
def transaction_history():
    transactions = pharmacy.get_transaction_details()
    combined_transactions = pharmacy.combine_transactions(transactions)
    return render_template('transaction_history.html', combined_transactions=combined_transactions)

# Wrap the Flask app with the Prometheus WSGI middleware
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})


if __name__ == '__main__':
    pharmacy = PharmacyManagementSystem()
    app.run(debug=True , host='0.0.0.0')






