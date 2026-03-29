#include "config.h"

#include <iostream>
#include <fstream>
#include <cmath>
using namespace std;

// Simple 3D vector
struct Vec3 {
    double x, y, z;

    Vec3 operator+(const Vec3& b) const {
        return {x + b.x, y + b.y, z + b.z};
    }

    Vec3 operator*(double s) const {
        return {x * s, y * s, z * s};
    }
};

// Cross product
Vec3 cross(const Vec3& a, const Vec3& b) {
    return {
        a.y*b.z - a.z*b.y,
        a.z*b.x - a.x*b.z,
        a.x*b.y - a.y*b.x
    };
}

int main() {
    // --- Physical constants (SI) ---
    double q = ICS_ELEMENTARY_CHARGE;
    double m = ICS_PROTON_MASS;

    // --- Initial conditions ---
    Vec3 x = {0.0, 0.0, 0.0};
    Vec3 v = {1e5, 0.0, 0.0};

    Vec3 B = {0.0, 0.0, 1.0};

    double dt = ICS_TIME_STEP;
    int steps = ICS_NUM_STEPS;

    // --- Output file ---
    ofstream file(OUTPUT_FILE);
    file << "t,x,y,z,vx,vy,vz\n";

    double t = 0.0;

    for (int i = 0; i < steps; i++) {
        // Write current state
        file << t << ","
             << x.x << "," << x.y << "," << x.z << ","
             << v.x << "," << v.y << "," << v.z << "\n";

        // Physics: Lorentz force
        Vec3 F = cross(v, B) * q;
        Vec3 a = F * (1.0 / m);

        // Integrate (Euler)
        v = v + a * dt;
        x = x + v * dt;

        t += dt;
    }

    file.close();

    cout << "Simulation complete. Data written to trajectory.csv\n";

    return 0;
}
