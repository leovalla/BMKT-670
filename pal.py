#-------------------------------------------------------------------------------
# palindrome.py
# This project allow the user to explore if a string is a palindrome
# Author: Leonardo Valladares
# Date: 2025-09-06
#------------------------------------------------------------------------------

# Import Modules
import sys

# Define functions

# Function to check if a string is a palindrome
def is_palindrome(string):
    # Check if the string is equal to its reverse
    return string == string[::-1]

# Funtion to check if a string is an inexact palindrome   
def is_inexact_palindrome(string):
    # Remove punctuation and spaces
    string = ''.join(char for char in string if char.isalnum())
    # Check if the string is equal to its reverse
    return string == string[::-1]

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:      # Evaluate that the length of the arguments is 2
    print("Usage: python pal.py <stirng to check>")
    sys.exit(1)             # Exit the program with an error code

# Get user input from command line arguments and convert to lowercase
string_input = sys.argv[1].lower()  
#print(f'\nChecking if "{string_input}" is a palindrome or an inexact palindrome...\n')

# Check if the input is a palindrome or an inexact palindrome
if is_palindrome(string_input):
    print("This is a palindrome.")
elif is_inexact_palindrome(string_input):
    print("This is an inexact palindrome.")
else:
    print("Sorry, this is not a palindrome.")