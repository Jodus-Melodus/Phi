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
- `break` - Terminates the loop. Works for [while loop](#loop-with-break), [do while loop](#loop-with-break-1) and [for loop](#for-loop)
- `continue` - Skips to the next iteration of the loop
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
This will create the variable and give it a value of 0
```
int x
```
- ### Constant:
```
int X = 10
```
This will create the variable and give it a value of 0
```
int X
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
### `output()`
Prints the output of any type to console.
Example usage:
```
output("hello world")
```
Output:
```
hello world
```
### `input()`
Reads input from user and returns it as string.
Example usage:
```
str input = input("> ")
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
## Case Statements
Case statements are similar to if else statements, but they can handle multiple conditions. They work by comparing a value with different cases and executing the code block of the value if it matches. The code block is a default code block and does not need to return a value.
```
int x = 3

str r = match x {
    case 1 {<- "one"}
    case 2 {<- "two"}
    case 3 {<- "three"}
    case 4 {<- "four"}
    case 5 {<- "five"}
}

output(r)
```
Result:
```
three
```
## While Loops
Conditions are the same as [if statements](#if-else-statements)
- ### Looping until a condition is met.
```
int a = 0
while (a < 2) {
    output(a)
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
    output(b)
    b += 1
}
```
This will run forever, as the while loop's condition always evaluates to true (`T`).
- ### While Loop with break
To exit early from a loop you can use `break`.
```
int c = 0
while (T) {
    output(c)
    c += 1
    if (c == 5) {
        break
    }
}
```
Result:
```
0
1
2
3
4
```
- ### While Loops with continue
`continue` skips the rest of the current iteration and jumps directly to the next one.
```
d = 0
while (T) {
    d += 1
    if (d % 2 == 0) {
        continue
    }
    output("I am odd!")
}
```
Result:
```
I am odd!
I am odd!
I am odd!
```
## For Loops
For loops have three parts separated by colons (`,`)
- ### Example of a for loop.
```
for (int i = 0, i < 5, i += 1){
    output(i)
}
```
Result:
```
0
1
2
3
4
```
The variable `i` starts at 0 and continues until it is no longer less than 5. After each iteration, `i` is incremented.
- ### For Loop with break
```
for (int j = 0; j < 10; j++){
    if (j == 5){
        break
    }
}
```
Result:
```
0
1
2
3
4
```
- ### For Loop with continue
The `continue` statement skips the rest of the code in the current iteration and moves on to the next one.
```
for (k = 0; k <= 9; k++) {
    if (k % 2 == 0) {
        continue
    }
}
```
Result:
```
1
3
5
7
9
```
## For-Each Loops
For-each loops are used when you want to perform an action on each element in a collection without having to manually iterate through it using an index.
```
array a = [6, 4, 29, 234, 1209, 98203, 12, 0, 2]

for each (int i in a){
    output(i)
}
```
Result:
```
6
4
29
234
1209
98203
12
0
2
```
## Do-While Loops
The do-while loop works similarly to the while loop, but it runs at least once before checking the condition.
- ### Example of a do-while loop.
```
int c = 0
do {
    output(c)
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
- ### Do-While Loop with break
```
int j = 0
do {
    j += 1
    if (j > 5) {
        break
    }
} while (T)
```
Result:
```
1
2
3
4
5
```
- ### Do-While Loop with continue
```
int k = 0
do {
    k += 1
    if (k % 2 == 0) {
        continue
    }
    output(k)
} while (k < 10)
```
Result:
```
1
3
5
7
9
```
# Modules
## Importing a module
```
import math
import math as m
```
## Accessing a module's functions
```
output(math.root(16, 2))
output(m.root(16, 2))
```
Result:
```
4
4
```
## Accessing a module's variables
```
output(math.pi)
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
# Error Handeling
## Try-Catch
The try block is where you put the code that might throw an error. The catch block is where you handle it if there is one.
```
try {
    int x = 5 / 0
} catch (zeroDivisionError) {
    output("Can't devide a number by 0")
}
```
Result:
```
Can't divide a number by 0
```
## Throw
You can also throw an error if something goes wrong in your code. This is useful when you want to handle errors yourself instead of letting them crash your program.
```
throw syntaxError
```