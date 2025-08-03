from flask import Flask, jsonify, request, render_template
import sqlite3
from sqllite_connection.sql_operation import connect_to_database, drop_table, create_all_tables, insert_data
from api_helper.helper import get_patient_details, get_helper_details, get_patient_mapped_to_helper, get_patients_mapped_to_doctor, get_dashboard_game_details

app = Flask(__name__)

@app.route('/users')
def get_patient_detail():
    """Fetches data from the 'users' table and returns it as JSON."""
    conn = connect_to_database()
    if not conn:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({'users': data})

@app.route("/get_patient/<int:patient_id>")
def get_patient(patient_id):
    """API endpoint to retrieve patient details."""
    conn = connect_to_database()
    return get_patient_details(conn, patient_id)

@app.route("/get_helper_detail/<int:helper_id>")
def get_helper(helper_id):
    """API endpoint to retrieve helper details."""
    conn = connect_to_database()
    return get_helper_details(conn, helper_id)

@app.route("/get_helper_patient_detail/<int:helper_id>")
def get_patient_mapped_to_helper(helper_id):
    """API endpoint to retrieve patients mapped to a helper."""
    conn = connect_to_database()
    return get_patient_mapped_to_helper(conn, helper_id)

@app.route("/get_doctor_detail/<int:doctor_id>")
def get_doctor(doctor_id):
    """API endpoint to retrieve doctor details."""
    conn = connect_to_database()
    return get_helper_details(conn, doctor_id)

@app.route("/get_doctor_patient_detail/<int:doctor_id>")
def get_patients_mapped_to_doctor(doctor_id):
    """API endpoint to retrieve patients mapped to a doctor."""
    conn = connect_to_database()
    return get_patients_mapped_to_doctor(conn, doctor_id)

@app.route("/get_dashboard_detail/<int:patient_id>")
def get_dashboard_details_for_game(patient_id):
    """API endpoint to retrieve dashboard details for a patient."""
    conn = connect_to_database()
    return get_dashboard_game_details(conn, patient_id)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

# @app.route('/profile')
# def profile():
#     return render_template('profile.html')

# @app.route('/patienttests')
# def patienttests():
#     return render_template('patienttests.html')

# @app.route('/doctor')
# def doctor():
#     return render_template('doctor.html')

# @app.route('/caretaker')
# def caretaker():
#     return render_template('caretaker.html')

if __name__ == '__main__':
    with connect_to_database() as conn:
        drop_table(conn, "patient")
        drop_table(conn, "helper")
        drop_table(conn, "doctor")
        create_all_tables(conn)
        insert_data(conn)
    app.run(debug=True, port=8080)
