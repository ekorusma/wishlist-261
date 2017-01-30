import sqlite3 as lite
import sys

con = lite.connect('app1.db')
cur = con.cursor()

sql = """
DELETE FROM Cars
WHERE Id = 12
"""
with con:
  cur.execute(sql)
