import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np
import pandas as pd


# Enable the cache

ff1.Cache.enable_cache("./cache")


# Setup plotting

plotting.setup_mpl()


# Load the session data

session = ff1.get_session(2024, "Silverstone", "R")
print(session)
print(session.event["EventName"])


# Get the laps

load = session.load(telemetry=True)
print(f"session results:\n{session.results}")


print(f"session result columns:\n {session.results.columns }")
q3 = session.results.iloc[0:10].loc[:, ["Abbreviation", "Q3"]]
print(f"session result for Q3:\n{q3}")


# Get all the laps for a single driver.

laps_ver = session.laps.pick_driver("VER")
laps_ham = session.laps.pick_driver("HAM")


# Filter out slow laps as they distort the graph axis.

fastest_ver = (
    laps_ver.pick_fastest().get_telemetry().assign(Driver="VER").add_distance()
)
fastest_ham = (
    laps_ham.pick_fastest().get_telemetry().assign(Driver="HAM").add_distance()
)


# print(fastest_ver)


# Concatenate DataFrames

telemetry = pd.concat([fastest_ver, fastest_ham], ignore_index=True)
# print(telemetry)


num_minisectors = 25  # can be any number

track_length = telemetry["Distance"].max()
minisector_length = track_length / num_minisectors


# Create a list of distances where each minisector starts

minisector_start_distances = [i * minisector_length for i in range(num_minisectors)]
print(f"Minisector Start Distances:\n {minisector_start_distances}")

# Assign minisector to each telemetry point
telemetry["Minisector"] = (telemetry["Distance"] // minisector_length).astype(int)

# Calculate the average speed per driver per minisector
avg_speed_per_minisector = (
    telemetry.groupby(["Minisector", "Driver"])["Speed"].mean().unstack()
)


fastest_driver_per_minisector = avg_speed_per_minisector.idxmax(axis=1)
print("Fastest Driver per Minisector:", fastest_driver_per_minisector)

# Add the fastest driver per minisector to the telemetry data
telemetry = telemetry.merge(
    fastest_driver_per_minisector.rename("Fastest_Driver"), how="left", on="Minisector"
)

driver_mapping = {"VER": 1, "HAM": 2}
telemetry["Fastest_Driver_Int"] = telemetry["Fastest_Driver"].map(driver_mapping)

# Sort the telemetry data by Distance
telemetry = telemetry.sort_values(by="Distance")
