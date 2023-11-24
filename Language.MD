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
- Assignment 
    - =
- Plus/Addition 
    - +
- Minus/Subtraction 
    - -
- Multiplication 
    - *
- Division 
    - /
- Modulus 
    - %
- Powers 
    - ^
- Comments 
    - #
- Or 
    - |
- And 
    - &
- Equal 
    - ==
- Not Equal 
    - !=
- Greater than 
    - \>
- Less than 
    - <
- Greater than or equal to 
    - \>=
- Less than or eqaul to 
    - <=
- Return 
    - <-
- Add-assign(increment) 
    - +=
- Subtract-assign(decrement)
    - -=
- Multiply-assign
    - *=
- Divide-assign
    - /=
- Modulus-assign
    - %=
- Power-assign
    - ^=

## Built-in Constants
- null/nil/none (_)
- True (T)
- False (F)

## Conditions
### True
    (T)
    (3 == 3)
    ("hello" != "hi")
    (3 > 2)
    (9 >= 2)
### False
    (F)
    (4 < 2)
    (3 <= 2)
    (F | F)
    (4 == 2)

## Expressions
### var
    var name* = value*
- Can be changed throughout the program
### const
    const name* = value*
- Can not be changed throughout the program
## Built-in Functions
### out()
    out("Hello, world")
- Arguments
    - string
- Displays the output in the console
### in()
    in("> ")
- Arguments
    - string
- Reads the user input from the cosole and returns a string
### now()
    now()
- Returns the current time as a real value
### length()
    length(object)
- Arguments
    - object
- Returns the length of a object's properties as a integer
### wait()
    wait(5)
- Arguments
    - real | integer
- Halts the program for the amount of seconds specified
### root()
    root(5, 2)
- Arguments
    - real | integer (radicand)
    - real | integer (index)
- Returns the index root of the randicand

## Statements
### fn
    fn name*(parameters*) {
        body*
        <- returnvalue*
    }
### If
    if (condition*) {
        body*
    }

    var x = if (a == b){<-a}
- Check if a condition is met and then execute a code block
- [Conditions](#conditions)
### While
    while (condition*) {
        body*
    }
- Run code repeatedly until a condition is false
- [Conditions](#conditions)
### Do-While
    do {
        body*
    } while (condition*)
- Run code once then repeatedly until a condition is false
- [Conditions](#conditions)

*user defined