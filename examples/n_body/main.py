#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from scinumtools.dip import DIP
from scinumtools.dip.docs import ExportDocsPDF

# =========================
# PARAMETERS (example tuning interface)
# =========================
with DIP() as dip:
    dip.add_file("defaults.dip")   # default settings
    dip.add_file("settings.dip")   # user modifications
    dip.add_file("derived.dip")    # derived settings
    params = dip.parse().data()

# =========================
# INITIALIZATION
# =========================
def initialize_system(p):
    np.random.seed(p["seed"])

    N = p["particles.number"]

    positions = np.random.randn(N, 2) * p["particles.scales.space"]
    velocities = np.random.randn(N, 2) * p["particles.scales.velocity"]
    masses = np.abs(np.random.randn(N)) * p["particles.scales.mass"]

    return positions, velocities, masses


# =========================
# FORCE COMPUTATION
# =========================
def compute_forces(positions, masses, G, softening):
    N = len(masses)
    forces = np.zeros_like(positions)

    for i in range(N):
        for j in range(i + 1, N):
            r = positions[j] - positions[i]
            dist_sq = np.dot(r, r) + softening**2
            dist = np.sqrt(dist_sq)

            # Newtonian gravity
            force_mag = G * masses[i] * masses[j] / dist_sq
            force_dir = r / dist

            force = force_mag * force_dir

            forces[i] += force
            forces[j] -= force  # Newton's 3rd law

    return forces


# =========================
# INTEGRATOR (Euler)
# =========================
def step(positions, velocities, masses, p):
    forces = compute_forces(
        positions,
        masses,
        p["system.gravitation"],
        p["softening"]
    )

    # Update velocities
    velocities += forces / masses[:, None] * p["system.time.step"]

    # Update positions
    positions += velocities * p["system.time.step"]

    return positions, velocities


# =========================
# SIMULATION LOOP
# =========================
def run_simulation(p):
    positions, velocities, masses = initialize_system(p)

    trajectory = []

    for _ in range(p["system.num_steps"]):
        positions, velocities = step(positions, velocities, masses, p)
        trajectory.append(positions.copy())

    return np.array(trajectory), masses


# =========================
# VISUALIZATION (optional)
# =========================
def plot_trajectory(trajectory, masses, params):
    plt.figure(figsize=(6, 6))

    for i in range(trajectory.shape[1]):
        path = trajectory[:, i, :]
        plt.plot(path[:, 0], path[:, 1], linewidth=1)
        plt.scatter(path[-1, 0], path[-1, 1], s=masses[i] * 5)

    plt.title(params['figure.title'])
    plt.xlabel(params['figure.xlabel'])
    plt.ylabel(params['figure.ylabel'])
    plt.axis("equal")
    plt.grid(True)
    plt.show()


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    trajectory, masses = run_simulation(params)
    if params['figure']:
        plot_trajectory(trajectory, masses, params)
