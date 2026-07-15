import numpy as np
import matplotlib.pyplot as plt

def make_heat_to_rgb(heat_values):
    heat_max = np.max(heat_values)
    cmap = plt.get_cmap("magma")
    print(f"heat_max = {heat_max}")

    def heat_to_rgb(heat):
        t     = np.clip(heat / heat_max, 0.0, 1.0)  # linéaire [0, 1]
        t_inv = 1.0 - t                               # 0=clair, max=sombre
        r, g, b, _ = cmap(t_inv)
        return (int(r * 255), int(g * 255), int(b * 255))

    return heat_to_rgb