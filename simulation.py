# %% [markdown]
# Peas in a pod system simulation in REBOUND, testing the runtime of simulations

# %%
import rebound
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
def setup_system(Mstar):
    """
    Creates a peas in a pod system in REBOUND of stellar mass Mstar
    
    :param Mstar: Mass of the star in units of solar mass
    """
    sim = rebound.Simulation()
    sim.units = ('yr', 'AU', 'Msun')

    # The Star '*'
    # Mass: Mstar
    sim.add(m=Mstar, hash='*')

    # Create DataFrame to organize planets in system
    df=pd.DataFrame(columns=['mass', 'radius', 'semi-major_axis', 'eccentricity', 'inclination'])

