#ifndef CONFIG_H
#define CONFIG_H

#include <stdbool.h>

#define RADIATION 
#define SIMULATION_NAME "Configuration test"
const bool SIMULATION_OUTPUT = true;
const float BOX_WIDTH = 12.0;
const double BOX_HEIGHT = 15.0;
const long double DENSITY = 23.0;
const int NUM_CELLS = 100;
const unsigned long long int NUM_GROUPS = 23994957;
const bool VECTOR[3] = {true, true, false};
const int MATRIX[2][3] = {{1, 2, 3}, {4, 5, 6}};

#endif /* CONFIG_H */