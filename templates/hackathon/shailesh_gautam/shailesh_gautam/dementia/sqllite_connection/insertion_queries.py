import random  # Import for generating random data

def insert_sample_patients(conn):
    """Inserts 6 sample patient records into the 'patient' table.

    Args:
        conn: The database connection object.
    """

    # Sample data (modify as needed)
    sample_data = [
        ("John Doe", 1234567890, "john.doe@example.com", 35, 1, 1),
        ("Jane Smith", 9876543210, "jane.smith@example.com", 28, 2, 1),
        ("Michael Brown", 1023456789, "michael.brown@example.com", 65, 3, 3),
        ("Alice White", 1122334455, "alice.white@example.com", 42, 4, 4),
        ("David Miller", 2233445566, "david.miller@example.com", 50, 5, 2),
        ("Emily Jones", 3344556677, "emily.jones@example.com", 72, 6, 1)]

    # Construct the INSERT query based on the schema
    column_names = ", ".join(["patient_name", "mobile_number", "email_id", "age", "helper_id", "doctor_id"])
    placeholders = ", ".join(["?"] * len(sample_data[0]))
    insert_query = f"INSERT INTO patient ({column_names}) VALUES ({placeholders})"

    cursor = conn.cursor()
    for data in sample_data:
        cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()

    print("6 Sample patient records inserted successfully!")

# def insert_patients_data(conn):
#   """Inserts sample patient records into the 'Patient' table.

#   Args:
#       conn: The database connection object.
#   """
#   # Sample data (modify as needed)
#   sample_data = [
#       ('John Doe', 65, 'M'),
#       ('Jane Smith', 72, 'F'),
#       ('Michael Lee', 58, 'M'),
#       ('Olivia Jones', 81, 'F'),
#       ('David Brown', 49, 'M'),
#       ('Emily Garcia', 37, 'F')
#   ]

#   cursor = conn.cursor()
#   for name, age, gender in sample_data:
#       cursor.execute("INSERT INTO Patient (patient_name, age, gender) VALUES (?, ?, ?)", (name, age, gender))
#   conn.commit()
#   cursor.close()

#   print("Sample patient records inserted successfully!")

def insert_sample_helpers(conn):
  """Inserts 10 sample helper records into the 'helper' table.

  Args:
      conn: The database connection object.
  """

  # Sample data (modify as needed)
  sample_data = [
      ("John Smith", 1234567890, "john.smith@helper.com", "Nurse", 30, 1),
      ("Jane Doe", 9876543210, "jane.doe@helper.com", "Caregiver", 25, 2),
      ("Michael Brown", 1123456789, "michael.brown@helper.com", "Therapist", 42, 3),
      ("Alice White", 1122334455, "alice.white@helper.com", "Nurse", 38, None),
      ("David Miller", 2233445566, "david.miller@helper.com", "Caregiver", 55, 1),
      ("Emily Jones", 3344556677, "emily.jones@helper.com", "Therapist", 60, None),
      ("Charles Johnson", 4455667788, "charles.johnson@helper.com", "Nurse", 28, 2),
      ("Sarah Williams", 5566778899, "sarah.williams@helper.com", "Caregiver", 48, 3),
      ("Matthew Davis", 6677889900, "matthew.davis@helper.com", "Therapist", 35, None),
      ("Jennifer Lopez", 7788990011, "jennifer.lopez@helper.com", "Nurse", 22, 1),
  ]

  # Construct the INSERT query based on the schema
  column_names = ", ".join(["helper_name", "mobile_number", "email_id", "helper_type", "age", "patient_mapped"])
  placeholders = ", ".join(["?"] * len(sample_data[0]))
  insert_query = f"INSERT INTO helper ({column_names}) VALUES ({placeholders})"

  cursor = conn.cursor()
  for data in sample_data:
      cursor.execute(insert_query, data)
  conn.commit()
  cursor.close()

  print("10 Sample helper records inserted successfully!")


def insert_sample_doctors(conn):
  """Inserts 10 sample doctor records into the 'doctor' table.

  Args:
      conn: The database connection object.
  """

  # Sample data (modify as needed)
  sample_data = [
      ("William Brown", 1234567890, "william.brown@doctor.com", "City Hospital", 50, None),
      ("Ashley Young", 9876543210, "ashley.young@doctor.com", "General Hospital", 38, 2),
      ("David Miller", 1223456789, "david.miller@doctor.com", "Central Clinic", 45, 1),
      ("Elizabeth Moore", 1122334455, "elizabeth.moore@doctor.com", "City Hospital", 62, 3),
      ("Christopher Clark", 2233445566, "christopher.clark@doctor.com", "General Hospital", 42, None),
      ("Sarah Jones", 3344556677, "sarah.jones@doctor.com", "Central Clinic", 58, 1),
      ("Daniel Garcia", 4455667788, "daniel.garcia@doctor.com", "City Hospital", 35, 2),
      ("Emily Hernandez", 5566778899, "emily.hernandez@doctor.com", "General Hospital", 40, None),
      ("Robert Lewis", 6677889900, "robert.lewis@doctor.com", "Central Clinic", 55, 3),
      ("Jennifer Walker", 7788990011, "jennifer.walker@doctor.com", "City Hospital", 32, 1),
  ]

  # Construct the INSERT query based on the schema
  column_names = ", ".join(["doctor_name", "mobile_number", "email_id", "hospital", "age", "patient_mapped"])
  placeholders = ", ".join(["?"] * len(sample_data[0]))
  insert_query = f"INSERT INTO doctor ({column_names}) VALUES ({placeholders})"

  cursor = conn.cursor()
  for data in sample_data:
      cursor.execute(insert_query, data)
  conn.commit()
  cursor.close()

  print("10 Sample doctor records inserted successfully!")


