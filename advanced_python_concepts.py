# Advanced Python Concepts: Examples

# 1. List Comprehensions with Conditions
# Create a list of squares of even numbers from 0 to 9
squares_of_even = [x**2 for x in range(10) if x % 2 == 0]
print("List Comprehensions with Conditions:")
print(f"squares_of_even: {squares_of_even}\n")

# 2. Lambda Functions and map/filter/reduce
from functools import reduce

nums = [1, 2, 3, 4, 5]
# Use map to square each number in the list
squared = list(map(lambda x: x**2, nums))
# Use filter to keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, nums))
# Use reduce to multiply all numbers together
product = reduce(lambda x, y: x * y, nums)
print("Lambda Functions and map/filter/reduce:")
print(f"squared: {squared}")
print(f"evens: {evens}")
print(f"product: {product}\n")

# 3. Decorators
# A decorator is a function that modifies the behavior of another function
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")      # Code before the function
        result = func(*args, **kwargs)     # Call the original function
        print("After function call")       # Code after the function
        return result
    return wrapper

# Apply the decorator to say_hello
@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")               # Print a greeting

print("Decorators:")
say_hello("Alice")                         # Call the decorated function
print()

# 4. Generators
# A generator yields values one at a time, saving memory
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a                            # Yield the next Fibonacci number
        a, b = b, a + b                    # Update values

print("Generators:")
print(f"First 7 Fibonacci numbers: {list(fibonacci(7))}\n")

# 5. Context Managers
# Custom context manager for file handling
class CustomFile:
    def __init__(self, filename, mode):
        self.file = open(filename, mode)   # Open the file
    def __enter__(self):
        return self.file                   # Return the file object
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()                  # Ensure the file is closed

print("Context Managers:")
with CustomFile("advanced_sample.txt", "w") as f:
    f.write("Using a custom context manager.\n")  # Write to the file
with open("advanced_sample.txt", "r") as f:
    print(f"File content: {f.read()}")            # Read and print file content

# 6. Exception Handling with Custom Exceptions
# Define a custom exception for negative numbers
class NegativeNumberError(Exception):
    pass

# Recursive factorial function with error checking
def factorial(n):
    if n < 0:
        raise NegativeNumberError("Negative numbers are not allowed.")  # Raise custom error
    return 1 if n == 0 else n * factorial(n - 1)                        # Recursive case

print("\nException Handling with Custom Exceptions:")
try:
    print(f"Factorial of 5: {factorial(5)}")        # Should succeed
    print(f"Factorial of -1: {factorial(-1)}")      # Should raise error
except NegativeNumberError as e:
    print(f"Error: {e}")                            # Handle the custom error

# 7. Object-Oriented Programming: Inheritance and Polymorphism
class Animal:
    def speak(self):
        return "Some sound"                         # Base method

class Dog(Animal):
    def speak(self):
        return "Woof!"                              # Override for Dog

class Cat(Animal):
    def speak(self):
        return "Meow!"                              # Override for Cat

print("\nObject-Oriented Programming:")
animals = [Dog(), Cat(), Animal()]                  # List of different animals
for animal in animals:
    print(animal.speak())                           # Polymorphic call