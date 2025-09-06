#-------------------------------------------------------------------------------
# compount.py
# This project claculates the countenues interest and the compounded interest
# Author: Leonardo Valladares
# Date: 2025-09-05
#------------------------------------------------------------------------------

# Import Modules
import math
import sys

## Fomula for countinues Interest amount = principal * e^(rate * years)

# Check if the correct number of arguments are provided
if len(sys.argv) != 4:      # Evaluate that the length of the arguments is 4
    print("Usage: python compound.py <years> <principal> <rate>")
    sys.exit(1)             # Exit the program with an error code

# Get user input from command line arguments
years = float(sys.argv[1])      # Number of years the money is invested or borrowed for
principal = float(sys.argv[2])  # Initial amount of money (the principal)
rate = float(sys.argv[3])       # Annual interest rate (as a decimal)  

# Calculate Continuous interest amount
# It idealized growth by compounding at every instant
continuous_amount = principal * math.exp(rate * years)

# Formula for compounded interest amount = principal * (1 + rate/n)^(n*years)
# where n is the number of times that interest is compounded per year
# We are assuming interest is compounded annually, so n = 1

# Calculate compounded interest amount
n = 1  # Compounded annually
compounded_amount = principal * (1 + rate/n)**(n*years)


# Display the result
print(f"After {years:.1f} years at an interest rate of {rate*100:.2f}%,")
print(f"the amount of money accumulated for Continuous Interest is: ${continuous_amount:.2f},")
print(f"and the amount of money accumulated for Compounded Interest is: ${compounded_amount:.2f}")