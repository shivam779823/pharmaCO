
#*****************************************
#  Maintainer : SHIVAM 
#*****************************************

#Imports
from flask import Flask, render_template, request, redirect, url_for , session ,send_file
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

# Define environment variables for MySQL connection
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "test")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "12345678")
MYSQL_DB = os.environ.get("MYSQL_DB", "test")

# MySQL connection pooling
db_config = {
    "host": MYSQL_HOST,
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "database": MYSQL_DB,
    "pool_size": 5,
}

cnx_pool = pooling.MySQLConnectionPool(**db_config)


app = Flask(__name__)
app.secret_key = os.urandom(24)


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
            return

        current_quantity = int(current_quantity_row[0])

        cursor.execute('SELECT * FROM medicines WHERE name = %s', (name,))
        medicine_data = cursor.fetchone()

        if medicine_data is None:
            print(f"Medicine '{name}' does not exist in the inventory.")
            cursor.close()
            connection.close()
            return

        if current_quantity and current_quantity >= int(quantity):
            total_amount = medicine_data[3] * int(quantity)

            quantity_left = current_quantity - int(quantity)
            datestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute('UPDATE medicines SET quantity = %s WHERE name = %s', (quantity_left, name))

            cursor.execute('INSERT INTO transaction_info (customer_name, phone_no, issued_by, medicine_name, quantity_sold, total_amount, datestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                            ("", "", "", name, int(quantity), total_amount, datestamp))

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
            customer = Transaction_details(*customer_data[1:])
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
        return render_template('register.html', result=result ,message='New User Register Sucessfully!!')

    return render_template('register.html')


# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



#########################################################################

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


    return render_template('index.html', medicines=all_medicines, expired_medicines=expired_medicines , recently=recently , outstocks=out_of_stock_medicines ,users=users,sell=recently_sold)


@app.route('/remove_user', methods=['GET', 'POST'])  
@login_required
def remove_user():
    message=None
    all_users = pharmacy.get_users()
    if request.method == 'POST':
        selected_user = request.form.getlist('user_checkbox')

        for username in selected_user:
            pharmacy.remove_user(username)
        message=f"{username} Removed Successfully! "
    return render_template('remove_user.html',users=all_users,message=message)


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
        
        
    return render_template('remove_medicine.html', medicines=all_medicines ,message=message)


@app.route('/remove_sales_history', methods=['GET', 'POST'])
@login_required
def remove_sales_history():
    message1 = None
    history = None  # Add this line to initialize the history variable
    if request.method == 'POST':
        id = request.form['id']
        # customer_name = request.form['customer_name']
        pharmacy.remove_transaction_details(id)
        # pharmacy.remove_customer_info(customer_name)
        message1 = f"History for ID '{id}' removed successfully!"
    
    # Fetch updated sales history after removal
    # sales_history = pharmacy.get_sales()
    x=pharmacy.get_transaction_details()
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



if __name__ == '__main__':
    pharmacy = PharmacyManagementSystem()
    app.run(debug=True , host='0.0.0.0')






