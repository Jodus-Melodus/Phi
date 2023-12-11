# Phi: A Dynamic Scripting Language
Welcome to Phi, a dynamic scripting language designed for flexibility and ease of use.

## Conventions
- All code should be indented using 4 spaces.
- All code should be written using [Camel Case](https://en.wikipedia.org/wiki/Camel_case) although other cases are supported.
# Reporting Issues
If you encounter any unexpected behavior while using Phi, please report it promptly. Include a screenshot and a detailed description to help us improve.
# Keywords
The following keywords are reserved in the Phi programming language:
- `int` - Declare an integer
- `real` - Declare a floating-point number
- `str` - Declare a string value
- `bool` - Declare a boolean value
- `obj` - Declare an object value
- `array` - Declare an array value
- `lambda` - Used to assign a function
- `if` - [Conditional statement](#if-else-statements)
- `else` - Else clause for [conditional statements](#if-else-statements)
- `while` - [While loops](#while-loops)
- `do` - Part of [do-while](#do-while-loops) loop
- `fn` - Declare a new [function](#user-defined-functions)
- `import` - [Import](#importing-a-module) a module
- `export` - [Export](#exporting-a-module) a value
- All other [built-in functions](#built-in-functions) and methods are also reserved words.
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
- `$` String format character
- `~` Used to name anonymous function
- `<-` Return operator
# Datatypes
## Variables and Constants
- ### Variable:
```
int x = 10
```
- ### Constant:
```
int X = 10
```
## Built-in Constants
The following constants are built into the system:
* `_`: Represents an empty value or nothingness.
* `T` / `F`: Boolean values representing true/false conditions.
## Integer/Real
```
int x = 2
real y = 2.1
```
- ### Operations:
```
int x = 2 + 4 / 2 * 9 - 5 % 3^2
x += 3
x -= 4
x *= 5
x /= 6
x %= 7
x ^= 2
```
## Booleans
```
bool x = T
bool y = F
```
## Strings
```
str x = "Hello, world"
str y = "123 - 2"
str z = "Testing 123"
```
- ### Length:
```
str x = "hello world"
int result = x.length()
```
Result: 
```
11
```
- ### Format:
```
str result = "Hello $ world $".format("there", 500)
```
Result:
```
"Hello there world 500"
```
- ### Concatenation:
```
str x = "hello"
str y = " world"
str result = x + y
str += " !"
```
Result:
```
"hello world !"
```
## Arrays
```
array a = [1, 2, 3]
array b = ["hello", 12, ["world", 9.2]]
```
- ### Length:
```
array a = [1, 4, "hello"]
int result = a.length()
```
Result:
```
3
```
- ### Append:
```
array a = [1, 2, "hello"]
a.append(9.12)
# OR
a = a.append(9.12)
# OR
a += 9.12
```
Result:
```
[1, 2, "hello", 9.12]
```
- ### Join:
```
array arr = [1, 2, "hello"]
str result = arr.join(", ")
```
Result:
```
"1, 2, hello"
```
- ### Indexing:
```
array arr = [1, 5, 90]
int result = arr[2]
```
Result:
```
90
```
## Objects
See [Functions](#user-defined-functions)
```
obj o = {
    name: "John Doe",
    age: 30,
    city: "New York",
    property: value,
    method: fn name(){<-"Hello"}
}
```
- ### Accessing properties:
```
int result = o.age
```
Result:
```
30
```
- ### Adding new properties:
```
o.newProperty = "I am a new property"
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
IDK result = o.method()
```
Result:
```
Hello
```
- ### Adding new Methods:
```
o.newMethod = fn name(){<-"New method"}
```
Result:
```
{
    name: "John Doe",
    age: 30,
    city: "New York",
    property: value,
    method: fn name(){<-},
    newMethod: fn name(){<-"New method"}
}
```
- ### Getting list of keys:
```
array result = o.keys()
```
Result:
```
[
    "name",
    "age",
    "city",
    "property",
    "method",
    "newMethod"
]
```
- ### Getting list of values:
```
array result = o.values()
```
Result:
```
[
    "John Doe",
    30,
    "New York",
    value,
    fn name(){<-},
    fn name(){<-"New method"}
]
```
# Statments
## Built-in Functions
### `Int()`
Return a integer version of the input.
```
int i1 = Int("34")
int i2 = Int(43.2)
```
Output:
```
i1 = 34
i2 = 43
```
### `Real()`
Return a real version of the input.
```
real r1 = Real("34.56")
real r2 = Real(34)
```
Output:
```
r1 = 34.56
r2 = 34.0
```
### `Str()`
Return a string version of the input.=
```
str s1 = Str(23)
str s2 = Str(64.2)
```
Output:
```
s1 = "23"
s2 = "64.2"
```
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
str input = in("> ")
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
int today = now()
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
### `hash`(data)
Generate hash code for data(sha256)
```
str hsh = hash("Hello World!")
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
int result = add(2, 5)
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
int a = 0
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
int b = 0
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
int c = 0
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
# Modules
## Importing a module
```
import math
import math as m
```
## Accessing a module's functions
```
out(math.root(16, 2))
out(m.root(16, 2))
```
Result:
```
4
4
```
## Accessing a module's variables
```
out(math.pi)
```
Result:
```
3.141592653589793
```
## Exporting a module
Also the format for the modules
```
export obj name = {
    variable:value,
    function:value
}
```
Example:
```
export obj math = {
    pi:3.141592653589793,
    root:fn r(radicand, index){<- radicand ^ (1 / index)}
}
```