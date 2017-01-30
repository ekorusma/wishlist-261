import sqlite3 as lite
import sys

cars = (
  (9, 'Suzuki', 52642),
  (10, 'Honda', 57127),
  (11, 'Nissan', 9000),
  (12, 'Hyundai', 29000),
  (13, 'Jialing', 350000)
)

con = lite.connect('app1.db')

with con: #Function like commit

  cur = con.cursor()

  #cur.execute("DROP TABLE IF EXISTS Cars")
  #cur.execute("CREATE TABLE Cars(Is INt, Name TEXT, Price INT)")
  cur.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)
