# %% [markdown]
# Peas in a pod system simulation in REBOUND, testing the runtime of simulations

# %%
import rebound
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
def inner_edge(gamma_0=0.1, gamma_1=0.54, m_star=1.0, n_planets=5):
    return

# %%
def setup_system(m_star):
    """
    Creates a peas in a pod system in REBOUND of stellar mass Mstar
    
    :param m_star: Mass of the star in units of solar mass
    """
    sim = rebound.Simulation()
    sim.units = ('yr', 'AU', 'Msun')

    # The Star '*'
    # Mass: m_star
    sim.add(m=m_star, hash='*')

    # Create DataFrame to organize planets in system
    df=pd.DataFrame(columns=['mass', 'radius', 'semi-major_axis', 'eccentricity', 'inclination'])

