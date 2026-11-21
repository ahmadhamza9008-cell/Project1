#A variable is a container for storing values. In Python, you can create a variable by assigning a value to it using the assignment operator (=). For example:

# Rules of creating variable in python 
# 1. variable name can contain letters, numbers, and underscores(_)
# 2. variable name must start with a letter or an underscore (_)
# 3. variable names are case-sentitve (e.g. myVariable and mynvariable)
# 4. A variiable name cannot start with a number 
    #2NAME = "John" # Invalid variable name, starts with a number

# Datatypes in python

# 1. Numeric : int, float, and double
    #int 1 = 10 # interger
    #float 1 = 10.5 # float
    #double 1 = 3.12159 # double

# 2. String
    #Name 1 = "Hamza" # string
    #Name 2 = "Hamza" # string

# 3. Tuple 
    ##Tuple 1 = (1, 2, 3) # tuple

# 4. Dictionary 
    #Dict 1 = {"name": "Hamza", "age": 25} # dictionary

# 5. Set
    #Set 1 = {1, 2, 3} # set

# Conditional statement in python
    # if condition

    #if int1 > 5:
        #print("int 1 is greater than 5")
    #else:
       # print("int 1 is not greater than 5")

    #if int1 < 5:
        #print("int 1 is less than 5")
    #else:
        #print("int 1 is not less than 5")


    # for condition
        #for i in range(5):
            #print(i)


    # While condition
# number = 1

# while True:
#     print(number)
#     number +=1 # Keeps counting up endlessly (press ctrl + c to stop)


# Operators in python 

    # 1. Assign operator
        # Sikgn and symbols
            #   =, +=, -=, /=, *=.

            # e.g.
                # x = 10 
                # x += 5  #  same as x = x + 5
                # x -= 3  #  same as x = x - 3
                # x *= 2  #  same as x = x * 2
                # x /= 3  #  same as x = x / 3

    # 2. Comparism operator
        # Sign and Symbols
            # ==, !=, >, <, >=, ,<=

        # e.g.
            # X == Y  # Equal to
            # X != Y  # Not eqaul to
            # 7 > 10  # Greater than
            # 7 < 3  # Less than
            # 5 <= 5  # Greater than or Equal to 
            # 5 <= 10  # Greater than  or Eqlau to 

    # 3. logical operator
        # and, or, not
            # X > 5 and Y < 10  True if both conditioons are true, True
            # X > 5 or Y < 10  True if at least one condition is true, True
            # not (x > 5)  # Negation 
                # it's_raining = True
                # it's_sunny = False
                # print(it's_raining and it's_sunny) # False
                # print(it's_raining or it's_sunny) # true 


    # 4. Bitwise operator
        # AND, OR, XOR, NOT, Left Shift, Rigth shift
            


    # 5. Membership operator
        # in, not in


    # 6. Identity operator
        # is, is not

    # 7. Arithmetic operator
        # +, -, *, /, %, **
            


# Function in python 
    # Function is a reusable block of code that can be call anytime anywhere in our code.

    # def greeting():
    #     no input: = start
    # print("Welcome to Havard")

    # def welcome(name):
        #return f"Welcome,{Hamza}!"
    # print(welcom to Havard("Hamza"))

# Input in function

# name = input("What is your name?")
# print("Hello " + name)

# age = input("How old are your?")
# print(age + " years old")

# temperature = input("What is your temperature? ")
# print(temperature)


# firstName = input("What is your firstName ")
# lastName = input("What is your lastName ")
# print("Your fullname is " + firstName, lastName)

# multiply = input("What is your multiply number? ")
# result = int(multiply) * 2
# addition = input("What is your addition number?")
# result = int(addition)
# print("The result of multiplying " + multiply + " by 2 is: " + str(result))
# print("The result of addition " + addition + str(result))

# num1 = int(input("Enter first number:"))
# operator = input("Enter operator(+, -, *, /):")
# num2 = int(input("Enter second number:"))
# if operator == "+":
#     print(f"Result:{num1 + num2}")
# elif operator == "-":
#     print(f"Result:{num1 - num2}")
# elif operator == "*":
#     print(f"Result:{num1 * num2}")
# elif operator == "/":
#  if num2 != 0:
#     print(f"Result:{num1 / num2}")
# else:
#     print("Cannot devide by zero!")
