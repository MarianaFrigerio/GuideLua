from luaparser import ast
from luaparser import astnodes
import enchant
d = enchant.Dict("en_US")
d.check("Hello")
d.check("Helo")
import re

if __name__ == '__main__':
    d = enchant.Dict("en_US")
    src1 = """  local function sayHello()
    print('hello world !')
    local X = 3 + 5
    local X2 = 2
    if( a == 20 )
    then
        print('Hi!') --hey come on hey,
    end
    if( c == 25 )
    -- holota
    then
        local J = 3
        print('Hi!') --HeyHi,
    end
    print('Hi!')
    print('Hi!')
    print('Hi!')
    print('Hi!')
    print('Hi!')
    print('Hi!')
    print('Hi!')
print("cant")
print("d")
end
sayHello()
lib:sayHi(hey)
NewJ = 0

local function b()
end"""

    print(type(src1))

    tree = ast.parse(src1)
    aux = ast.to_pretty_str(tree)
    print(aux)

    # print(d.check("Hello"))
    # print(d.check("Helo"))
    for node in ast.walk(tree):
        if isinstance(node, astnodes.Comment):
            print("Hey")
        if isinstance(node, astnodes.String):
            print("STRINGS")
            if d.check(node.s) is False:
                print(node.s + " is not English compliant.")
        if isinstance(node, astnodes.Name):

            # print(node.id)
            # print(d.check(node.id))
            if d.check(node.id) is False:
                print(node.id + " is not English compliant.")

        if isinstance(node, astnodes.Call):
            print("CALLS")
                # print(node.comments)
                #if d.check(node.comments) is False:
                    # print(node.comments)
        if isinstance(node, astnodes.LocalAssign):
            # si el stop_char es 182 significa que en total son 183 chars ese bloque
            #print(node)
            #print(node.display_name)
            print(str(node.targets))
            #print(node.values)
        # if isinstance(node, astnodes.Name):
            # print(node.id)
            # print(node.to_json())
            # print(node.stop_char)"""

