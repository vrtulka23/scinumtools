# ⚡ Electromagnetic Force Simulator (C++)

This project demonstrates a simple electromagnetic particle simulation implemented in C++, combined with a lightweight Python workflow for building, running, and analyzing results.

It also showcases how to integrate DIP into a C++/CMake-based build process.

## 🚀 Usage

Run the full pipeline (initialize, build, execute, and plot):

```bash
python3 simulation.py --init --build --run --plot
```

## 📄 Documentation

To generate a PDF containing the DIP parameter documentation:

```bash
python3 simulation.py --docs
```

## 🧩 Overview
C++: Numerical simulation (Lorentz force)
* CMake: Build system
* Python: Workflow automation and plotting
* DIP: Parameter handling and documentation
  
## 📁 Output

The simulation produces:

* `trajectory.csv` — particle trajectory data
* plots generated via `plot.py`
