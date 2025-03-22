#include <stdio.h>
#include <assert.h>
#include "range_calculator.h" 

void test_calculate_max_range() {
    printf("Running Tests for calculate_max_range:\n");

    // Test Case 1: Normal case
    double result1 = calculate_max_range(100, 5, 50);
    printf("Test 1 - Fuel: 100, Burn Rate: 5, Speed: 50 -> Expected: 1000, Got: %.2f\n", result1);
    assert(result1 == 1000);

    // Test Case 2: Zero fuel (should return 0)
    double result2 = calculate_max_range(0, 5, 50);
    printf("Test 2 - Fuel: 0, Burn Rate: 5, Speed: 50 -> Expected: 0, Got: %.2f\n", result2);
    assert(result2 == 0);

    // Test Case 3: Negative fuel (invalid case)
    double result3 = calculate_max_range(-100, 5, 50);
    printf("Test 3 - Fuel: -100, Burn Rate: 5, Speed: 50 -> Expected: -1, Got: %.2f\n", result3);
    assert(result3 == -1);

    // Test Case 4: Extremely high fuel values
    double result4 = calculate_max_range(100000, 5, 50);
    printf("Test 4 - Fuel: 100000, Burn Rate: 5, Speed: 50 -> Expected: 1000000, Got: %.2f\n", result4);
    assert(result4 == 1000000);

    // Test Case 5: Zero speed (should return 0)
    double result5 = calculate_max_range(100, 5, 0);
    printf("Test 5 - Fuel: 100, Burn Rate: 5, Speed: 0 -> Expected: 0, Got: %.2f\n", result5);
    assert(result5 == 0);

    printf("\nAll test cases completed.\n");
}

int main() {
    test_calculate_max_range();
    return 0;
}
