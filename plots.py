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
