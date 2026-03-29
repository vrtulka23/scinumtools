#ifndef CONFIG_H
#define CONFIG_H

constexpr double ICS_PROTON_MASS = 1.672623e-27;
constexpr double ICS_ELEMENTARY_CHARGE = 1.602176634e-19;
constexpr double ICS_TIME_STEP = 1e-09;
constexpr int ICS_NUM_STEPS = 10000;
const char* OUTPUT_FILE = "trajectory.csv";
constexpr bool PLOTS_TRAJ2D = true;
constexpr bool PLOTS_TRAJ3D = true;
constexpr bool PLOTS_VELOCITY = true;

#endif /* CONFIG_H */