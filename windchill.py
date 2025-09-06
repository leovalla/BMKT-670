#-------------------------------------------------------------------------------
# compount.py
# This project claculates wind chill
# Author: Leonardo Valladares
# Date: 2025-09-05
#------------------------------------------------------------------------------

import sys

## Asumptions:
# The formula to calculate wind chill is: w = 35.74 + 0.6215*t + (0.4275*t - 35.75)*v**0.16
#   * Temperature t is in Fahrenheit
#   * Wind speed v is in miles per hour
#   * The formula is not valid if t is larger than 50 in absolute value or 
#     if v is larger than 120 or less than 3. 

# Check if the correct number of arguments are provided
if len(sys.argv) != 3:      # Evaluate that the length of the arguments is 3
    print("Usage: python windchill.py <temperature in Fahrenheit> <wind speed in mph>")
    sys.exit(1)             # Exit the program with an error code

# check if the input values are within the valid range
if not (-50 <= float(sys.argv[1]) <= 50) or not (3 <= float(sys.argv[2]) <= 120):     
    print("Error: Temperature must be between -50 and 50 Fahrenheit, and wind speed must be between 3 and 120 mph.")
    sys.exit(1)             # Exit the program with an error code

# Get user input from command line arguments
t = float(sys.argv[1])      # Temperature in Fahrenheit
v = float(sys.argv[2])      # Wind speed v in miles per hour

# Calculate wind chill (w)
w = 35.74 + 0.6215*t + (0.4275*t - 35.75)*v**0.16

# Display the result
print(f"At a temperature of {t:.1f} degrees Fahrenheit")
print(f"and a wind speed of {v:.1f} miles per hour,")
print(f"The wind chill index is: {w:.3f} degrees Fahrenheit")