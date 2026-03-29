cmake_minimum_required(VERSION 3.10)

# Project name
project(EMSimulation)

# Use modern C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Create executable
add_executable(sim main.cpp)
