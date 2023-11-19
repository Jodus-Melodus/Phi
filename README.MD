# PHI
Phi is a dynamic OOP scripting language.

# Data Structures/Types
- _Integer_ - All positive and negative numbers without decimal
    - 123, -321

- _Real_ - All positive and negative numbers with decimal
    - 123.456, -3583.2

- _Boolean_ - True or False
    - T, F
- _String_ - All the characters of the alphabet
    - "Hello", "John", "testing123"
- _Object_ - A collection of properties accessed with a key
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
- _var_
    - Initializes a variable that can be changed throughout the program
    - var name* = value*
- _const_
    - Initializes a variable that can not be changed throughout the program
    - const name* = value*
- _fn_
    - Initializes a function
    - Automatically returns last evaluation
    - fn name*(parameters*){body*}

# Built-in Functions
- _out("Hello, World")_
    - Takes 1 positional arguement
    - Displays the output in the console
- _in("> ")_
    - Takes 1 positional arguement of type string
    - Reads the user input from the cosole and returns a string
- _now()_
    - Takes 0 positional arguements
    - Returns the current time as a real value
- _length(object)_
    - Takes 1 positional arguement
    - Returns the length of a object's properties as a integer
- _wait(seconds)_
    - Takes 1 positional arguement as a real
    - Halts the program for the amount of seconds specified
- _root(radicand, index)_
    - Takes 2 positional arguements both real
    - Returns the index root of the randicand


# Flow Control Statements
- _If statement_
    - Check if a condition is met and then execute a code block
    - if (condition*){code block/body*}
    - Condition
        - T | F
        - T & F
        - T
        - F
        - 4 == 3
        - "hello" == "hello"


*user defined