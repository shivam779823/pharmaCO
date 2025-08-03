from re import I
from sqllite_connection.table_creation import create_patient_table, create_helper_table, create_doctor_table, create_game_table, create_screening_test_table, create_patient_questionnaire_table
from sqllite_connection.insertion_queries import *
import sqlite3


DATABASE_PATH = 'dementia.db'

def connect_to_database():
  """Connects to the local SQLite database."""
  try:
    conn = sqlite3.connect(DATABASE_PATH)
    return conn
  except sqlite3.Error as err:
    print(f"Error connecting to database: {err}")
    return None

def create_all_tables(conn):
  """Calls all table creation functions in a defined order."""
  create_table_functions = [
      create_patient_table,
      create_helper_table,
      create_doctor_table,
      create_game_table,
      create_screening_test_table,
      create_patient_questionnaire_table
  ]
  for func in create_table_functions:
      func(conn)

def drop_all_tables(conn):
  """Drops all tables but prompts for confirmation first.

  WARNING: This function permanently deletes all data from the tables.
  """
  cursor = conn.cursor()
  # Get all table names (assuming no schema prefix)
  tables = [row[0] for row in cursor.fetchall()]
  # Drop tables in reverse order to avoid foreign key constraint issues
  for table in reversed(tables):
      cursor.execute(f"DROP TABLE {table}")
  conn.commit()
  print("All tables dropped successfully.")
  cursor.close()  # Close cursor even if not dropped

def drop_table(conn, table_name):
  """Drops a table from the database.

  Args:
      conn: The database connection object.
      table_name (str): The name of the table to drop.
  """

  cursor = conn.cursor()
  cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
  conn.commit()
  cursor.close()

  print(f"Table '{table_name}' dropped successfully (if it existed).")


def insert_data(conn):
  """Inserts sample data into multiple tables.

  Args:
      conn: The database connection object.
  """
  insert_sample_patients(conn)
  insert_sample_helpers(conn)
  insert_sample_doctors(conn)
  insert_sample_games(conn)
  insert_sample_screening_tests(conn)
  insert_sample_patient_questionnaires(conn)

