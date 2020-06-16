from luaparser import ast
from luaparser import astnodes
import re
import enchant
# from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE


class StyleLua:
    readFile = open(r"C:\Users\maryf\Desktop\LuaFiles\ex.lua", "r")
    saveFile = readFile.read()
    lineasFile = saveFile.splitlines()
    # lineasN = readFile.readlines()
    # print(lineasN)
    readFile.close()
    #  print(saveFile)
    # print(lineasFile)

    def parseLua(self):
        tree = ast.parse(self.saveFile)
        return ast.to_pretty_str(tree)

    # Usage of the UTF-8 encoding
    # def formatting_code_encoding(self):

    # Check the usage of the CRLF line break type
    def formatting_line_break(self):
        crlf = b'\r\n'
        lfcr = b'\n\r'
        lf = b'\n'
        cr = b'\r'

        end_list = [crlf, lfcr, lf, cr]
        counts = dict.fromkeys(end_list, 0)

        with open(r"C:\Users\maryf\Desktop\LuaFiles\ex.lua", 'rb') as file_binary:
            for line in file_binary:
                for ending in end_list:
                    if line.endswith(ending):
                        counts[ending] += 1
                        break
        if counts[crlf] == 0 or counts[lfcr] > 0 or counts[cr] > 0 or counts[lf] > 0:
            print("WARNING: The document is not using in its entirety CRLF line break type. Check if others (LFCR, LF"
                  " or CR) line breaks types are being used.")

    # Checking if the document is formatted with an indentation that is multiple of 4
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

    def formatting_tab(self):
        tab = b'\t'
        line_number = 0

        with open(r"C:\Users\maryf\Desktop\LuaFiles\ex.lua", 'rb') as file_binary:
            for line in file_binary:
                line_number += 1
                if line.find(tab) != -1:
                    print("WARNING Line " + str(line_number) + ": Presence of a TAB character. For code indentation,"
                                                               " please use 4 spaces")

    # def formatting_trailing_spaces(self):

    def formatting_max_line_length(self):
        lineas = self.lineasFile
        for linea in range(len(lineas)):
            if(len(lineas[linea])) > 120:
                print("WARNING Line " + str(linea + 1) + ": line length larger than 120 characters")

    # def naming_local_variable(self):
    def styleLocalVariableName(self, ast_tree):
        op = "LocalAssign: {}"
        # print(ast_tree)
        matches_op = re.finditer(op, ast_tree)
        matches_positions_op = [match.start() for match in
                                matches_op]  # lista de primera posicion de match del char
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

    # def naming_global_variable(self):

    # def naming_local_function(self):

    # def naming_global_variable(self):

    # def naming_argument(self):

    # def naming_library(self):

    # def naming_libraries_calls(self):

    # def naming_unneeded_variables(self):

    # def naming_hungarian_notation(self):

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

    # def layout_operators(self, ast_tree):

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

    # def layout_spaces_next_brackets(self):

    # def layout_space_alignment(self):

    # def layout_empty_line_between_functions(self):

    # def layout_max_successive_empty_lines(self):

    def comments_english(self):
        lineas = self.lineasFile
        d = enchant.Dict("en_US")
        word_checked = ""

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

    # def comments_space_btw_comment_mark_text(self):

    # def comments_luadoc_docstrings(self):

    # def comments_commented_code(self):

    # def keywords_todo(self):

    # def keywords_bug(self):

    # def keywords_note(self):

    # def scopes_preferred_scope(self):

    # def scopes_modules_not_global(self):

    # def scopes_local_aliases(self):

    # def strings_double_quoted(self):

    # def functions_calls_not_self(self):

    # def functions_call_self(self):

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

    # def functions_total_arguments(self):

    # def functions_one_line_functions(self):

    # def functions_return(self):

    # def functions_arguments_indentation(self):

    # def tables_broke_tables_assignments_if_many(self):

    # def tables_keys_alignments_when_multiple_lines(self):

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

    # def tables_dictionary_constructors(self):

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

    # def other_ternary(self):

    # def other_avoid_3_levels_of_nesting(self):

def main():
    styleL = StyleLua()
    parsed = styleL.parseLua()

    # styleL.formatting_code_encoding()
    styleL.formatting_line_break()
    styleL.formatting_indentation()
    styleL.formatting_tab()
    # styleL.formatting_trailing_spaces()
    styleL.formatting_max_line_length()

    # styleL.naming_local_variable()
    styleL.styleLocalVariableName(parsed)
    # styleL.naming_global_variable()
    # styleL.naming_local_function()
    # styleL.naming_global_variable()
    # styleL.naming_argument()
    # styleL.naming_library()
    # styleL.naming_libraries_calls()
    # styleL.naming_unneeded_variables()
    # styleL.naming_hungarian_notation()
    styleL.naming_bad_characters()

    # styleL.layout_operators(parsed)
    # styleL.layout_operators_IfEquals(parsed)
    # styleL.layout_spaces_next_brackets()
    # styleL.layout_space_alignment()
    # styleL.layout_empty_line_between_functions()
    # styleL.layout_max_successive_empty_lines()

    styleL.comments_english()
    # styleL.comments_space_btw_comment_mark_text()
    # styleL.comments_luadoc_docstrings()
    # styleL.comments_commented_code()

    # styleL.keywords_todo()
    # styleL.keywords_bug()
    # styleL.keywords_note()

    # styleL.scopes_preferred_scope()
    # styleL.scopes_modules_not_global()
    # styleL.scopes_local_aliases()

    # styleL.strings_double_quoted()

    # styleL.functions_calls_not_self()
    # styleL.functions_call_self()
    styleL.functions_funct_size()
    # styleL.functions_total_arguments()
    # styleL.functions_one_line_functions()
    # styleL.functions_return()
    # styleL.functions_arguments_indentation()

    # styleL.tables_broke_tables_assignments_if_many()
    # styleL.tables_keys_alignments_when_multiple_lines()
    styleL.tables_commas()
    # styleL.tables_dictionary_constructors()

    styleL.other_nil()
    # styleL.other_ternary()
    # styleL.other_avoid_3_levels_of_nesting()


if __name__ == '__main__':
    main()
