# Phi: A Dynamic Scripting Language
Welcome to Phi, a dynamic scripting language designed for flexibility and ease of use.
# Reporting Issues
If you encounter any unexpected behavior while using Phi, please report it promptly. Include a screenshot and a detailed description to help us improve.
# Keywords
The following keywords are reserved in the Phi programming language:
- `var` - Declare a variable
- `const` - Define constant value (read only)
- `if` - [Conditional statement](#if-else-statements)
- `else` - Else clause for [conditional statements](#if-else-statements)
- `while` - [While loops](#while-loops)
- `do` - Part of [do-while](#do-while-loops) loop
- `fn` - Declare a new [function](#user-defined-functions)
All other [built-in functions](#built-in-functions) are also reserved words.
# Comments
Comments start with `#` symbol and continue until end of line.
# Operators
The following operators are supported in Phi:
- `=` Assignment operator
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division (integer division)
- `%` Modulus
- `//` Floor division
- `^` Power
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal to
- `<=` Less than or equal to
- `==` Equal to
- `!=` Not equal to
- `&` Logical AND
- `|` Logical OR
- `.` Member access
- `+=` Increment
- `-=` Decrement
- `*=` Multiply by
- `/=` Divide by
- `%=` Remainder after dividing by
- `^=` Exponentiation assignment
- `[...]` Array literal
- `{...}` Object literal
- `"..."` String literals
- `<-` Return operator
# Datatypes
## Built-in Constants
The following constants are built into the system:
* `_`: Represents an empty value or nothingness.
* `T` / `F`: Boolean values representing true/false conditions.
## Integer/Real
```
var x = 2
const y = 2.1
```
- ### Operations:
```
var int = 2 + 4 / 2 * 9 - 5 % 3^2
int += 3
int -= 4
int *= 5
int /= 6
int %= 7
int ^= 2
```
## Booleans
```
var x = T
const y = F
```
## Strings
```
var x = "Hello, world"
var y = "123 - 2"
var z = "Testing 123"
```
- ### Length:
```
var x = "hello world"
var result = x.length()
```
Result: 
```
11
```
- ### Concatenation:
```
var x = "hello"
var y = " world"
var result = x + y
result += " !"
```
Result:
```
"hello world !"
```
## Arrays
```
var arr = [1, 2, 3]
const array = ["hello", 12, ["world", 9.2]]
```
- ### Length:
```
var arr = [1, 4, "hello"]
var result = arr.length()
```
Result:
```
3
```
- ### Append:
```
var arr = [1, 2, "hello"]
arr.append(9.12)
# OR
arr = arr.append(9.12)
# OR
arr += 9.12
```
Result:
```
[1, 2, "hello", 9.12]
```
- ### Indexing:
```
var arr = [1, 5, 90]
var result = arr[2]
```
Result:
```
90
```
## Objects
See [Functions](#user-defined-functions)
```
var obj = {
    name: "John Doe",
    age: 30,
    city: "New York",
    property: value,
    method: fn name(){<-"Hello"}
}
```
- ### Accessing properties:
```
var result = obj.age
```
Result:
```
30
```
- ### Adding new properties:
```
obj.newProperty = "I am a new property"
```
Result:
```
{
    name: "John Doe",
    age: 30,
    city: "New York",
    property: value,
    method: fn name(){<-},
    newProperty: "I am a new property"
}
```
- ### Accessing methods:
```
var result = obj.method()
```
Result:
```
Hello
```
- ### Adding new properties:
```
obj.newMethod = fn name(){<-"New method"}
```
Result:
```
{
    name: "John Doe",
    age: 30,
    city: "New York",
    property: value,
    method: fn name(){<-},
    newMethod: fn name()
}
```
# Statments
## Built-in Functions
### `out()`
Prints the output of any type to console.
Example usage:
```
out("hello world")
```
Output:
```
hello world
```
### `in()`
Reads input from user and returns it as string.
Example usage:
```
var input = in("> ")
```
Input (user):
```
1234567890
```
Output:
```
1234567890
```
### `now()`
Returns current date and time as a real value.
Example usage:
```
var today = now()
```
Output:
```
375612369804852324361987698
```
### `wait()`
Pauses execution for specified amount of seconds.
Example usage:
```
wait(1) # waits for one second
```
### `root`(radicand, index)
Calculates nth root of radicand.
Example usage:
```
root(16, 2) # calculates square root of 16
```
Output:
```
4
```
## User Defined Functions
Functions are defined using the `fn` keyword followed by its name and parameters in parentheses. The function body is enclosed within curly braces.

- ### Creating functions with parameters and return values:
```
fn add(x, y){
    <- x + y
}
```
- ### Calling functions:
```
result = add(2, 5)
```
Result:
```
7
```
## If Else statements
### Conditions:
- #### True
```
(T)
(T | F)
("hello" != "world")
(5 >= 2)
(5 != 2)
(5 > 2)
```
- #### False
```
(T & F)
(F)
(5 == 2)
(5 < 2)
(5 <= 2)
("hello" == "world")
```
- ### Simple if else statement:
```
if (T) {
    <- "True"
} else {
    <- "False"
}
```
Result:
```
True
```
- ### Nested if else statement:
```
if (F) {
    <- "First False"
} else {
    if (T) {
        <- "Second True"
    } else {
        <- "Both False"
    }
}
```
Result:
```
Second True
```
## While Loops
Conditions are the same as [if statements](#if-else-statements)
- ### Looping until a condition is met.
```
var a = 0
while (a < 2) {
    out(a)
    a += 1
}
```
Result:
```
0
1
```
- ### Infinite loop example.
```
var b = 0
while (T) {
    out(b)
    b += 1
}
```
This will run forever, as the while loop's condition always evaluates to true (`T`).
## Do-While Loops
The do-while loop works similarly to the while loop, but it runs at least once before checking the condition.
- ### Example of a do-while loop.
```
var c = 0
do {
    out(c)
    c += 1
} while (c < 3)
```
Result:
```
0
1
2
```
Do-while loops can be useful when you want to ensure that your code block executes at least once regardless of whether or not the condition is false.