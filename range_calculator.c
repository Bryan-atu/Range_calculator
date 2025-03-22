#include <stdio.h>
#include <stdbool.h>
#include "range_calculator.h"

// Requirement ID: REQ-001
// // Description: Calculate the maximum range (in nautical miles) a flight can travel
// // based on fuel capacity (in gallons) and fuel consumption rate (in gallons per hour).
// // Assumptions: Average airspeed is constant at 500 knots.
//
// // Function Declaration
// // Inputs:
// //   - fuel_capacity: Total fuel available in gallons (must be > 0).
// //   - fuel_consumption_rate: Rate of fuel consumption in gallons per hour (must be > 0).
// //   - airspeed: Average airspeed in knots (must be > 0).
// // Output:
// //   - Returns the maximum range in nautical miles as a double.
// //   - Returns -1.0 for invalid input.te_max_range(double fuel_capacity, double fuel_consumption_rate, double airspeed) {


double calculate_max_range(double fuel_capacity, double fuel_consumption_rate, double airspeed) {
    // If there is no fuel, the aircraft cannot travel
    if (fuel_capacity == 0) {
        return 0.0;  // Range should be zero
    }

    if (airspeed == 0) {
        return 0.0;
    }

    // Input validation for other parameters
    if (fuel_capacity < 0 || fuel_consumption_rate <= 0 || airspeed <= 0) {
        return -1.0; // Invalid input
    }

    // Calculate flight duration (hours)
    double flight_duration = fuel_capacity / fuel_consumption_rate;

    // Calculate maximum range (nautical miles)
    double max_range = flight_duration * airspeed;

    return max_range;
}
