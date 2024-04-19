from datetime import datetime
import argparse
import time
from db_config import getmeasurementsconnection
import mac_address
import aranet4

NUM_RETRIES = 10

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--devices", nargs="+", type=str)
args = parser.parse_args()

devices = args.devices

con = getmeasurementsconnection()
cur = con.cursor()

for mac in devices:
  device = mac_address.toint(mac)
  entry_filter = {}

  res = cur.execute('''SELECT timestamp FROM measurements WHERE device = ?
                       ORDER BY timestamp DESC LIMIT 1''', (device,))
  row = res.fetchone()
  if row is not None:
    entry_filter['start'] = datetime.fromtimestamp(row[0])

  for attempt in range(NUM_RETRIES):
    entry_filter['end'] = datetime.now()
    try:
      history = aranet4.client.get_all_records(mac, entry_filter)
      break
    except Exception as e:
      print('attempt', attempt, 'failed, retrying:', e)

  data = []
  for entry in history.value:
    if entry.co2 < 0:
      continue

    data.append((
      device,
      time.mktime(entry.date.utctimetuple()),
      entry.co2,
      entry.temperature,
      entry.humidity,
      entry.pressure      
    ))
  print('fetched', len(data), 'measurements', entry_filter)
  cur.executemany(
    'INSERT OR IGNORE INTO measurements VALUES(?, ?, ?, ?, ?, ?)', data)
  con.commit()

con.close()
