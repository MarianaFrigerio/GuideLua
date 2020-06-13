from luaparser import ast
from luaparser import astnodes
import re


class StyleLua:
    readFile = open(r"C:\Users\maryf\Desktop\LuaFiles\ex.lua", "r")
    saveFile = readFile.read()
    lineasFile = saveFile.splitlines()
    readFile.close()
    # print(saveFile)
    # print(lineasFile)

    def parseLua(self):
        tree = ast.parse(self.saveFile)
        return ast.to_pretty_str(tree)

    def styleIfEquals(self, ast_tree):
        op = "REqOp"
        substring = "=="
        count_warns = 0
        if op in ast_tree:
            lineas = self.lineasFile
            i = 0
            # for para iterar entre las lineas, en cada linea
            for linea in range(len(lineas)):
                matches = re.finditer(substring, lineas[linea])  # viendo en cada linea si existe el simbolo ==
                matches_positions = [match.start() for match in matches]  # lista de primera posicion de match del char
                if matches_positions:
                    for char_index in range(len(lineas[linea])):
                        i = i + 1
                        if char_index == matches_positions[0]:
                            if lineas[linea][char_index - 1] is not " ":
                                count_warns = 1
                                print("WARNING Line " + str(linea + 1) + ": missing spaces around operator")
                        if char_index == (matches_positions[0] + 1):
                            if lineas[linea][char_index + 1] is not " ":
                                if count_warns is not 1:
                                    print("WARNING Line " + str(linea + 1) + ": missing spaces around operator")

    def styleMaxLineLength(self):
        lineas = self.lineasFile
        for linea in range(len(lineas)):
            if(len(lineas[linea])) > 120:
                print("WARNING Line " + str(linea + 1) + ": line length larger than 120 characters")

    def styleLocalVariableName(self, ast_tree):
        op = "LocalAssign: {}"
        matches_op = re.finditer(op, ast_tree)
        matches_positions_op = [match.start() for match in matches_op]  # lista de primera posicion de match del char
        print(matches_positions_op)

        splitat = matches_positions_op[0]  # posicion del primer char de donde se encontro lo buscado
        cutTree = ast_tree[splitat:]  # solo se queda con el tree desde lo encontrado
        # print(cutTree)

        id_busqueda = "id: '"
        matches_id = re.finditer(id_busqueda, cutTree)
        matches_positions_id = [match.start() for match in matches_id]  #
        print(matches_positions_id)

        print(re.search(id_busqueda, cutTree).end())
        splitat = re.search(id_busqueda, cutTree).end()  # posicion del primer char de donde se encontro lo buscado
        cutTree = cutTree[splitat:]  # solo se queda con el tree desde lo encontrado
        variableName = ""

        for charId in range(len(cutTree)):

            if cutTree[charId] is "'":
                break
            variableName = variableName + cutTree[charId]

        lineas = self.lineasFile

        substring = "local " + variableName
        for linea in range(len(lineas)):
            matches = re.finditer(substring, lineas[linea])  # viendo en cada linea si existe el simbolo ==
            matches_positions = [match.start() for match in matches]  # lista de primera posicion de match del char

            if matches_positions:
                for char_index in range(len(lineas[linea])):
                    if char_index == matches_positions[0]:
                        if 64 < ord(lineas[linea][char_index + 6]) < 91:
                            print("WARNING Line " + str(linea + 1) + ": Name of variable not compliant with the "
                                                                     "coding conventions")


def main():
    styleL = StyleLua()
    parsed = styleL.parseLua()
    styleL.styleIfEquals(parsed)
    styleL.styleMaxLineLength()
    styleL.styleLocalVariableName(parsed)


if __name__ == '__main__':
    main()
