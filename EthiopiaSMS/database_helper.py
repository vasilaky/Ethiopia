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

          q = ''' INSERT INTO users (name, cell_phone, region, village) 
          VALUES ( %(name)s, %(cell_phone)s, %(village)s, %(region)s) '''
          # Insert a row of data
          db.execute(q, {"name":user_entry['name'], "cell_phone":user_entry['cell_phone'], 
                          "region":user_entry['region'], "village":user_entry['village']})


#
# Deleting a user
#
def delete_user(user_entry):
  with connect(DATABASE_URL) as conn:
        with dict_cursor(conn) as db:

          q = ''' DELETE FROM users WHERE name = %(name)s '''
          # Insert a row of data
          db.execute(q, {"name":user_entry['name']})


#
# Getting all Current users from the Database
#
def get_all_users():
  with connect(DATABASE_URL) as conn:
        with dict_cursor(conn) as db:
          q = '''SELECT * FROM users'''
          db.execute(q)
          data = db.fetchall()
  return data

def get_user_info_from_id_list(id_list):
  user_info = []
  with connect(DATABASE_URL) as conn:
    with dict_cursor(conn) as db:
      for id_number in id_list:
        q = 'SELECT * FROM USERS WHERE id = {id_number}'.format(id_number=id_number)
        db.execute(q)
        result = db.fetchone()
        print "Fetched {user} from our database".format(user=result)
        user_info.append(result)

  return user_info

# Fetching Calls from the database
def add_call_to_db(user_id, call_info):
  with connect(DATABASE_URL) as conn:
    with dict_cursor(conn) as db:
      q_call_array = 'SELECT calls FROM USERS WHERE id = {id_number}'.format(id_number=user_id)
      db.execute(q_call_array)
      result = db.fetchone()
      if result['calls'] is None:
        q = 'UPDATE USERS SET CALLS = ARRAY[\'{call_info}\'] WHERE id={user_id}'.format(call_info=call_info, user_id=user_id)
      else:
        q = 'UPDATE USERS SET CALLS = array_append(ARRAY{}, \'{}\') WHERE id={}'.format(result['calls'], call_info, user_id)
      db.execute(q)

# Check for Region in database

