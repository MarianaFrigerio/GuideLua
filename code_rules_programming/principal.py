from luaparser import ast
from luaparser import astnodes
import re
import enchant


class StyleLua:
    readFile = open(r"C:\Users\maryf\Desktop\LuaFiles\ex.lua", "r")
    saveFile = readFile.read()
    lineasFile = saveFile.splitlines()
    #lineasN = readFile.readlines()
    #print(lineasN)
    readFile.close()
    #  print(saveFile)
    # print(lineasFile)

    def parseLua(self):
        tree = ast.parse(self.saveFile)
        return ast.to_pretty_str(tree)

    def layout_operators_IfEquals(self, ast_tree):
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

    def layout_max_line_length(self):
        lineas = self.lineasFile
        for linea in range(len(lineas)):
            if(len(lineas[linea])) > 120:
                print("WARNING Line " + str(linea + 1) + ": line length larger than 120 characters")

    def styleLocalVariableName(self, ast_tree):
        op = "LocalAssign: {}"
        # print(ast_tree)
        matches_op = re.finditer(op, ast_tree)
        matches_positions_op = [match.start() for match in matches_op]  # lista de primera posicion de match del char
        # print(matches_positions_op)

        splitat = matches_positions_op[0]  # posicion del primer char de donde se encontro lo buscado
        cutTree = ast_tree[splitat:]  # solo se queda con el tree desde lo encontrado

        id_busqueda = "id: '"
        matches_id = re.finditer(id_busqueda, cutTree)
        matches_positions_id = [match.start() for match in matches_id]
        # print(matches_positions_id)

        # print(re.search(id_busqueda, cutTree).end())
        splitat = re.search(id_busqueda, cutTree).end()  # posicion del primer char de donde se encontro lo buscado
        cutTree = cutTree[splitat:]  # solo se queda con el tree desde lo encontrado
        variableName = ""

        for charId in range(len(cutTree)):

            if cutTree[charId] is "'":
                break
            variableName = variableName + cutTree[charId]

        lineas = self.lineasFile

        substring = "local " + variableName + " "
        for linea in range(len(lineas)):
            matches = re.finditer(substring, lineas[linea])  # viendo en cada linea si existe el simbolo
            matches_positions = [match.start() for match in matches]  # lista de primera posicion de match del char

            if matches_positions:
                for char_index in range(len(lineas[linea])):
                    if char_index == matches_positions[0]:
                        if 64 < ord(lineas[linea][char_index + 6]) < 91:
                            print("WARNING Line " + str(linea + 1) + ": Name of variable not compliant with the "
                                                                     "coding conventions")

    # TODO: AGREGAR QUE SE PUEDA HACER BUSQUEDA A TODAS LAS VARIABLES (AHORA MISMO SOLO BUSCA SEGUN LA PRIMERA
    # TODO: VARIABLE ENCONTRADA) AGREGAR BUCLE EN MATCHES_POSITIONS_OP
    # TODO: HACER COMO EN tables_commas !!

    def formatting_indentation(self):
        lineas = self.lineasFile
        len_lineas = range(len(lineas))
        count_spaces = 0
        for linea in len_lineas:
            len_linea = range(len(lineas[linea]))
            for char_index in len_linea:
                if lineas[linea][char_index] is not " ":
                    break
                if lineas[linea][char_index] is " ":
                    count_spaces = count_spaces + 1
            if count_spaces % 4 is not 0:
                print("WARNING Line " + str(linea + 1) + ": Indentation is not a multiple of 4")
            count_spaces = 0

    def naming_bad_characters(self):
        lineas = self.lineasFile
        len_lineas = range(len(lineas))
        count_warns = 0

        for linea in len_lineas:
            len_linea = range(len(lineas[linea]))
            for char_index in len_linea:
                if ord(lineas[linea][char_index]) > 127:      # 0 > ord(lineas[linea][char_index]
                    if count_warns is not 1:
                        print("WARNING Line " + str(linea + 1) + ": There are non accepted characters (outside "
                                                                 "[0,127] in the ASCII table) on this line")
                    count_warns = 1
            count_warns = 0

    def formatting_tab(self):
        substring1 = r"\t"
        string = "\t"
        substring2 = "\t"
        string_tab = repr(substring1)
        # print(string_tab)
        for linea in range(len(self.lineasFile)):
            # print(self.lineasFile[linea])
            matches_id = re.finditer(string_tab, self.lineasFile[linea])
            matches_positions_ss = [match.start() for match in matches_id]
            # print(matches_positions_ss)
            for char_index in range(len(self.lineasFile[linea])):
                if matches_positions_ss:
                    for match_pos in range(len(matches_positions_ss)):
                        if char_index == matches_positions_ss[match_pos]:
                            print("WARNING Line " + str(
                                linea + 1) + ": Prsence of a TAB character. For code indentation, please use 4 spaces")

    def comments_english(self):
        lineas = self.lineasFile
        d = enchant.Dict("en_US")
        word_checked = ""
        # if d.check(node.id) is False:
        # print(node.id + " is not English compliant.")

        len_lineas = range(len(lineas))
        count_warns = 0
        saved_index = 0
        words_save = ""
        isComment = False
        is_upper = False
        word_camel = ""
        word_pre_camel = ""

        for linea in len_lineas:
            len_linea = range(len(lineas[linea]))
            for char_index in len_linea:
                if lineas[linea][char_index - 1] is "-" and lineas[linea][char_index - 2] is "-":
                    isComment = True
                    saved_index = char_index

                if isComment:
                    if not(64 < ord(lineas[linea][char_index]) < 91) and not(96 < ord(lineas[linea][char_index]) < 123):
                        words_save = words_save + " "
                    if 64 < ord(lineas[linea][char_index]) < 91 or 96 < ord(lineas[linea][char_index]) < 123:
                        words_save = words_save + lineas[linea][char_index]
            isComment = False
            if words_save:
                splitted_words = words_save.split()
                for word in splitted_words:
                    if d.check(word) is False:
                        count_warns = 1
                        for char_word in range(len(word)):
                            if word[char_word].isupper() and char_word == 0:
                                word_pre_camel = word_pre_camel + word[char_word]
                            else:
                                if word[char_word].isupper():
                                    is_upper = True
                                if is_upper:
                                    word_camel = word_camel + word[char_word]
                                else:
                                    word_pre_camel = word_pre_camel + word[char_word]
                        if word_camel and word_pre_camel:
                            if d.check(word_camel) is True and d.check(word_pre_camel):
                                count_warns = 0
                        word_pre_camel = ""
                        word_camel = ""
                        if count_warns > 0:
                            print("WARNING Line " + str(linea + 1) + ": Comment that is not English compliant")
            words_save = ""
            count_warns = 0

    def functions_funct_size(self):
        count_warns = 0
        file_internal = self.saveFile
        tree = ast.parse(file_internal)
        aux = ast.to_pretty_str(tree)
        char_start_locF = 0
        char_end_locF = 0
        char_count = 0
        total_chars = 0
        local_funct_name = ""
        linea_beggining = 0
        linea_end = 0
        total_lines = 0
        warning = False
        for node in ast.walk(tree):
            if isinstance(node, astnodes.LocalFunction) or isinstance(node, astnodes.Function):
                char_start_locF = node.start_char
                char_end_locF = node.stop_char
                local_funct_name = node.name.id
                total_chars = char_end_locF - char_start_locF
                for linea in range(len(self.lineasFile)):
                    for char_index in range(len(self.lineasFile[linea])):
                        if char_count == char_start_locF:
                            linea_beggining = linea + 1
                        if char_count == char_end_locF:
                            warning = True
                            linea_end = linea + 1
                            break
                        char_count += 1
                    char_count += 1  # agregando el caracter de newline (\n)
                    if warning:
                        total_lines = linea_end - linea_beggining
                        if total_lines > 20:
                            print("WARNING Line " + str(linea_beggining) + ": Function named " + local_funct_name +
                                  " exceeds the  maximum of 20 code lines per function")
                        break
            char_count = 0
            warning = False

    def tables_commas(self):
        file_internal = self.saveFile
        tree = ast.parse(file_internal)
        aux = ast.to_pretty_str(tree)
        last_key = ""
        last_value = ""
        for node in ast.walk(tree):
            if isinstance(node, astnodes.LocalAssign):
                if isinstance(node.values[0], astnodes.Table):
                    for field in range(len(node.values[0].fields)):
                        if field == len(node.values[0].fields) - 1:
                            last_key = node.values[0].fields[field].key.id
                            last_value = node.values[0].fields[field].value.id

                    id_busqueda = last_key + " = " + last_value
                    for linea in range(len(self.lineasFile)):
                        matches_id = re.finditer(id_busqueda, self.lineasFile[linea])
                        matches_positions_id = [match.start() for match in matches_id]
                        for char_index in range(len(self.lineasFile[linea])):
                            if matches_positions_id:
                                for match_pos in range(len(matches_positions_id)):
                                    if char_index == matches_positions_id[match_pos]:
                                        if (char_index + len(id_busqueda)) >= len(self.lineasFile[linea]):
                                            print("WARNING Line " + str(
                                                linea + 1) + ": A comma after the last item of table assignation is not"
                                                             " used.")
                                        elif self.lineasFile[linea][char_index + len(id_busqueda)] is not ",":
                                            print("WARNING Line " + str(
                                                linea + 1) + ": A comma after the last item of table assignation is not"
                                                             " used.")

    def other_nil(self):
        substring = "nil"
        for linea in range(len(self.lineasFile)):
            matches_id = re.finditer(substring, self.lineasFile[linea])
            matches_positions_ss = [match.start() for match in matches_id]
            for char_index in range(len(self.lineasFile[linea])):
                if matches_positions_ss:
                    for match_pos in range(len(matches_positions_ss)):
                        if char_index == matches_positions_ss[match_pos]:
                            print("WARNING Line " + str(
                                linea + 1) + ": Usage of nil. Preferably, use only the variable name to denote "
                                             "non-value")


def main():
    styleL = StyleLua()
    parsed = styleL.parseLua()
    styleL.layout_operators_IfEquals(parsed)
    styleL.layout_max_line_length()
    styleL.styleLocalVariableName(parsed)
    styleL.formatting_indentation()
    styleL.naming_bad_characters()
    styleL.formatting_tab()
    styleL.comments_english()
    styleL.functions_funct_size()
    styleL.tables_commas()
    styleL.other_nil()


if __name__ == '__main__':
    main()
