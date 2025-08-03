from flask import jsonify

def get_patient_details(conn, patient_id):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM patient WHERE patient_id = ?", (patient_id,))
        results = cursor.fetchall()

        if results:
        # Convert results to dictionary (modify based on your table schema)
            data = dict(zip([col[0] for col in cursor.description], results))
            return jsonify(data), 200  # Success

        else:
            return jsonify({"message": "No results found for patient ID: {}".format(patient_id)}), 404  # Not Found

    except Exception as e:
        return jsonify({"message": "Error retrieving results: {}".format(str(e))}), 500  # Internal Server Error

def get_helper_details(conn, helper_id):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM helper WHERE helper_id = ?", (helper_id,))
        results = cursor.fetchall()

        if results:
        # Convert results to dictionary (modify based on your table schema)
            data = dict(zip([col[0] for col in cursor.description], results))
            return jsonify(data), 200  # Success

        else:
            return jsonify({"message": "No results found for patient ID: {}".format(helper_id)}), 404  # Not Found

    except Exception as e:
        return jsonify({"message": "Error retrieving results: {}".format(str(e))}), 500  # Internal Server Error

def get_patient_mapped_to_helper(conn, helper_id):
    try:
        cursor = conn.cursor()
        cursor.execute(f"select * from patient where patient_id in (SELECT patient_id FROM helper WHERE helper_id = ?)", (helper_id,))
        results = cursor.fetchall()

        if results:
        # Convert results to dictionary (modify based on your table schema)
            data = dict(zip([col[0] for col in cursor.description], results))
            return jsonify(data), 200  # Success

        else:
            return jsonify({"message": "No results found for patient ID: {}".format(helper_id)}), 404  # Not Found

    except Exception as e:
        return jsonify({"message": "Error retrieving results: {}".format(str(e))}), 500  # Internal Server Error


def get_doctor_details(conn, doctor_id):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM doctor WHERE doctor_id = ?", (doctor_id,))
        results = cursor.fetchall()

        if results:
        # Convert results to dictionary (modify based on your table schema)
            data = dict(zip([col[0] for col in cursor.description], results))
            return jsonify(data), 200  # Success

        else:
            return jsonify({"message": "No results found for patient ID: {}".format(doctor_id)}), 404  # Not Found

    except Exception as e:
        return jsonify({"message": "Error retrieving results: {}".format(str(e))}), 500  # Internal Server Error

def get_patients_mapped_to_doctor(conn, doctor_id):
    try:
        cursor = conn.cursor()
        cursor.execute(f"select * from patient where patient_id in (SELECT patient_id FROM doctor WHERE doctor_id = ?)", (doctor_id,))
        results = cursor.fetchall()

        if results:
        # Convert results to dictionary (modify based on your table schema)
            data = dict(zip([col[0] for col in cursor.description], results))
            return jsonify(data), 200  # Success

        else:
            return jsonify({"message": "No results found for patient ID: {}".format(doctor_id)}), 404  # Not Found

    except Exception as e:
        return jsonify({"message": "Error retrieving results: {}".format(str(e))}), 500  # Internal Server Error


def get_dashboard_game_details(conn, patient_id):
  """
  Calculates the average total score for each patient and execution month in the 'game' table.

  Args:
      conn: The SQLite database connection object.

  Returns:
      list: A list of dictionaries containing patient ID, execution month, and average score.
  """

  query = f"""
  SELECT patient_id, execution_month, AVG(total_score) AS average_score
  FROM game
  where patient_id = {patient_id}
  GROUP BY patient_id, execution_month
  """

  cursor = conn.cursor()
  cursor.execute(query)
  results = cursor.fetchall()

  # Convert results to a list of dictionaries
  data = []
  for row in results:
    patient_id, execution_month, asverage_score = row
    data.append({
      "patient_id": patient_id,
      "execution_month": execution_month,
      "average_score": asverage_score
    })

  return data