from datetime import datetime, timedelta  # For generating sample timestamps

def insert_sample_games(conn):
  """Inserts 10 sample game records into the 'game' table.

  Args:
      conn: The database connection object.
  """

  # Sample data (modify as needed)
  sample_data = [
      (1, 3, 70, 60, datetime.now() - timedelta(days=7), "July 2024"),
      (2, 1, 85, 35, datetime.now() - timedelta(days=5), "July 2024"),
      (2, 5, 60, 90, datetime.now() - timedelta(days=3), "July 2024"),
      (1, 2, 90, 50, datetime.now() - timedelta(days=1), "July 2024"),
      (2, 0, 100, 25, datetime.now(), "July 2024"),  # Today's game
      (3, 4, 75, 75, datetime.now() + timedelta(days=1), "August 2024"),  # Future game
      (1, 1, 80, 45, datetime.now() + timedelta(days=3), "August 2024"),
      (2, 3, 65, 80, datetime.now() + timedelta(days=5), "August 2024"),
      (1, 0, 100, 30, datetime.now() + timedelta(days=7), "August 2024"),
      (1, 2, 95, 60, datetime.now() + timedelta(days=9), "August 2024")
  ]

  # Construct the INSERT query based on the schema
  column_names = ", ".join(["patient_id", "wrong_attempts", "total_score", "time_in_sec", "execution_time", "execution_month"])
  placeholders = ", ".join(["?"] * len(sample_data[0]))
  insert_query = f"INSERT INTO game ({column_names}) VALUES ({placeholders})"

  cursor = conn.cursor()
  for data in sample_data:
      cursor.execute(insert_query, data)
  conn.commit()
  cursor.close()

  print("10 Sample game records inserted successfully!")


from datetime import datetime, timedelta  # For generating sample timestamps

def insert_sample_screening_tests(conn):
  """Inserts 10 sample screening test records into the 'screening_test' table.

  Args:
      conn: The database connection object.
  """

  # Sample data (modify as needed)
  sample_data = [
      (1, 80, 1, datetime.now() - timedelta(days=7), "July 2024"),
      (2, 90, 0, datetime.now() - timedelta(days=5), "July 2024"),
      (1, 75, 2, datetime.now() - timedelta(days=3), "July 2024"),
      (1, 95, 0, datetime.now() - timedelta(days=1), "July 2024"),
      (2, 100, 0, datetime.now(), "July 2024"),  # Today's test
      (1, 85, 1, datetime.now() + timedelta(days=1), "August 2024"),  # Future test
      (1, 90, 0, datetime.now() + timedelta(days=3), "August 2024"),
      (2, 70, 2, datetime.now() + timedelta(days=5), "August 2024"),
      (2, 95, 0, datetime.now() + timedelta(days=7), "August 2024"),
      (1, 80, 1, datetime.now() + timedelta(days=9), "August 2024")
  ]

  # Construct the INSERT query based on the schema
  column_names = ", ".join(["patient_id", "total_score", "dementia_level", "execution_time", "execution_month"])
  placeholders = ", ".join(["?"] * len(sample_data[0]))
  insert_query = f"INSERT INTO screening_test ({column_names}) VALUES ({placeholders})"

  cursor = conn.cursor()
  for data in sample_data:
      cursor.execute(insert_query, data)
  conn.commit()
  cursor.close()

  print("10 Sample screening test records inserted successfully!")

from datetime import datetime, timedelta  # For generating sample timestamps

def insert_sample_patient_questionnaires(conn):
  """Inserts 10 sample patient questionnaire records into the 'patient_questionnaire' table.

  Args:
      conn: The database connection object.
  """

  # Sample data (modify as needed)
  sample_data = [
      (1, 70, 2, datetime.now() - timedelta(days=7), "July 2024"),
      (2, 85, 1, datetime.now() - timedelta(days=5), "July 2024"),
      (1, 65, 3, datetime.now() - timedelta(days=3), "July 2024"),
      (1, 90, 0, datetime.now() - timedelta(days=1), "July 2024"),
      (2, 100, 0, datetime.now(), "July 2024"),  # Today's questionnaire
      (1, 80, 1, datetime.now() + timedelta(days=1), "August 2024"),  # Future questionnaire
      (1, 85, 0, datetime.now() + timedelta(days=3), "August 2024"),
      (2, 75, 2, datetime.now() + timedelta(days=5), "August 2024"),
      (2, 90, 0, datetime.now() + timedelta(days=7), "August 2024"),
      (1, 78, 1, datetime.now() + timedelta(days=9), "August 2024")
  ]

  # Construct the INSERT query based on the schema
  column_names = ", ".join(["patient_id", "total_score", "dementia_level", "execution_time", "execution_month"])
  placeholders = ", ".join(["?"] * len(sample_data[0]))
  insert_query = f"INSERT INTO patient_questionnaire ({column_names}) VALUES ({placeholders})"

  cursor = conn.cursor()
  for data in sample_data:
      cursor.execute(insert_query, data)
  conn.commit()
  cursor.close()

  print("10 Sample patient questionnaire records inserted successfully!")
