# Guidelines Documentation

Documentation of the Guidelines and Style followed on the coding of the Industry 4.0 project of Boehringer Ingelheim, and, also, of the application to check that the code is following the guidelines.
For more information about the application visit the [About](http://127.0.0.1:8000/about/) page.

## Guidelines and style
These code guidelines and style are are a combination of the inmation's ESI Coding Standards, the S+S' style, the Luacheck lintern, and various coding standards of the Lua language. The compliance of these rules is checked through the GuideLua application.


### 1. Formatting

#### 1.1. Code encoding
The project must use the UTF-8 encoding.

#### 1.2. Line break type
The project must use the CRLF ( carriage return `\r` + line feed `\n`) line break type because the operating system will be Windows.

#### 1.3. Indentation
The default tab size must be of 4 spaces.

local function foo( )
    local j = 0
end
&nbsp;

#### 1.4. Usage of the TAB character
the `\t` character should not be used, instead, to indicate an indentation (tab size), use 4 spaces.

#### 1.5. Trailing spaces
Avoid the usage of trailing spaces.

#### 1.6. Line length
 The maximum code line length permitted is of 120 characters. The longer instructions can be broken like this:

    local function()
    local suc,res=pcall(
        function() return inmation.setvalue(self.path..".StateManagement.StateTable",self.tstate) end
    )


likewise, for larger strings use multi-line strings:

    local longString = [[This is a string that
    even though you change of line
    is always recognized as the same string
    mostly used for SQL queries
    ]]

### 2. Naming conventions

#### 2.1. Naming of variables, functions, and arguments

The chosen notation is Camel Case with some variations detailed below -

| Index number | Element type   |      Scope      |  Notation |  Example  |
|:------------:|:----------------:|:-----------------:|:-----------:|:-----------:|
| 2.1.1. | Variable | Local | Lower Camel Case | `decInt` |
| 2.1.2. | Variable | Global | Upper Camel Case | `GitVersion` |
| 2.1.3. | Function | Local | Underscore followed by Lower Camel Case | `_deleteOne` |
| 2.1.4. | Function | Global | Upper Camel Case | `GetSum()` |
| 2.1.5. | Arguments | n/a | Lower Camel Case | `paramExample` |
| 2.1.6. | Library | n/a | According to the namespace in the system, where every single namespace in the Upper Camel Case is separated by dots | `SuS.Mailer` |

&nbsp;

#### 2.2. Libraries naming
The libraries should follow the scheme of `<Environment>.[<System>][.<Module>]*`, so, in the case of Boehringer Ingelheim this scheme by default should be `BI.<Use Case or scope>.<Functionality>`

    -- example
    BI.SAP.IdocReceiver

#### 2.3. Libraries calls
The libraries are always called when a function is created or from inside the code as

    --good calling notation
    --name of the library : FunctionName
    lib:Function()

#### 2.4. Unneeded variables
The unneeded variables are notated using `_`.

    for _,v in ipairs(t) do
    print(v)
    end

#### 2.5. Hungarian Notation
Don't use Hungarian notation. Don't add information about the type of data the variables carry, only use its name to describe its purpose.

    -- DON'T
    local bIsBoolean = false

    -- DO
    local isBoolean = true

#### 2.6. Bad characters
Check if the code has some characters outside [0,127] in the ASCII table

### 3. Layout

#### 3.1. Operators

Use spaces around operators

        -- DON'T
        local var1 = 3+2
        if (var1==3)
        then
            --empty
        end

        -- DO
        local var2 = 3 + 2
        if (var2 == 3)
        then
            --empty
        end

#### 3.2. Spaces next to brackets

No spaces are permitted after the `([` characters and before the `)]` characters.

        -- DON'T
        if ( var1==3 )
        then
            --empty
        end

        -- DO
        if (var2 == 3)
        then
            --empty
        end

#### 3.3. Space alignment of items using spaces
Align variable assignments, function arguments and other code items that repeat structure.

    -- DON'T
    local var1 = "Hi"
    local varNewLarge = "Hi large"

    -- DO
    local var1        = "Hi"
    local varNewLarge = "Hi large"

#### 3.4. Empty lines between functions bodies
Leave an empty line between the `end` line of a function and the beggining of the next function.

    -- DON'T
    local function one()
        -- body
    end
    local function two()
        -- body
    end

    -- DO
    local function one()
        -- body
    end

    local function two()
        -- body
    end

#### 3.5. Maximum of successive empty lines permitted
The maximum number of successive empty lines permitted is of 2.

### 4. Comments
Try to avoid the usage of comments. Only write comments that are necessary to the understanding of the code, i.e., when a certain program logic is not completely obvious.

#### 4.1 Comments language
All comment shall be written in the English language.

#### 4.2. Inline single-line comments
If it is necessary to comment something, use single line comments using the characters `--` and, afterwards, the comment.

    print("It ends!") -- this print serves to know when something has finished



#### 4.3. Space between the comment starting mark and the text
Separate the comment mark and the comment itself with a single space

    --DON'T
    -- DO

#### 4.4. Luadoc Docstrings
Use Luadoc Docstring for formal comment documentation.
Use @param and @return if existing to document functions parameters and returning values, their purpose and specifications.

    -- @param p1 first parameter
    -- @return c string value
    local function (p1)
    end

#### 4.5. Commented code
Delete all the commented code that could exist on the files. Use the repository history (versions) as a wiki to find all the not-being-used code.

### 5. Keywords in comments
Use the `todo`, `bug` and `note` tags.
It is also possible to, if wanted, add the name or alias of the person responsible of this annotated code between parentheses.

    -- TODO: Finish function development (Mariana) 

#### 5.1. `todo`
Use this tag to indicate that there is a required improvement which the author of the comment is aware of, but could not be implemented yet.

#### 5.2. `bug`
Use this tag to indicate that there is a bug which needs to be fixed.

#### 5.3. `note`
Use this keyword to denote an important statement about the code found below

### 6. Scopes

#### 6.1. Preferred scope
The preferred scope to use is local

#### 6.2. Use of modules instead of the global scope
In most cases, it is better to use modules instead of storing very different data in the global scope.

#### 6.3. Creation of local aliases
It is preferred to create local aliases when there is a `require` of a module.

### 7. Strings

#### 7.1. Usage of double-quoted strings
It is preferred to use double-quoted strings (`"hello"`) instead of the single-quoted strings (`'hello'`). Otherwise, for longer strings (longer than 100 characters), use multi-line strings (`local string = [[multiline string
continues]]`).

### 8. Functions
All functions within a library (in this case `lib`) must be defined with the colon notation

    --good calling notation
    --name of the library : FunctionName
    lib:Function()

If the function is to be exposed by the library, its name has to be capitalized, if it is an internal (helper) function, it must be lowercase with a trailing underscore.

In cases where the intrinsic `self` parameter is not used, we need to do a classic dot-based declaration in order to not raise linter problems.

    -- this would not please the linter, because the invisible self parameter is not used in the function body
    function lib:_makesqldate(posix)
        return inmation.gettime(posix):sub(1,19)
    end
        
    -- this is the 'work-around' to please the linter, using the underscore (`_`) symbol
    function lib._makesqldate(_,posix)
        return inmation.gettime(posix):sub(1,19)
    end

#### 8.1. Functions calls if `self` is not used in the function

    -- if self is NOT USED in the function
    function lib.selfNotUsed(_,arg1)
        return "function received arg : " .. arg1
    end

#### 8.2. Functions calls if `self` is used in the function

    -- if self is USED in the function 
    function lib:selfUsed(arg1)
        return "function called from " .. inmation.getselfpath() .. " received arg = " ..  arg1
    end
#### 8.3. Functions size
The functions have to be to the point, small and short. The maximum of lines a function can have is 20. To achieve this number the function can be separated into smaller sub-functions.

#### 8.4. Number of arguments per function
The number of arguments per function should be of 4 or less parameters.

#### 8.5. One-line functions
The one-line functions should be avoided.

    -- DON'T
    local funcion one() local x = false end

    -- DO
    local function one()
        local x = false
    end

#### 8.6. Functions return
Avoid having different place of return for functions. If needed, an early return can be used.

    -- DON'T
    local function f1(p1)
        if p1 == 1 then
            -- body 1
            return 8
        elseif p1 == 2 then
            -- body 2
            return 4
        else
            -- other body
            return 2
        end
    end

    -- DO
    local function f1(p1)
        if not p1 then return 8 end
        -- body 
        return 2
    end

#### 8.7. Indentation of functions' arguments
When calling a function, if ever argument is defined in a different line each, then these arguments should be aligned based on the position of the first argument.

    lib:funct(par1,
            par2,
            par3)

### 9. Tables style

#### 9.1. Tables assignment when broken in multiple lines
When the table has a lot of assignments, the table is broken into multiple lines.

#### 9.2. Keys alignments when table in multiple lines
Align the table keys when the table is broken into multiple lines.

#### 9.3. Usage of commas
Use commas as the principal separator when assigning values to the keys of a table.
Prefer to use a comma after the last item is defined.

    -- DON'T
    table = {key1=val1, key2=val2, key3=val3, key4=val4}

    -- DO
    table = {
    key1 = val1,
    key2 = val2,
    key3 = val3,
    key4 = val4,
    }

#### 9.4. Dictionary constructors
Prefer using the simpler version of tables constructors and its keys and values definition 

    table = {
    key1 = val1,
    key2 = val2,
    }

than using another longer and overdone version such as 
    
    table = {
        ["key1"] = val1,
        ["key2"] = val2
    }

### 10. Other style rules
#### 10.1. Checking if a variable is void
When checking if a variable is void (nil, without content), it is preferred to use only the variable name, not to use nil.

    -- NOT PREFERRED
    if var ~= nil then
    end

    -- DO
    if var then
    end

#### 10.2. Ternary operators-like assignments
When possible, use ternary operator-like assignment instead of the longer standard structure if-then-else.

    -- DON'T
    if not a then
    a = 3

    -- DO
    a = a or 3

#### 10.3. Avoid more than 3 levels of nesting