import sqlite3 as lite
import sys

con = lite.connect('app1.db')
cur = con.cursor()

sql = """
SELECT * FROM Cars
"""
with con:
  cur.execute(sql)
