import sqlite3

def create_patient_table(conn):
  """Creates a 'Patient' table if it doesn't exist."""
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Patient (
      patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
      patient_name VARCHAR(255) NOT NULL,
      mobile_number BIGINT NOT NULL,
      email_id VARCHAR(255),
      age INTEGER NOT NULL,
      gender VARCHAR(255),
      helper_id INTEGER,
      doctor_id INTEGER
    )
  """)
  #FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id), 
  #FOREIGN KEY (helper_id) REFERENCES Helper(helper_id)
  conn.commit()
  cursor.close()

def create_helper_table(conn):
  """Creates a 'Helper' table if it doesn't exist."""
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Helper (
      helper_id INTEGER PRIMARY KEY AUTOINCREMENT,
      helper_name VARCHAR(255) NOT NULL,
      mobile_number BIGINT NOT NULL,
      email_id VARCHAR(255),
      helper_type VARCHAR(50) NOT NULL,
      age INTEGER NOT NULL,
      patient_mapped INTEGER
    )
  """)
  #FOREIGN KEY (patient_mapped) REFERENCES Patient(patient_id)
  conn.commit()
  cursor.close()
  
def create_doctor_table(conn):
  """Creates a 'Doctor' table if it doesn't exist."""
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Doctor (
      doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
      doctor_name VARCHAR(255) NOT NULL,
      mobile_number BIGINT NOT NULL,
      email_id VARCHAR(255),
      hospital VARCHAR(255),
      age INTEGER NOT NULL,
      patient_mapped INTEGER
    )
  """)
  #,FOREIGN KEY (patient_mapped) REFERENCES Patient(patient_id)
  conn.commit()
  cursor.close()


def create_game_table(conn):
  """Creates a 'Game' table if it doesn't exist."""
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Game (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      patient_id INTEGER NOT NULL,
      wrong_attempts INTEGER NOT NULL,
      total_score INTEGER NOT NULL,
      time_in_sec INTEGER NOT NULL,
      execution_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      execution_month VARCHAR(255) 
    )
  """)
  #FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
  conn.commit()
  cursor.close()

def create_screening_test_table(conn):
  """Creates a 'screening_test' table if it doesn't exist."""
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS screening_test (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      patient_id INTEGER NOT NULL,
      total_score INTEGER NOT NULL,
      dementia_level INTEGER,
      execution_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      execution_month VARCHAR(255)
    )
  """)
  #FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
  conn.commit()
  cursor.close()
  
def create_patient_questionnaire_table(conn):
  """Creates a 'patient_questionnaire' table if it doesn't exist."""
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS patient_questionnaire (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      patient_id INTEGER NOT NULL,
      total_score INTEGER NOT NULL,
      dementia_level INTEGER,
      execution_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      execution_month VARCHAR(255)
    )
  """)
  #FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
  conn.commit()
  cursor.close()
 
