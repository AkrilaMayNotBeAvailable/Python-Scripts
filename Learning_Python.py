nome="@AkrilaMayNotBeAvailable"
contato="Github"

"""
    Comment multiple lines
"""

# Basic Operations
"""
print(2**8) # Power of N^m
print(2 == 5) # Boolean type
print(2 != 2) # Boolean type
print(2 < 3 and 3 < 4) # Logic and operation
print(2 > 3 or 4 > 2) # Logic or operation

print(contato[1])
print(contato[-1]) # This works
print(contato[2:]) # This works too
"""

# Methods for strings
"""
string = "Hello world"
lots_of_strings = ["Cachorro", "Sua mãe", "Seu pai"]
modif = string.replace("Hello", "Olá")
print(string.strip()) # Removes white space at beginning or end
print(modif) # Replace substring or char
print(len(modif)) # String size
print(string.split(" ")) # Split strings
print(", ".join(lots_of_strings)) # Concatenate strings from array
print(string.count("o")) # Counts how many times char appears
print(string.find("W")) # Finds char in a string
print(string.lower())
print(string.title())
"""

# More Methods for strings
"""
isupper
islower
capitalize
isalpha
isdecimal
upper
"""

# String format
"""
greeting = "Hello {}. Have a nice day on {}".format(nome, contato)
print(greeting)
"""

# Lists: Arrays, Multiple dimensional arrays
"""
# Append on Array
# Slice arrays
# Arrays are mutable, strings not
# Arrays can be concatenated inside arrays with + sign
# Arrays can be nested inside another array within a new array
This will become a bidimensional array

array_a = [ 30, "Random" ]
array_b = [ 60, "Not so random" ]
array_c = [ array_a, array_b ]
print(array_c[0][1]) # Random
print(array_c[1][0]) # 60

len()
append()
insert()
pop()
del ----(special)
remove(index)
reverse()
index()

print("Akrila" in nome) # Checks if is inside array
print("Akrila" not in nome) # Checks if is inside array

sort()

values = [-1, 0, 1, 12, 15, 18]
new_values = [number + 100 for number in values if number > 0]
print(new_values)
"""

# Tuples: Indexed, immutable collections
"""
# Slicing and index operations work on Tuples
carros = ("Audi Le Mans Cuatro", "Corsa 2008", "Ford Mustango GT")
motos = ("Fazer 138", "XRE 2000", "Harley Davidson")
veiculos = (carros, motos) # Isso vira uma matriz
# veiculos = carros + motos # Isso concatena e aumenta o vetor

print(carros)
print(veiculos)
"""

# Dictionaries: Keywords equivalent to another Keywords, comes in sets of 2
"""
eng_to_br = {
    "Car" : "Carro",
    "Airplane" : "Avião",
    "Rocket" : "Foguete"
}

Car_translation = eng_to_br["Car"]

print(Car_translation)

get()
dict ---(Special)

words = {
    'a': 'Alpha',
    'b': 'Beta',
    'd': 'Delta',
}

words['g'] = 'Gamma'
words['b'] = 'Bravo' # Changes Element
words.pop('a') # Remove element
del words['b'] # Remove element

print(words)
"""

# Sets: Unordered, not indexed collections
"""
Can add tuples, but can't add dictionaries or lists
All elements on a set are unique


first_set = {1, 2, 3}

empty_set = set() # Mister Lonely
second_set = set((5, 10, 15)) # Tuple converted into set

print(first_set)
print(second_set)

# len() method to check set size
# add() method to add elements
# update() method to add multiple elements
# discard() or remove() to remove elements, remove gives error if element is not within
# union() method concatenates elements and returns unique items
# intersection() method returns elements that appear on both sets
# difference() method returns elements within a set that doesn't appear on another set
"""

# Data Structure Types:
"""
Lists
Tuples
Dictionaries
Sets

=================
#Conversion:
Any type can be converted to another type with a determined method
this can be complicated with Dictionaries because they need to be
sets of 2 elements
"""

