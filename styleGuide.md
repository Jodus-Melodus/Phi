# Phi Style Guide

## Naming Conventions

- Use camelCase for variable and function names. For example, `myVariable` or `calculateSquare()`.
- File/Modules are also named using camelCase.
- Constants are in all caps.

## Indentation

- Always use four spaces for indentation. Never tabs.

## Whitespace

- Place one space after commas in lists/arrays/objects.
- Avoid trailing whitespace at the end of lines.
- Always add whitespace around these operators. (`+`, `-`, `*`, `/`, `:`)
- There should always be a whitespace before an opening brace (`{`)
- No whitespaces after the function name.

Example:

```phi
# Correct
fn add() {}

# Incorrect
fn add () {}
```

- Always add a whitespace after the return(`<-`) operator.

## Comments

- Write comments to explain complex code sections. Keep them concise and clear.
- Do not overuse inline comments (comments on a single line). If something is obvious it doesn't need commenting.
- Do not overuse comments; if a piece of code is unclear, refactor it instead.
- Inline comments must have atleast 4 spaces infront of the `#` and one trailing space.
- Comments should always start with a capital letter.

Example:

```phi
int x = 5     # This initializes the variable x to 5
```

## Function Signatures

- Function signatures (the part before the `{`) should be on a single line:

```phi
functionName(parameter1, parameter2, ...) {

}
```

## Variable Declarations

- The assignment operator (`=`) should be surrounded by single whitespace characters.

Example:

```phi
int x = 3
```

- Only assign a value to `unknown` when it is necessary.

## Code blocks

- Code inside curly braces (`{}`) should be placed on separate lines with proper indentation.
- Each level of indentation should be 4 spaces from its parent block.
- The first curly brace should be in the same line as the function/object declaration.
- The closing curly brace should be on a new line by itself.

Example:

```phi
obj object = {
    ...
}
```

- If code blocks are empty or they only contain one line, they should be collapsed.

Example:

```phi
fn add(a, b) {}

fn add(a, b) {<- a + b}
```

- When other statements follow the block like `if else`, `while else`, `do while else`, `try-catch` the second statement is in the same line as the closing curly brace.
- `try-catch` statements are never collapsed.

Example:

```phi
if (a > b){
    output(T)
} else {
    output(F)
}
```

## Conditions

- Should always be in `()` (parenthesis)

## Imports

- Imports are separated into two groups: standard libraries and user defined modules.
- Standard Libraries go first followed by User Defined Modules.
- There should be exactly one blank line between these two groups.

Example:

```phi
import math

import userDefined
```

- Always `import` similar modules in the same line.
- When importing a module `as` another name do it in it's own separate line.

Example:

```phi
# Correct
import math as m
import debug

# Incorrect
import math as m, debug
```

## Exports

- Only export **ONE** (**1**) value in a file.
- If you need to export multiple values use an object.

Example:

```phi
export obj a = {
    x : 5,
    y : "hello",
    z : fn add(a, b) {<- a + b}
}
```

## Error Handling

- Error handling is done using try-catch statements.
- The error should always be in `()`.
- The throw statement should always include an error and a message seperated by a single space.

Example:

```phi
try {
    # code that might cause an exception
    } catch (error) {
        # handle the error here
        throw error "Error Message"
}


```

## Commas

- Always use commas to separate items in arrays and function parameters.

Example:

```phi
array a = [3, 2, "hello world"]
```

## Strings

- Use double quotes (`""`) for strings.

## Flow Control Statements

- All flow control statements have a block of code associated with them.
- The code block should be collapsed if it only uses one line unless it is nested.

Example:

```phi
# Correct
if (a > b) {output(T)} else {output(F)}

# Incorrect
if (F) {<- "First False"} else {if (T) {<- "Second True"} else {<- "Both False"}}
```

## Case Statements

- Each case should be in it's own line.
- Collapse the case body if it contains only one expression.

Example:

```phi
int x = 3

str r = match x {
    case 1 {<- "one"}
    case 2 {<- "two"}
    case 3 {<- "three"}
    case 4 {<- "four"}
    case 5 {<- "five"}
}
```

## Loops

- Collapse the body if it contains only one expression.
- `for` loops's expressions should be separated by `,`.

Example:

```phi
for (int i = 0, i < 5, i += 1) {output(i)}
```

- Limit using of `continue` and `break`
- When using `for-each` statement try not to use `unknown` rather use the correct data type. (This only applies when the list does not contain just a single data type.)
