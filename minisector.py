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
