# PHI
Phi is a dynamic OOP scripting language.

## Data Structures/Types
### Integer
    var e.g. = 123
    var e.g. = -321
- All positive and negative numbers without decimal
### Real
    var e.g. = 123.456
    var e.g. = -3583.2
- All positive and negative numbers with decimal
### Boolean
    var e.g. = T
    var e.g. = F
- True or False
### String
    var e.g. = "Hello"
    var e.g. = "John"
    var e.g. = "testing123"
- All the characters of the alphabet
### Array
    var e.g. = [1, 2, 3, 4, 5]
    var e.g. = ["hello", 2, 123.2, {a:1, b:2}]
- A list/collection of values
### Object
    var e.g. = {
        a : 123,
        b : "apple",
        c : 2.3,
        d : {
            z : "zebra"
            }
        }
- A collection of properties accessed with a key
    
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
- Return - <-

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
    var name* = value*
- Can be changed throughout the program
### const
    const name* = value*
- Can not be changed throughout the program
### fn
    fn name*(parameters*) {
        body*
        <- returnvalue*
    }

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