# %% [markdown]
# Peas in a pod system simulation in REBOUND, testing the runtime of simulations

# %%
import math
import rebound
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
def inner_edge(gamma_0=0.1, gamma_1=0.54, m_star=1.0):
    '''
    Calculates the inner edge of peas in a pod system according to Sun et al. (2025)
    Returns the inner edge of system
    
    :param gamma_0: Average inner-edge of system with star of 1.0 solar mass
    :param gamma_1: Coefficient of power law to calculate inner edge
    :param m_star: Mass of star in system
    '''
    return gamma_0 * math.pow(m_star, gamma_1)

def next_orbit(r_h, a_j1, m_j1, m_j2, m_star):
    '''
    Returns semi-major axis of planet with mutual rill radii of r_h
    
    :param r_h: Desired mutual hill radii
    :param a_j1: Semi-major axis of preceding planet
    :param m_j1: Mass of preceding planet
    :param m_j2: Mass of planet
    :param m_star: Mass of star
    '''
    return ((2 * r_h) / math.pow((m_j1 + m_j2) / (3 * m_star), (1/3))) - a_j1

# %%
def setup_system(m_star):
    """
    Creates a peas in a pod system in REBOUND of stellar mass m_star
    
    :param m_star: Mass of the star in units of solar mass
    """
    sim = rebound.Simulation()
    sim.units = ('yr', 'AU', 'Msun')

    # The Star '*'
    # Mass: m_star
    sim.add(m=m_star, hash='*')

    # Create DataFrame to organize planets in system
    df=pd.DataFrame(columns=['mass', 'radius', 'semi-major_axis', 'eccentricity', 'inclination'])
