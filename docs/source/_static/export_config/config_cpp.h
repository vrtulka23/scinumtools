#ifndef CONFIG_H
#define CONFIG_H

#define RADIATION 
#define SIMULATION_NAME "Configuration test"
constexpr bool SIMULATION_OUTPUT = true;
const float BOX_WIDTH = 12.0;
const double BOX_HEIGHT = 15.0;
constexpr long double DENSITY = 23.0;
constexpr int NUM_CELLS = 100;
constexpr unsigned long long int NUM_GROUPS = 23994957;
constexpr bool VECTOR[3] = {true, true, false};
constexpr int MATRIX[2][3] = {{1, 2, 3}, {4, 5, 6}};

#endif /* CONFIG_H */