import numpy as np
import particle_filter.script.parameter as pf_param
from matplotlib import get_backend
from matplotlib import pyplot as plt
from particle_filter.script.map import Map as PfMap


class Map(PfMap):
    def show_beacons_by_mac_list(self, mac_list: np.ndarray) -> None:
        beacon_idx_list = np.empty(len(mac_list), dtype=np.int16)
        beacon_mac_list: list[str] = self.beacon_mac_list.tolist()
        for i, m in enumerate(mac_list):
            beacon_idx_list[i] = beacon_mac_list.index(m)

        plt.figure(figsize=(12, 12))
        if pf_param.SHOW_RANGE is not None:
            plt.xlim(left=pf_param.SHOW_RANGE[0, 1], right=pf_param.SHOW_RANGE[0, 0])
            plt.ylim(bottom=pf_param.SHOW_RANGE[1, 0], top=pf_param.SHOW_RANGE[1, 1])
        plt.imshow(self.plain_gray_img, cmap="gray")
        annot = plt.annotate("", (1000, 1000), backgroundcolor="white")
        scatter = plt.scatter(self.beacon_pos_list[:, 0], self.beacon_pos_list[:, 1])
        plt.scatter(self.beacon_pos_list[beacon_idx_list, 0], self.beacon_pos_list[beacon_idx_list, 1])

        backend = get_backend()
        print(f"map.py: matplotlib GUI backend is {backend}")
        match backend:
            case "TkAgg":                            # tk
                print("map.py: press any button to stop")
                with plt.ion():
                    while True:
                        plt.connect("motion_notify_event", lambda event: self._on_hover(annot, event, scatter))
                        if plt.waitforbuttonpress(0.5):
                            break

                plt.close()

            case "module://ipympl.backend_nbagg":    # widget
                with plt.ion():
                    plt.connect("motion_notify_event", lambda event: self._on_hover(annot, event, scatter))

            case _:
                raise Exception("map.py: backend is expected to be tk or widget")
