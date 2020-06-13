from luaparser import ast
from luaparser import astnodes
import enchant
d = enchant.Dict("en_US")
d.check("Hello")
d.check("Helo")
import re

if __name__ == '__main__':
    d = enchant.Dict("en_US")
    src1 = """local function sayHello()
                    print('hello world !')
                    local x = 3 + 5
                    
                    x2 = 43
                    if( a==20 ) -- inline comment
                    then
                        print('Hi!')
                    end
                    if( c==25 )
                    then
                        print('Hi!')
                    end
                end
                sayHello()
                lib:sayHi(hey)"""



    print(type(src1))

    tree = ast.parse(src1)
    aux = ast.to_pretty_str(tree)
    print(aux)

    # print(d.check("Hello"))
    # print(d.check("Helo"))
    for node in ast.walk(tree):
        if isinstance(node, astnodes.String):
            print("STRINGS")
            if d.check(node.s) is False:
                print(node.s + " is not English compliant.")
            print("!!!!")
        if isinstance(node, astnodes.Name):

            # print(node.id)
            # print(d.check(node.id))
            if d.check(node.id) is False:
                print(node.id + " is not English compliant.")

        if isinstance(node, astnodes.Call):
            print("CALLS")
            if node.comments:
                # print(node.comments)
                for item in range(len(node.comments)):
                    print(str(node.comments[item]))
                #if d.check(node.comments) is False:
                    # print(node.comments)
            print("!!!!")
        # if isinstance(node, astnodes.LocalAssign):
            # si el stop_char es 182 significa que en total son 183 chars ese bloque
            #print(node)
            #print(node.display_name)
            #print(str(node.targets))
            #print(node.values)
        # if isinstance(node, astnodes.Name):
            # print(node.id)
            # print(node.to_json())
            # print(node.stop_char)

