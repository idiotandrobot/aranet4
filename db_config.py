import os
import sqlite3

db_path = os.path.join(os.path.expanduser('~'), 'aranet4.db')

def getmeasurementsconnection():

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS measurements(
                device INTEGER,
                timestamp INTEGER,
                co2 INTEGER,
                temperature REAL,
                humidity INTEGER,
                pressure REAL,
                PRIMARY KEY(device, timestamp))''')
    con.commit()

    return con
