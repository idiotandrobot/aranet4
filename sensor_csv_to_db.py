from datetime import datetime
import argparse
import csv
import time
from db_config import getmeasurementsconnection

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--csv", type=str)
parser.add_argument("-m", "--mac", type=str)

args = parser.parse_args()

csvpath = args.csv
mac = args.mac
device = int(mac.replace(':',''), 16)

with open(csvpath,'r') as f:
    dr = csv.DictReader(f)
    data = [(device,
            time.mktime(datetime.strptime(i['Time(DD/MM/YYYY H:mm:ss)'], '%d/%m/%Y %H:%M:%S').replace(second=0).utctimetuple()), 
             i['Carbon dioxide(ppm)'], 
             i['Temperature(°C)'], 
             i['Relative humidity(%)'], 
             i['Atmospheric pressure(hPa)']
             ) for i in dr]

con = getmeasurementsconnection()
cur = con.cursor()
cur.executemany('INSERT OR IGNORE INTO measurements (device, timestamp, co2, temperature, humidity, pressure) VALUES(?, ?, ?, ?, ?, ?)', data)
con.commit()

con.close()