def select_all_games(conn):
  """Selects all records from the 'game' table.

  Args:
      conn: The database connection object.

  Returns:
      A list of dictionaries representing the game records or None if no records found.
  """

  cursor = conn.cursor()
  cursor.execute("SELECT * FROM game")
  results = cursor.fetchall()
  cursor.close()

  if not results:
      return None

  return [dict(row) for row in results]  # Convert rows to dictionaries

# Example usage (assuming you have a way to establish a connection)
# conn = ... (your connection logic)
# games = select_all_games(conn)
# if games:
#     for game in games:
#         print(game)
# else:
#     print("No game records found")


def select_all_patient(conn):
  """Selects all records from the 'patient' table.

  Args:
      conn: The database connection object.

  Returns:
      A list of dictionaries representing the game records or None if no records found.
  """

  cursor = conn.cursor()
  cursor.execute("SELECT * FROM patient")
  results = cursor.fetchall()
  cursor.close()

  if not results:
      return None

  return [dict(row) for row in results]  # Convert rows to dictionaries

# Example usage (assuming you have a way to establish a connection)
# conn = ... (your connection logic)
# games = select_all_games(conn)
# if games:
#     for game in games:
#         print(game)
# else:
#     print("No game records found")
