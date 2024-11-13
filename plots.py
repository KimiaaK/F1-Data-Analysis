import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np
import pandas as pd


def speedDistance(telemetry):
    plt.figure(figsize=(15, 8))
    # Plot each minisector with a color corresponding to the fastest driver
    for minisector in telemetry["Minisector"].unique():
        sector_data = telemetry[telemetry["Minisector"] == minisector]
        color = "red" if sector_data["Fastest_Driver"].iloc[0] == "VER" else "blue"
        plt.plot(sector_data["Distance"], sector_data["Speed"], color=color)

    plt.title("Speed by Distance (Color-Coded by Fastest Driver per Minisector)")
    plt.xlabel("Distance (m)")
    plt.ylabel("Speed (km/h)")
    plt.legend(loc="best")
    plt.show()


def fast_segments(telemetry):
    x = np.array(telemetry["X"].values)

    y = np.array(telemetry["Y"].values)

    # Create points and segments for the LineCollection
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Fastest driver data as an array for color coding
    fastest_driver_array = telemetry["Fastest_Driver_Int"].to_numpy().astype(float)

    # Create the color map
    cmap = cm.get_cmap("winter", 2)
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N + 1), cmap=cmap)
    lc_comp.set_array(fastest_driver_array)
    lc_comp.set_linewidth(5)

    # Plot setup
    plt.rcParams["figure.figsize"] = [18, 10]
    fig, ax = plt.subplots()

    # Add the collection to the plot
    ax.add_collection(lc_comp)
    ax.axis("equal")
    ax.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    # Add color bar to indicate drivers
    cbar = plt.colorbar(mappable=lc_comp, boundaries=np.arange(1, 4))
    cbar.set_ticks([1.5, 2.5])
    cbar.set_ticklabels(["VER", "HAM"])

    # Save and display the plot
    plt.savefig("2023_ver_ham_q.png", dpi=300)
    plt.show()
