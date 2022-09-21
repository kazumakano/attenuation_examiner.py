import csv
import os.path as path
from datetime import datetime
from statistics import multimode
import numpy as np
import pandas as pd
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

    def print_rssi_info_list(self) -> None:
        if not hasattr(self, "vis_mac_list"):
            raise Exception("log.py: log visualizer hasn't been initialized yet")

        rssi_info_list = np.empty((len(self.vis_mac_list), 4), dtype=np.float32)
        for i in range(len(self.vis_mac_list)):
            rssi_info_list[i][0] = np.mean(multimode(self.vis_rssi_list[i]))
            rssi_info_list[i][1] = np.median(self.vis_rssi_list[i])
            rssi_info_list[i][2] = np.mean(self.vis_rssi_list[i])
            rssi_info_list[i][3] = self.vis_rssi_list[i].max()

        print(pd.DataFrame({
            "mac address": self.vis_mac_list,
            "mode": rssi_info_list[:, 0],
            "median": rssi_info_list[:, 1],
            "mean": rssi_info_list[:, 2],
            "max": rssi_info_list[:, 3]
        }))
