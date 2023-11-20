# PHI
Phi is a dynamic OOP scripting language.

## Data Structures/Types
### Integer - All positive and negative numbers without decimal
    var e.g. = 123
    var e.g. = -321
### Real - All positive and negative numbers with decimal
    var e.g. = 123.456
    var e.g. = -3583.2
### Boolean - True or False
    var e.g. = T
    var e.g. = F
### String - All the characters of the alphabet
    var e.g. = "Hello"
    var e.g. = "John"
    var e.g. = "testing123"
### Object - A collection of properties accessed with a key
    var e.g. = {
        a : 123,
        b : "apple",
        c : 2.3,
        d : {
            z : "zebra"
            }
        }
    
## Important Symbols
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

## Built-in Constants
- null/nil/none - _
- True - T
- False - F

## Conditions
    (T | F)
    (T)
    (F)
    (3 == 3)
    (3 != 2)
    ("hello" & "hi")

## Keywords
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

## Built-in Functions
### out()
    out("Hello, world")
- Arguements
    - string
- Displays the output in the console
### in()
    in("> ")
- Arguements
    - string
- Reads the user input from the cosole and returns a string
### now()
    now()
- Returns the current time as a real value
### length()
    length(object)
- Arguements
    - object
- Returns the length of a object's properties as a integer
### wait()
    wait(5)
- Arguements
    - real | integer
- Halts the program for the amount of seconds specified
### root()
    root(5, 2)
- Arguements
    - real | integer (radicand)
    - real | integer (index)
- Returns the index root of the randicand

## Flow Control Statements
### If
    if (condition*) {
        code block/body*
    }
- Check if a condition is met and then execute a code block
- [Conditions](#conditions)
### While
    while (condition*) {
        code block/body*
    }
- Run code repeatedly until a condition is false
- [Conditions](#conditions)


*user defined