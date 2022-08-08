from statistics import multimode
import numpy as np
import pandas as pd
from .log import Log


def get_rssi_info_list(log: Log) -> pd.DataFrame:
    rssi_info_list = np.empty((len(log.vis_mac_list), 3), dtype=np.float32)
    for i in range(len(log.vis_mac_list)):
        rssi_info_list[i][0] = np.mean(multimode(log.vis_rssi_list[i]))
        rssi_info_list[i][1] = np.median(log.vis_rssi_list[i])
        rssi_info_list[i][2] = np.mean(log.vis_rssi_list[i])

    rssi_info_list = pd.DataFrame({
        "mac address": log.vis_mac_list,
        "mode": rssi_info_list[:, 0],
        "median": rssi_info_list[:, 1],
        "mean": rssi_info_list[:, 2]
    })

    return rssi_info_list
