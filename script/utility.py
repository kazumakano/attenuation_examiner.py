from statistics import multimode
import numpy as np
import pandas as pd
from .log import Log


def get_rssi_info(log: Log) -> pd.DataFrame:
    rssi_info = np.empty((len(log.vis_mac_list), 3), dtype=np.float32)
    for i in range(len(log.vis_mac_list)):
        rssi_info[i][0] = np.mean(multimode(log.vis_rssi_list[i]))
        rssi_info[i][1] = np.median(log.vis_rssi_list[i])
        rssi_info[i][2] = np.mean(log.vis_rssi_list[i])

    rssi_info = pd.DataFrame({
        "mac address": log.vis_mac_list,
        "mode": rssi_info[:, 0],
        "median": rssi_info[:, 1],
        "mean": rssi_info[:, 2]
    })

    return rssi_info
