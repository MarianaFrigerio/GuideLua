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

    # Check if the TAB character is being used in the source code
    def formatting_tab(self):
        tab = b'\t'
        line_number = 0

        with open(r"C:\Users\maryf\Desktop\LuaFiles\ex.lua", 'rb') as file_binary:
            for line in file_binary:
                line_number += 1
                if line.find(tab) != -1:
                    print("WARNING Line " + str(line_number) + ": Presence of a TAB character. For code indentation,"
                                                               " please use 4 spaces")

    # Checking if there are trailing spaces
    def formatting_trailing_spaces(self):
        end_line = b'\n'
        line_number = 0

        with open(r"C:\Users\maryf\Desktop\LuaFiles\ex.lua", 'rb') as file_binary:
            for line in file_binary:
                line_number += 1
                index_found = line.find(end_line)
                if index_found != -1:
                    for char in range(len(line)):
                        if line[index_found - 2] == 32 or line[index_found - 2] == 11:  # equals to SPACE or TAB
                            print("WARNING Line " + str(
                                line_number) + ": Presence of trailing spaces.")
                        break
                else:
                    for char in range(len(line)):
                        if line[len(line) - 1] == 32 or line[index_found - 2] == 11: # equals to SPACE or TAB
                            print("WARNING Line " + str(
                                line_number) + ": Presence of trailing spaces.")
                        break

    # Checking if the maximum of lines length is exceeded
    def formatting_max_line_length(self):
        lineas = self.lineasFile
        for linea in range(len(lineas)):
            if(len(lineas[linea])) > 120:
                print("WARNING Line " + str(linea + 1) + ": line length larger than 120 characters")

    # Notation of local variables: Lower Camel Case
    def naming_local_variable(self):
        file_internal = self.saveFile
        tree = ast.parse(file_internal)
        lineas_file = self.lineasFile
        warning = False
        search_file = ""

        for node in ast.walk(tree):
            if isinstance(node, astnodes.LocalAssign):
                if node.targets[0].id.islower() or node.targets[0].id.isupper():
                    # if all the letters are uppercase or lowercase
                    warning = True
                else:
                    if len(node.targets[0].id) == 1 and node.targets[0].id[0].isupper():
                        # when the only letter is uppercase
                        warning = True
                    else: # con más de una letra
                        if node.targets[0].id[0].isupper():
                            # when the first letter is uppercase
                            warning = True
                        if len(node.targets[0].id) > 1:
                            if node.targets[0].id[1].islower():
                                # when the second letter is lowercase
                                warning = True
                        for char in range(len(node.targets[0].id)):
                            if len(node.targets[0].id) > 2:
                                if node.targets[0].id[char].isupper():
                                    if char is not 0:
                                        if not node.targets[0].id[char - 1].islower():
                                            # when the previous letter of an uppercase is not a lowercase
                                            warning = True
                                    if len(node.targets[0].id) > char + 1:
                                        if not node.targets[0].id[char + 1].islower():
                                            # when the next letter of a uppercase is not a lowercase
                                            warning = True
                if warning:
                    search_file = "local " + node.targets[0].id + " "
                    for linea in range(len(lineas_file)):
                        matches = re.finditer(search_file, lineas_file[linea])  # viendo en cada linea si existe
                        matches_positions = [match.start() for match in matches]  # lista de primera posicion de
                                                                                  # match del char
                        if matches_positions:
                            for match in matches_positions:
                                for char_index in range(len(lineas_file[linea])):
                                    if char_index == match:
                                        print("WARNING Line " + str(linea + 1) + ": Name of local variable not "
                                                                                 "compliant with the coding conventions"
                                                                                 " - Lower Camel Case")
                warning = False

    # Notation of local variables: Upper Camel Case
    def naming_global_variable(self):
        file_internal = self.saveFile
        tree = ast.parse(file_internal)
        lineas_file = self.lineasFile
        warning = False
        search_file = ""

        for node in ast.walk(tree):
            if isinstance(node, astnodes.Assign) and not isinstance(node, astnodes.LocalAssign):
                if node.targets[0].id.islower() or node.targets[0].id.isupper():
                    # if all the letters are uppercase or lowercase
                    warning = True
                else:
                    if len(node.targets[0].id) == 1 and node.targets[0].id[0].islower():
                        # when the only letter is lowercase
                        warning = True
                    else:  # con más de una letra
                        if node.targets[0].id[0].islower():
                            # when the first letter is lowercase
                            warning = True
                        if len(node.targets[0].id) > 1:
                            if node.targets[0].id[1].isupper():
                                # when the second letter is uppercase
                                warning = True
                        for char in range(len(node.targets[0].id)):
                            if len(node.targets[0].id) > 2:
                                if node.targets[0].id[char].isupper():
                                    # print(char)
                                    if char is not 0:
                                        if not node.targets[0].id[char - 1].islower():
                                            # when the previous letter of an uppercase is not a lowercase
                                            warning = True
                                    if len(node.targets[0].id) > char + 1:
                                        if not node.targets[0].id[char + 1].islower():
                                            # when the next letter of a uppercase is not a lowercase
                                            warning = True
                if warning:
                    search_file = node.targets[0].id + " ="
                    for linea in range(len(lineas_file)):
                        matches = re.finditer(search_file, lineas_file[linea])  # viendo en cada linea si existe
                        matches_positions = [match.start() for match in matches]  # lista de primera posicion de
                        # match del char
                        if matches_positions:
                            for match in matches_positions:
                                for char_index in range(len(lineas_file[linea])):
                                    if char_index == match:
                                        print("WARNING Line " + str(linea + 1) + ": Name of global variable not "
                                                                                 "compliant with the coding conventions"
                                                                                 " - Upper Camel Case")
                warning = False

    # Notation of local functions: _lowerCamelCase
    def naming_local_function(self):
        file_internal = self.saveFile
        tree = ast.parse(file_internal)
        lineas_file = self.lineasFile
        warning = False
        search_file = ""

        for node in ast.walk(tree):
            if isinstance(node, astnodes.LocalFunction):
                if node.name.id.islower() or node.name.id.isupper():
                    # if all the letters are uppercase or lowercase
                    warning = True
                else:
                    if len(node.name.id) == 1:
                        warning = True
                    if len(node.name.id) == 2 and (node.name.id[0] is not "_" or node.name.id[1].isupper):
                        # when there are only two letters
                        warning = True
                    else:  # con más de una letra
                        if node.name.id[0] is not "_":
                            # when the first letter is not an underscore
                            warning = True
                        if node.name.id[1].isupper():
                            # when the first letter is uppercase
                            warning = True
                        if len(node.name.id) > 2:
                            if not node.name.id[2].islower():
                                # when the second letter is lowercase
                                warning = True
                        for char in range(len(node.name.id)):
                            if len(node.name.id) > 2:
                                if node.name.id[char].isupper():
                                    if char is not 0 or char is not 1:
                                        if not node.name.id[char - 1].islower():
                                            # when the previous letter of an uppercase is not a lowercase
                                            warning = True
                                    if len(node.name.id) > char + 1:
                                        if not node.name.id[char + 1].islower():
                                            # when the next letter of a uppercase is not a lowercase
                                            warning = True
                if warning:
                    search_file = "local function " + node.name.id + "\("
                    for linea in range(len(lineas_file)):
                        matches = re.finditer(search_file, lineas_file[linea])  # viendo en cada linea si existe
                        matches_positions = [match.start() for match in matches]  # lista de primera posicion de
                        # match del char
                        if matches_positions:
                            for match in matches_positions:
                                for char_index in range(len(lineas_file[linea])):
                                    if char_index == match:
                                        print("WARNING Line " + str(linea + 1) + ": Name of local function not "
                                                                                 "compliant with the coding conventions"
                                                                                 " - _lowerCamelCase")
                warning = False

    # Notation of local functions: Upper Camel Case
    def naming_global_function(self):
        file_internal = self.saveFile
        tree = ast.parse(file_internal)
        lineas_file = self.lineasFile
        warning = False
        search_file = ""

        for node in ast.walk(tree):
            if isinstance(node, astnodes.Function) and not isinstance(node, astnodes.LocalFunction):
                if node.name.id.islower() or node.name.id.isupper():
                    # if all the letters are uppercase or lowercase
                    warning = True
                else:
                    if len(node.name.id) == 1 and node.name.id[0].islower():
                        # when the only letter is lowercase
                        warning = True
                    else:  # con más de una letra
                        if node.name.id[0].islower():
                            # when the first letter is lowercase
                            warning = True
                        if len(node.name.id) > 1:
                            if node.name.id[1].isupper():
                                # when the second letter is uppercase
                                warning = True
                        for char in range(len(node.name.id)):
                            if len(node.name.id) > 2:
                                if node.name.id[char].isupper():
                                    # print(char)
                                    if char is not 0:
                                        if not node.name.id[char - 1].islower():
                                            # when the previous letter of an uppercase is not a lowercase
                                            warning = True
                                    if len(node.name.id) > char + 1:
                                        if not node.name.id[char + 1].islower():
                                            # when the next letter of a uppercase is not a lowercase
                                            warning = True
                if warning:
                    search_file = "function " + node.name.id + "\("
                    for linea in range(len(lineas_file)):
                        matches = re.finditer(search_file, lineas_file[linea])  # viendo en cada linea si existe
                        matches_positions = [match.start() for match in matches]  # lista de primera posicion de
                        # match del char
                        if matches_positions:
                            for match in matches_positions:
                                for char_index in range(len(lineas_file[linea])):
                                    if char_index == match:
                                        print("WARNING Line " + str(linea + 1) + ": Name of global function not "
                                                                                 "compliant with the coding conventions"
                                                                                 " - Upper Camel Case")
                warning = False

        aux = ast.to_pretty_str(tree)
        # print(aux)

    # Notation of arguments of functions: Lower Camel Case
    def naming_argument(self):
        file_internal = self.saveFile
        tree = ast.parse(file_internal)
        lineas_file = self.lineasFile
        warning = False
        search_function = ""
        search_arg1 = ""
        search_arg2 = ""

        for node in ast.walk(tree):
            if isinstance(node, astnodes.LocalFunction):
                # print(len(node.args))
                if node.args:
                    # print(len(node.args))
                    for arg in range(len(node.args)):
                        # print(arg)
                        # print(node.args[arg].id)
                        # print(node.name.id)

                        if node.args[arg].id.islower() or node.args[arg].id.isupper():
                            # if all the letters are uppercase or lowercase
                            warning = True
                        else:
                            if len(node.args[arg].id) == 1 and node.node.args[arg].id.isupper():
                                # when the only letter is uppercase
                                warning = True
                            else:  # con más de una letra
                                if node.args[arg].id.isupper():
                                    # when the first letter is uppercase
                                    warning = True
                                if len(node.args[arg].id) > 1:
                                    if node.args[arg].id.islower():
                                        # when the second letter is lowercase
                                        warning = True
                                for char in range(len(node.args[arg].id)):
                                    if len(node.args[arg].id) > 2:
                                        if node.args[arg].id[char].isupper():
                                            if char is not 0:
                                                if not node.args[arg].id[char - 1].islower():
                                                    # when the previous letter of an uppercase is not a lowercase
                                                    warning = True
                                            if len(node.args[arg].id) > char + 1:
                                                if not node.args[arg].id[char + 1].islower():
                                                    # when the next letter of a uppercase is not a lowercase
                                                    warning = True
                        if warning:
                            search_function = "function " + node.name.id + "\("
                            # print(node.name.id)
                            # print(node.args[arg].id)
                            search_arg1 = node.args[arg].id + ","
                            search_arg2 = node.args[arg].id + "\)"
                            for linea in range(len(lineas_file)):
                                matches_funct = re.finditer(search_function, lineas_file[linea])  # viendo en
                                # cada linea si existe
                                matches_positions_funct = [match.start() for match in matches_funct]
                                # lista de primera posicion de match del char

                                matches_arg1 = re.finditer(search_arg1, lineas_file[linea])  # viendo en
                                # cada linea si existe
                                matches_positions_arg1 = [match.start() for match in matches_arg1]
                                # lista de primera posicion de match del char

                                matches_arg2 = re.finditer(search_arg2, lineas_file[linea])  # viendo en
                                # cada linea si existe
                                matches_positions_arg2 = [match.start() for match in matches_arg2]
                                # lista de primera posicion de match del char

                                # print(matches_positions_arg)
                                # print(matches_positions_funct)
                                if matches_positions_funct and (matches_positions_arg1 or matches_positions_arg2):
                                    # print("entré")
                                    for match in matches_positions_arg1:
                                        for char_index in range(len(lineas_file[linea])):
                                            if char_index == match:
                                                print("WARNING Line " + str(linea + 1) + ": Name of argument '" +
                                                                                        node.args[arg].id + "' not "
                                                                                         "compliant with the coding "
                                                                                         "conventions"
                                                                                         " - Lower Camel Case")

                                    for match in matches_positions_arg2:
                                        for char_index in range(len(lineas_file[linea])):
                                            if char_index == match:
                                                print("WARNING Line " + str(linea + 1) + ": Name of argument '" +
                                                                                        node.args[arg].id + "' not "
                                                                                         "compliant with the coding "
                                                                                         "conventions"
                                                                                         " - Lower Camel Case")
                        warning = False

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

    # Check if the 20 lines max function size is exceeded
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

    # Check if the total arguments of a function is exceeded
    def functions_total_arguments(self):
        count_warns = 0
        file_internal = self.saveFile
        tree = ast.parse(file_internal)
        char_start_funct = 0
        local_funct_name = ""
        total_args = 0
        total_chars_lineas = 0

        for node in ast.walk(tree):
            if isinstance(node, astnodes.LocalFunction) or isinstance(node, astnodes.Function):
                total_args = len(node.args)
                local_funct_name = node.name.id
                if total_args > 4:
                    char_start_funct = node.start_char
                    for linea in range(len(self.lineasFile)):
                        total_chars_lineas += len(self.lineasFile[linea])
                        if total_chars_lineas >= char_start_funct:
                            print("WARNING Line " + str(linea + 1) + ": Function named " + local_funct_name +
                                  " exceeds the  maximum of 4 arguments per function")
                            total_chars_lineas = 0
                            break

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
    styleL.formatting_trailing_spaces()
    styleL.formatting_max_line_length()

    styleL.naming_local_variable()
    styleL.naming_global_variable()
    styleL.naming_local_function()
    styleL.naming_global_function()
    styleL.naming_argument()
    # styleL.naming_library()
    # styleL.naming_libraries_calls()
    # styleL.naming_unneeded_variables()
    # styleL.naming_hungarian_notation()
    styleL.naming_bad_characters()

    # styleL.layout_operators(parsed)
    styleL.layout_operators_IfEquals(parsed)
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
    styleL.functions_total_arguments()
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
