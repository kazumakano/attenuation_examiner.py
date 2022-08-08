import csv
import os.path as path
from datetime import datetime
import numpy as np
from particle_filter.script.log import Log as PfLog


class Log(PfLog):
    def __init__(self, file: str) -> None:
        self.ts = np.empty(0, dtype=datetime)
        self.mac = np.empty(0, dtype="<U17")
        self.rssi = np.empty(0, dtype=np.int8)
        self.mac_list = np.empty(0, dtype="<U17")

        with open(file) as f:
            for row in csv.reader(f):
                self.ts = np.hstack((self.ts, datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")))
                self.mac = np.hstack((self.mac, row[1]))
                self.rssi = np.hstack((self.rssi, np.int8(row[2])))
                if row[1] not in self.mac_list:
                    self.mac_list = np.hstack((self.mac_list, row[1]))

        print(f"log.py: {path.basename(file)} has been loaded")
        print(f"log.py: log begins at {self.ts[0]} and ends at {self.ts[-1]}")
