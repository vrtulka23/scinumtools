#!/usr/bin/python3
import subprocess
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(1, '../../src')   # run with local SNT version
from scinumtools.dip.config import ExportConfigCPP
from scinumtools.dip.docs import ExportDocsPDF
from scinumtools.dip import DIP

def initialise_header():
    # Parse DIP configuration
    with DIP() as dip:
        dip.add_file("config.dip")
        env = dip.parse()
    
    # Export configured parameters into a CPP configuration header
    with ExportConfigCPP(env) as exp:
        exp.parse(
            guard='CONFIG_H',
            const=['output.file']
        )
        exp.save("config.h")

def create_documentation():
    # Parse DIP configuration
    with DIP() as dip:
        dip.add_file("config.dip")
        docs = dip.parse_docs()
        
    # Create a PDF documentation
    with ExportDocsPDF(docs) as exp:
        exp.build(
            'documentation.pdf',
            "Electromagnetic force simulator",
            "Simple documentation of DIP parameters"
    )
        
def build_simulation():
    # Create build directory
    os.makedirs("build", exist_ok=True)
    
    # Run cmake configure and build
    subprocess.run(["cmake", ".."], cwd="build", check=True)
    subprocess.run(["cmake", "--build", "."], cwd="build", check=True)

def run_simulation():
    subprocess.run(["./sim"], cwd="build", check=True)
    
def plot_data():
    # Parse DIP configuration
    with DIP() as dip:
        dip.add_file("config.dip")
        env = dip.parse()
    params = env.data()

    # Load data
    data = pd.read_csv(params['output.file'])
    
    # Extract columns
    x = data["x"]
    y = data["y"]
    z = data["z"]
    t = data["t"]

    if params['plots.traj2d']:
        # --- 2D trajectory (x-y plane) ---
        plt.figure()
        plt.plot(x, y)
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.title("Particle Trajectory (x-y plane)")
        plt.axis("equal")  # important for correct geometry
        plt.grid()

    if params['plots.velocity']:
        # --- Velocity magnitude vs time ---
        vx = data["vx"]
        vy = data["vy"]
        vz = data["vz"]
        
        v_mag = (vx**2 + vy**2 + vz**2)**0.5
        
        plt.figure()
        plt.plot(t, v_mag)
        plt.xlabel("Time (s)")
        plt.ylabel("Speed (m/s)")
        plt.title("Speed vs Time")
        plt.grid()    
    
    if params['plots.traj3d']:
        # --- 3D trajectory (optional but useful) ---
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot(x, y, z)
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.set_zlabel("z (m)")
        ax.set_title("3D Trajectory")

    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Simulation setup script")
    
    parser.add_argument("--init", action="store_true", help="Prepare initial conditions")
    parser.add_argument("--docs", action="store_true", help="Create a DIP documentation/")
    parser.add_argument("--build", action="store_true", help="Build the code")
    parser.add_argument("--run", action="store_true", help="Run simulation")
    parser.add_argument("--plot", action="store_true", help="Plot resulting data")

    args = parser.parse_args()

    if args.init:
        initialise_header()
    if args.docs:
        create_documentation()
    if args.build:
        build_simulation()
    if args.run:
        run_simulation()
    if args.plot:
        plot_data()

if __name__ == "__main__":
    main()
