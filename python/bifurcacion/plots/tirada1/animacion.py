import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use("dark_background")

xs = pd.read_pickle("xs2.pkl").to_numpy()
ys = pd.read_pickle("ys2.pkl").to_numpy()
# bs = np.linspace(-0.375, -0.5, 1000)
bs = np.arange(22.8, 50, 0.01)


peak_heights_dict = {}

peaks_dataframe = pd.DataFrame()

for n, b in enumerate(bs):
    peaks, vals = find_peaks(xs[n, ::], height=0)
    heights = np.array(vals["peak_heights"])
    peaks_df = np.array([np.full_like(heights, b), heights]).T
    peak_heights_dict[b] = heights
    peaks_dataframe = (
        pd.concat([peaks_dataframe, pd.DataFrame(peaks_df)])
        .drop_duplicates()
        .reset_index(drop=True)
    )

peaks, vals = peaks_dataframe.T.to_numpy()


fig, ax = plt.subplots(2, 1, figsize=(10, 10))

ax[0].plot(
    (-0.45),
    (-0.25),
    ls="",
    marker=">",
    ms=10,
    color="white",
    transform=ax[0].get_yaxis_transform(),
    clip_on=False,
)

ax[0].plot(
    (-0.375),
    (-0.18),
    ls="",
    marker="^",
    ms=10,
    color="white",
    transform=ax[0].get_xaxis_transform(),
    clip_on=False,
)

ax[1].plot(
    (1),
    (-0.2),
    ls="",
    marker=">",
    ms=10,
    color="white",
    transform=ax[1].get_yaxis_transform(),
    clip_on=False,
)
ax[1].plot(
    (0),
    (2),
    ls="",
    marker="^",
    ms=10,
    color="white",
    transform=ax[1].get_xaxis_transform(),
    clip_on=False,
)

ax[0].spines["right"].set_visible(False)
ax[0].spines["top"].set_visible(False)

ax[1].spines["right"].set_visible(False)
ax[1].spines["top"].set_visible(False)


ax[0].scatter(peaks, vals + 2.62349582070007 * peaks, s=0.4, alpha=1, c="white")
ax[0].set_xlim(-0.375, -0.45)
ax[0].set_ylim(-0.25, -0.18)

(dot_plot,) = ax[0].plot([], [], "x", alpha=1, markersize=10, c="red")
(rili_plot,) = ax[1].plot([], [], "o", alpha=1, markersize=1, c="white")
# (select_plot) = ax[0].fill_betweenx([], [], [], alpha=0.4, color="orange")
# p = ax[0].axvspan([], [], alpha=0.5, color="red")
ax[1].set_xlim(0, 1)
ax[1].set_ylim(-0.2, 0.2)


def update(frame):
    counter = bs[frame]

    # dot_plot.set_data([peaks[counter]], [(vals + 2.62349582070007 * peaks)[counter]])

    B = np.full_like(peak_heights_dict[counter], counter)
    point = B, peak_heights_dict[counter] + 2.62349582070007 * B
    dot_plot.set_data(point)

    rili_plot.set_data(xs[frame, ::], ys[frame, ::])
    ax[1].set_xlim(np.min(xs), np.max(xs))

    # p.set_xy([[counter - counter / 2, 0], [counter + counter / 2, 0], [counter + counter / 2, 10], [counter - counter / 2, 10]])
    # p = ax[0].axvspan(
    #     counter - counter / 2, counter + counter / 2, alpha=0.5, color="red"
    # )
    # p = ax[0].axvline(counter, color="r", linestyle="--")
    # b = ax[0].axvspan(
    #     counter - 6 * 0.00012513, counter + 6 * 0.00012513, alpha=0.2, color="orange"
    # )

    return dot_plot, rili_plot


# ani = FuncAnimation(fig, update, frames=len(bs), interval=100, repeat=True, blit=True)
# ani.save("bifurcacion2.mp4", writer="ffmpeg", fps=30)
plt.show()
