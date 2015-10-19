from psycopg2 import connect, extras
from config import *

#
# Setup for DB
#
def dict_cursor(conn, cursor_factory=extras.RealDictCursor):
    return conn.cursor(cursor_factory=cursor_factory)

#
# Adding a User
#
def add_user(user_entry):
  with connect(DATABASE_URL) as conn:
        with dict_cursor(conn) as db:

          q = ''' INSERT INTO users (name, cell_phone) 
          VALUES ( %(name)s, %(cell_phone)s) '''
          # Insert a row of data
          db.execute(q, {"name":user_entry['name'], "cell_phone":user_entry['cell_phone']})
#
# Getting all Current users from the Database
#
def get_all_users():
  with connect(DATABASE_URL) as conn:
        with dict_cursor(conn) as db:
          q = '''SELECT * FROM users'''
          db.execute(q)
          data = None
          data = db.fetchall()
  return data