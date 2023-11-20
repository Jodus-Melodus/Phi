# PHI
Phi is a dynamic OOP scripting language.

# Data Structures/Types
- Integer - All positive and negative numbers without decimal
    - 123, -321

- Real - All positive and negative numbers with decimal
    - 123.456, -3583.2

- Boolean - True or False
    - T, F
- String - All the characters of the alphabet
    - "Hello", "John", "testing123"
- Object - A collection of properties accessed with a key
    - {a : 123, b : "apple", c : 2.3, d : {z : "zebra"}}
    
# Important Symbols
- Assignment =
- Plus/Addition +
- Minus/Subtraction -
- Multiplication *
- Division /
- Modulus %
- Power of ^
- Comments #
- Or - |
- And - &
- Equal - ==
- Not Equal - !=

# Built-in Constants
- null/nil/none - _
- True - T
- False - F

# Keywords
### var
    - Initializes a variable that can be changed throughout the program
    - var name* = value*
### const
    - Initializes a variable that can not be changed throughout the program
    - const name* = value*
### fn
    - Initializes a function
    - Automatically returns last evaluation
    - fn name*(parameters*){body*}

# Built-in Functions
### out("Hello, World")
    - Takes 1 positional arguement
    - Displays the output in the console
### in("> ")
    - Takes 1 positional arguement of type string
    - Reads the user input from the cosole and returns a string
### now()
    - Takes 0 positional arguements
    - Returns the current time as a real value
### length(object)
    - Takes 1 positional arguement
    - Returns the length of a object's properties as a integer
### wait(seconds)
    - Takes 1 positional arguement as a real
    - Halts the program for the amount of seconds specified
### root(radicand, index)
    - Takes 2 positional arguements both real
    - Returns the index root of the randicand

# Flow Control Statements
### If
    - Check if a condition is met and then execute a code block
    - if (condition*){code block/body*}
    - Condition
        - T | F
        - T & F
        - T
        - F
        - 4 == 3
        - "hello" == "hello"
### While
    - Run code repeatedly until a condition is false
    - while (condition*){code block/body*}
    - Condition is same as [If statement](#if)


*user defined