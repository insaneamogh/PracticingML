# Python Basics: Detailed Explanations and Examples

# 1. Variables and Data Types
# Variables store data. Python is dynamically typed.
name = "Alice"         # str (string)
age = 30               # int (integer)
height = 1.65          # float
is_student = False     # bool (boolean)

print("Variables and Data Types:")
print(f"name: {name}, age: {age}, height: {height}, is_student: {is_student}\n")

# 2. Lists
# Lists are ordered, mutable collections.
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")  # Add an item
print("Lists:")
print(f"fruits: {fruits}")
print(f"First fruit: {fruits[0]}")
# More list operations
fruits.remove("banana")  # Remove an item by value
print(f"After removing 'banana': {fruits}")
fruits.insert(1, "grape")  # Insert at index 1
print(f"After inserting 'grape' at index 1: {fruits}")
print(f"Length of list: {len(fruits)}")
numbers = [10, 20, 30]
sum_numbers = sum(numbers)  # Sum of elements
print(f"Sum of numbers: {sum_numbers}")
divided = [x / 2 for x in numbers]  # Divide each element by 2
print(f"Numbers divided by 2: {divided}\n")

# 3. Tuples
# Tuples are ordered, immutable collections.
coordinates = (10.0, 20.0)
print("Tuples:")
print(f"coordinates: {coordinates}")
print(f"X coordinate: {coordinates[0]}")
# More tuple operations
tuple1 = (1, 2, 3)
tuple2 = (4, 5)
concatenated = tuple1 + tuple2  # Concatenate tuples
print(f"Concatenated tuple: {concatenated}")
print(f"Length of tuple1: {len(tuple1)}")
# Accessing a slice
print(f"Slice of tuple1 (first two elements): {tuple1[:2]}\n")

# 4. Sets
# Sets are unordered collections of unique elements.
unique_numbers = {1, 2, 3, 2, 1}
unique_numbers.add(4)
print("Sets:")
print(f"unique_numbers: {unique_numbers}")
# More set operations
set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}
union = set_a | set_b  # Union of sets
intersection = set_a & set_b  # Intersection of sets
difference = set_a - set_b  # Elements in set_a but not in set_b
symmetric_diff = set_a ^ set_b  # Elements in either set, but not both
print(f"Union: {union}")
print(f"Intersection: {intersection}")
print(f"Difference (set_a - set_b): {difference}")
print(f"Symmetric Difference: {symmetric_diff}")
print(f"Length of set_a: {len(set_a)}\n")

# 5. Operators
# Arithmetic, comparison, logical, and assignment operators.
a, b = 5, 3
print("Operators:")
print(f"a + b = {a + b}")      # Addition
print(f"a - b = {a - b}")      # Subtraction
print(f"a * b = {a * b}")      # Multiplication
print(f"a / b = {a / b}")      # Division
print(f"a > b: {a > b}")       # Comparison
print(f"a == b: {a == b}")     # Equality
print(f"a and b: {a and b}")   # Logical AND
a += 2                         # Assignment
print(f"a after a += 2: {a}\n")

# 6. Logic (if, elif, else)
print("Logic:")
if age < 18:
    print("Minor")
elif age < 65:
    print("Adult")
else:
    print("Senior")
print()

# 7. Functions
# Functions are reusable blocks of code.
def greet(person):
    """Greets the person by name."""
    return f"Hello, {person}!"

print("Functions:")
print(greet(name))
print()

# 8. Strings
# Strings are sequences of characters.
message = "Hello, World!"
print("Strings:")
print(f"Uppercase: {message.upper()}")
print(f"Split: {message.split(', ')}\n")

# 9. File Handling
# Reading from and writing to files.
print("File Handling:")
with open("sample.txt", "w") as f:
    f.write("This is a sample file.\n")

with open("sample.txt", "r") as f:
    content = f.read()
    print(f"File content: {content}")

# 10. Modules
# Modules are files containing Python code. Use 'import' to use them.
import math
print("Modules:")
print(f"Square root of 16: {math.sqrt(16)}")