# Input and conditionals:
"""
number = input('Digite um numero:')
number = int(number)
if number < 0:
    print("Number is lower than 0")
elif number == 0:
    print("Number is Zero")
else:
    print("Number is Positive")
"""

# For loop
"""
for number in range(1, 7):
    print(number)

number = input("Dude say a number: ")
number = int(number)
for number in range(0, number):
    print(number)
"
"""

# While loop
"""
number = 1
while number < 10:
    print(number)
    number += 1 # Updates Iteration like C

number = -1

while number != 0:
    number = input("Dude say another number: ")
    number = int(number)
    print(number)
"""

# For and While on Data Structures
"""
name_list = [   
    ["Mia", "A young human girl that loves to sing"], 
    ["Laticce", "A half-angel girl, was thrown out of heavens"], 
    ["Akrila", "A young girl, guards a stone without power"], 
    ["Yakita", "A famous assassin, she hunts angels"], 
    ["Nyanitta", "A nekomata girl. She Lost her precious key"]
] # Matriz bidimensional / List of lists

numbers = [1, 2, 3]
square_numbers = [] # Empty

for first_number in numbers:
    for second_number in numbers:
        if first_number == 1 or second_number == 1:
            continue # Skip iteration
        current_square = first_number ** second_number
        square_numbers.append(current_square)
        
print(square_numbers)

for name_list in name_list:
    print(name_list)

name_and_personality = dict(name_list) # Dictionary

for key, value in name_and_personality.items():
    print("Character: " + key + "\nPersonality: " + value)
"""

# Functions in Python and Lambda functions
"""
def add(first_n, second_n):
    n_sum = first_n + second_n
    return n_sum
def add_ranged(first_n, second_n):
    result = 0
    
    while first_n < second_n:
        result += first_n
        first_n += 1
        
    return result
def multy_ranged(first_n, second_n):
    product = 1
    
    while first_n < second_n:
        product *= first_n
        first_n += 1
        
    return product
def hello_user(first_name, last_name=""):
    # Optional Argument
    return f"Hello {first_name} {last_name}"
def uppercase_names(list_of_strings):
    for i in range(len(list_of_strings)):
        list_of_strings[i] = list_of_strings[i].upper()
    return list_of_strings
def conversion(operation, value):
    return operation(value)

cities = ["Anima", "Hertagon", "Aeria"]

soma = add(1, 2) # Soma de dois números
soma_ranged = add_ranged(1, 10) # Soma de números em um intervalo
multy = multy_ranged(1, 10)
uppercase_names(cities)

print(cities)
print(soma)
print(soma_ranged)
print(multy)
print(hello_user("Akrila", "Silveria"))

# Lambda Functions
square_value = lambda number : number * number
is_positive = lambda a : f"{a} is positive" if a > 0 else f"{a} is not positive"

feet_meters = lambda feet : feet * 0.3048
meters_feet = lambda meters : meters / 0.3048
kilo_miles = lambda kilo : kilo / 1.609344
miles_kilo = lambda miles : miles * 1.69344

print(square_value(256))
print(is_positive(20))
print(conversion(meters_feet, 310))

# map()
# filter()
"""

# Decorators
"""
def reverse_list(initial_list):
    return initial_list[::-1]
def reverse_input_list(func, initial_list):
    return func(initial_list)
# Functions can be nested
def positive_numbers_decorator(input_list):
    def func_wrap():
        numbers = [number for number in input_list() if number > 0]
        return numbers
    
    return func_wrap

@positive_numbers_decorator # Nested functions can be Decorators
def get_number_list():
    return [1, -2, 3, -4, 5, -10, 12]

list_of_numbers = [1, 2, 3, 4]
# Positive_n_decorator is being applied to get_number_list
result = get_number_list() 

print(result)

#print(reverse_input_list(reverse_list, list_of_numbers))
"""

# OOP in Python (Methods, Constructors) --- Kinda complicated
"""
class Bicycle:
    def __init__(self, manufacturer=None, color="undefined", is_sporty=False):
        self.manufacturer = manufacturer
        self.color = color
        self.is_sporty = is_sporty
        
        
fav_bike = Bicycle("Honda", "Red", False)
"""