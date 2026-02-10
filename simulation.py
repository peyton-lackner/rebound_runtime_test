# %% [markdown]
# Peas in a pod system simulation in REBOUND, testing the runtime of simulations

# %%
import math
import time
import rebound
import numpy as np
import matplotlib.pyplot as plt

# %%
def inner_edge(gamma_0=0.1, gamma_1=0.54, m_star=1.0):
    '''
    Returns the inner edge of peas in a pod system according to Sun et al. (2025)
    
    :param gamma_0: Average inner-edge of system with star of 1.0 solar mass
    :param gamma_1: Coefficient of power law to calculate inner edge
    :param m_star: Mass of star in system
    '''
    return gamma_0 * math.pow(m_star, gamma_1)

# %%
def next_orbit(K, m_1, m_2, m_star, a_1):
    '''
    Returns semi-major axis of planet with mutual hill radii separation of K
    
    :param K: Mutual Hill Radii Separation Parameter
    :param m_1: Mass of inner planet
    :param m_2: Mass of outer planet
    :param m_star: Mass of star
    :param a_1: Semi-major axis of inner planet
    '''
    mu = math.pow((m_1 + m_2) / (3 * m_star), (1 / 3))
    a_2 = a_1 * ((2 + (K * mu)) / (2 - (K * mu)))

    return a_2

# %%
def setup_system(m_star, n_planets, planet_mass):
    """
    Creates a peas in a pod system in REBOUND of stellar mass m_star
    
    :param m_star: Mass of the star in units of solar mass
    """
    sim = rebound.Simulation()

    sim.integrator = 'mercurius'
    sim.ri_mercurius.r_crit_hill = 4.

    sim.units = ('yr', 'AU', 'Msun')

    # The Star '*'
    # Mass: m_star
    sim.add(m=m_star, hash='*')

    # Calculate semi-major axes
    curr_a = np.nan

    for i in range(n_planets):
        if i == 0:
            # First planet
            curr_a = inner_edge(m_star=m_star)
        else:
            curr_a = next_orbit(20, sim.particles[-1].m, planet_mass, m_star, sim.particles[-1].a)

        # Add planet to sim
        sim.add(m=planet_mass, a=curr_a, hash=chr(97+i))

    sim.move_to_com()
    return sim

# %%
def integration_time_test(masses, test_particles, integration_time):
    '''
    Run sims for all stellar masses and return array of all runtimes
    
    :param masses: Array of all stellar masses to be tested
    :param integration_time: Time to integrate sim for in units of yrs
    '''
    results = []

    print(f"Starting integration time test for {integration_time} years...")

    # Run sim for all mass values in masses
    for m_star in masses:
        print(f"Starting sim for {m_star} solar mass star...")

        # Create system with star mass m_star, 5 planets, and planets with 1.5 earth mass
        sim = setup_system(m_star, 5, 1.5*3e-6)

        # Add Test Particles
        sim.N_active = sim.N

        a_initial = np.linspace(0.5, 1, test_particles)
        for a in a_initial:
            sim.add(a=a,f=np.random.rand()*2.*np.pi)

        # Set timestep to 1/100 inner-most period
        sim.dt = sim.particles[1].P / 100

        # Run sim and measure time
        start_time = time.perf_counter()
        sim.integrate(integration_time)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        results.append(elapsed_time)
    
    return results

# %%
test_masses = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2] # Units of solar mass

results = integration_time_test(test_masses, 1000, 1000)

plt.figure(figsize=(10, 6))
plt.title("Simulation Time vs. Stellar Mass (1,000 yr integration)")
plt.xlabel("Stellar Mass (M_Sun)")
plt.ylabel("Simulation Time (s)")
plt.grid(True, alpha=0.3)

plt.plot(test_masses, results, marker='o', linestyle='-')

plt.show()
