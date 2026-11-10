import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

## PROCESAMIENTO:
xs = pd.read_pickle("xs2.pkl").to_numpy()
ys = pd.read_pickle("ys2.pkl").to_numpy()
betas = np.arange(22.8,38, 0.005)
ts = np.linspace(1000, 1150, 60000)

peak_heights = {}


for n,b in enumerate(betas):
    peaks_vals = np.unique(find_peaks(xs[n,::], height=0)[1]['peak_heights'])
    peak_heights[b] = peaks_vals[peaks_vals>1]

## STYLING: 
plt.style.use("dark_background")

fig, ax = plt.subplots(2, 1, figsize=(10, 10))

ax[0].spines["right"].set_visible(False)
ax[0].spines["top"].set_visible(False)

ax[1].spines["right"].set_visible(False)
ax[1].spines["top"].set_visible(False)

## INITIAL_PLOTTING

for b, heights in peak_heights.items():
    ax[0].plot([b]*len(heights), heights, '.', color='white', markersize=.5,alpha=0.4)
ax[0].set_xlabel("L [mH]")
ax[0].set_ylabel("V Picos [V]")

ax[0].set_xlim(betas[-1],betas[0])
ax[0].set_ylim(np.min(xs[xs>1]), np.max(xs))

ax[1].set_xlabel("x(t) [V]")
ax[1].set_ylabel("y(t) [V]")

(dot_plot,) = ax[0].plot([], [], "x", alpha=1, markersize=10, c="red")
(rili_plot,) = ax[1].plot([], [], "o", alpha=1, markersize=1, c="white")
ax[1].set_xlim(np.min(xs), np.max(xs))
ax[1].set_ylim(np.min(ys), np.max(ys))

#ANIMACION: 

(dot_plot,) = ax[0].plot([], [], "x", alpha=1, markersize=15, c="red")

(rili_plot,) = ax[1].plot([], [], ".", alpha=1, markersize=1, c="white")

lines, = ax[0].plot([],[],lw=1.4,ls='--',c='orange',alpha=0.9)

invbetas = betas[::-1]
invxs = xs[::-1,::]
invys = ys[::-1,::]

def update(frame):
    
    counter = invbetas[frame]
    
    dot_plot.set_data([counter]*len(peak_heights[counter]), peak_heights[counter])

    rili_plot.set_data(invxs[frame, ::], invys[frame, ::])
        
    ax[1].set_xlim(np.min(invxs[frame,::]), np.max(invxs[frame,::]))
    ax[1].set_ylim(np.min(invys[frame,::]), np.max(invys[frame,::]))

        
    return dot_plot, rili_plot, lines

ani = FuncAnimation(fig, update, frames=len(betas), interval=1,blit=True)
ani.save("bifurcacion2.mp4", writer="ffmpeg", fps=60)
plt.show()