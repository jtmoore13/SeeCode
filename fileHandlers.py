
from allPurpose import *
from infoClass import Info

INDENT = "    "


# adds the necessary code to support animations
def add_starter_code():
    with open("starterCode.txt", "r") as f:
        with open("translated.py", "w") as trans:
            for line in f:
                trans.write(line)
    f.close()
    trans.close()


# adds the necessary code at the bottom of the main function
def add_ending_code():
    with open("endCode.txt", "r") as f:
        with open("translated.py", "a") as trans:
            for line in f:
                trans.write(line)
    f.close()
    trans.close()


# adds the translated user's code to the main function to be executed
def add_user_code(output, original_input):
    displayed_lines = get_lines_to_display(original_input)
    with open("translated.py", "a") as trans:
        trans.write('\n\n')
        trans.write(INDENT + "lines_1999 = " + str(displayed_lines) + '\n')
        trans.write(INDENT + "show_lines(canvas, lines_1999)\n")
        trans.write(INDENT + "if check_for_else_syntax_error(lines_1999) != -1:\n")
        trans.write(INDENT*2 + "display_lines(canvas, check_for_else_syntax_error(lines_1999), 'red')\n")
        trans.write(INDENT*2 + "throw_error(canvas, 'SyntaxError: There must be code inside an else/elif statement.', "
                               "True)\n")
        trans.write(INDENT + "pause(canvas, SPEED/2)\n\n")
        trans.write(INDENT + "try:\n")
        trans.write(INDENT*2 + "pass\n")
        for line in output:
            if line != '\n':
                trans.write(INDENT*2 + line)
                if '\n' not in line:
                    trans.write('\n')
    trans.close()


# gets rid of the comments and blank lines because we don't need to show those
def get_lines_to_display(output):
    copy = output
    to_show = []
    for i in range(len(copy)):
        line = copy[i]
        if not is_comment(line) and not is_blank_line(line):
            to_show.append(line)
    return to_show


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# translates the code into animation-friendly language
def translate_file(lines):
    translate_vars_loops(lines)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# translates variables into usable variables, like: num --> num.val
def translate_untranslated_vars(lines):
    for i in range(len(lines)):
        if not is_comment(lines[i]):
            check_for_untranslated_vars(lines, i)


# words[0] or words[0][1] - returns 0
def get_first_index(name):
    return name[name.find("[")+1:name.find("]")]


# words[0][1] - returns 1
def get_second_index(name):
    copy = name[name.find("]")+1:]
    return get_first_index(copy)


# translates small variable operator commands
def translate_operator(lines, i):
    original = lines[i]
    line = clip_comment(lines[i])
    found = line.find("=")
    name = line[:found - 1].strip()

    name_copy = name + "_copy"
    val = line[found + 1:].strip()
    lines.insert(i, get_indent(line) + "temp1999x = " + val)
    i += 1
    line_num = original[original.find("line num =") + 10:].strip()
    lines[i] = line[:line.find('=')+1] + " temp1999x  # line num =" + line_num

    if is_index_of_list(name):
        actual_name = name[:name.find("[")].strip()
        first_index = get_first_index(name)
        lines[i] = get_indent(line) + actual_name + "_copy._underline_index(" + str(first_index) + ", 'yellow', False)"
        lines.insert(i+1, get_indent(line) + "try:")
        lines.insert(i+2, get_indent(line) + INDENT + original[:original.find("=")+1] + " temp1999x")
        lines.insert(i+3, get_indent(line) + INDENT + actual_name + "_copy.update(" + actual_name + ")")
        lines.insert(i+4, get_indent(line) + "except Exception as e:")
        if name.count("[") == 1:
            lines.insert(i+5, get_indent(line) + INDENT + actual_name + "_copy.handle_single_index_error(" +
                         str(first_index) + ", e.__class__.__name__, e)")
            return 5
        elif name.count("[") == 2:
            second_index = get_second_index(name)
            lines.insert(i+5, get_indent(line) + INDENT + actual_name + "_copy.handle_double_index_error(" +
                         str(first_index) + ", " + str(second_index) + ", " + "e.__class__.__name__, e)")
            return 5

    if "+=" in line:
        lines.insert(i + 1, get_indent(line) + name_copy + ".plus_equals(temp1999x)")
    elif "-=" in line:
        lines.insert(i + 1, get_indent(line) + name_copy + ".minus_equals(temp1999x)")
    elif "*=" in line:
        lines.insert(i + 1, get_indent(line) + name_copy + ".multiply_by(temp1999x)")
    elif "/=" in line and "//=" not in line:
        lines.insert(i+1, get_indent(line) + name_copy + ".divide_by_float(temp1999x)")
    elif '//=' in line:
        name = line[:found-2].strip()
        lines.insert(i+1, get_indent(line) + name_copy + ".divide_by_int(temp1999x)")
    else:
        print("missed something in fileHandlers.translate_operator()")

    return 1


# returns true if the variable being defined is redefining an existing variable
def is_redeclaration(lines, i):
    line = lines[i]
    found = line.find("=")
    name = line[:found].strip()
    return name in Info.small_vars or name in Info.big_vars


# translates a variable declaration
def translate_var(lines, i, name):
    original = lines[i]
    line = clip_comment(lines[i])
    found = line.find("=")
    name_copy = name + "_copy"
    val = line[found+1:].strip()
    line_indent = get_indent(line)
    line_num = original[original.find("line num =") + 10:].strip()

    lines.insert(i, line_indent + "temp1999x = " + val)
    i += 1
    lines[i] = line_indent + name + " = temp1999x  # line num =" + line_num

    lines.insert(i+1, line_indent + "if type(" + name + ") == list:")
    lines.insert(i+2, line_indent + INDENT + "if not is_already_a_var('" + name + "'):")
    lines.insert(i+3, line_indent + 2*INDENT + name_copy + " = List(canvas, " + "'" + name + "', temp1999x.copy())")  # was val
    lines.insert(i+4, line_indent + INDENT + "elif is_small_var('" + name + "'):")
    lines.insert(i+5, line_indent + 2*INDENT + "del " + name_copy)
    lines.insert(i+6, line_indent + 2*INDENT + name_copy + " = List(canvas, " + "'" + name + "', temp1999x.copy())") # was val
    lines.insert(i+7, line_indent + INDENT + "elif is_big_var('" + name + "'):")
    lines.insert(i+8, line_indent + 2*INDENT + name_copy + ".reset_to(" + name + ")")
    lines.insert(i+9, line_indent + "elif type(" + name + ") == int or type(" + name + ") == float or type(" + name +
                 ") == str or type(" + name + ") == bool:")
    lines.insert(i+10, line_indent + INDENT + "if not is_already_a_var('" + name + "'):")
    lines.insert(i+11, line_indent + 2*INDENT + name_copy + " = SmallVar(canvas, " + "'" + name + "', " + name + ", FLASH, False)") # was val
    lines.insert(i+12, line_indent + INDENT + "elif is_big_var('" + name + "'):")
    lines.insert(i+13, line_indent + 2*INDENT + "del " + name_copy)
    lines.insert(i+14, line_indent + 2*INDENT + name_copy + " = SmallVar(canvas, " + "'" + name + "', " + name + ", FLASH, False)") # was val
    lines.insert(i+15, line_indent + INDENT + "elif is_small_var('" + name + "'):")
    lines.insert(i+16, line_indent + 2*INDENT + name_copy + ".reset_to(" + name + ")")
    lines.insert(i+17, line_indent + "elif 'NoneType' in str(type(" + name + ")):")
    lines.insert(i+18, line_indent + INDENT + "not_supported(canvas, 'The right side of your expression does not "
                                              "return anything! Therefore, the variable \"" + name
                 + "\" cannot be set to anything.')")
    lines.insert(i+19, line_indent + "else:")
    lines.insert(i+20, line_indent + INDENT + "not_supported(canvas, 'Sorry, we only support animations for"
                                              " variables of type: int, float, str, bool, list!')")
    if is_list_method(line):
        name = line[line.find("=")+1:line.find(".")].strip()
        lines.insert(i+21, line_indent + name + "_copy.update(" + name + ")")
        return 22
    else:
        return 21


def is_else_in_sequence(lines, i, parent_indent):
    j = i+1
    while True:
        if j >= len(lines):
            return False
        line = lines[j]
        if should_skip(line):
            j += 1
            continue
        if get_num_indents(line) <= parent_indent and not (is_elif_statement(line) or is_else_statement(line)):
            return False
        elif get_num_indents(line) <= parent_indent and is_else_statement(line):
            return True
        j += 1


def add_fake_else(lines, i, parent_indent):
    j = i+1
    while True:
        if j >= len(lines):
            break
        line = lines[j]
        if should_skip(line) and not is_delete_statement(line):
            j += 1
            continue
        elif get_num_indents(line) <= parent_indent and not is_elif_statement(line):
            break
        else:
            j += 1
    lines.insert(j, parent_indent*INDENT + "else:  # fake else")


def display_elif_at_next_else(lines, i, displayed_i):
    j = i+1
    parent_indent = get_num_indents(lines[i])

    while j < len(lines) and ("display_lines(" in lines[j] or "fake else" in lines[j]):
        j += 1
    lines.insert(j, parent_indent * INDENT + INDENT + "display_lines(canvas, " + str(displayed_i) +
                 ", 'pale green')")
    lines.insert(j, parent_indent * INDENT + INDENT + "display_lines(canvas, " + str(displayed_i) +
                 ", HIGHLIGHT)")
    while True:
        if j >= len(lines):
            break
        if should_skip(lines[j]):
            j += 1
            continue
        if get_num_indents(lines[j]) == parent_indent and not is_else_statement(lines[j]) and\
                not is_elif_statement(lines[j]):
            # if there isn't a final 'else' statement (ends on elif)
            if is_elif_statement(lines[i]) and not is_else_in_sequence(lines, i, parent_indent):
                while j < len(lines) and "display_lines(" in lines[j] or "fake else" in lines[j]:
                    j += 1
                lines.insert(j, parent_indent * INDENT + "display_lines(canvas, " + str(displayed_i) +
                             ", HIGHLIGHT)")
            break
        if get_num_indents(lines[j]) < parent_indent and not is_blank_line(lines[j]) and not is_comment(lines[j]):
            break

        if get_num_indents(lines[j]) == parent_indent and (is_else_statement(lines[j]) or is_elif_statement(lines[j])):
            j += 1
            while j < len(lines) and "display_lines(" in lines[j]:
                j += 1
            lines.insert(j, parent_indent*INDENT + INDENT + "display_lines(canvas, " + str(displayed_i) +
                         ", HIGHLIGHT)")
        j += 1


# translates variable declarations
def translate_vars_loops(lines):
    i = 0
    insert_loop_here = 0
    parent_indent = 0
    nested_count = 0
    already_deleted = []
    displayed_line_index = 0

    while i < len(lines):
        if "fake else" not in lines[i] and "line num = " not in lines[i]:
            lines[i] = clip_comment(lines[i])
        line = lines[i]
        # don't need to do anything to these lines - delete statement previously added by hand (not written by user)
        if should_skip(line) or "fake else" in line:
            i += 1
            continue

        lines[i] = lines[i].rstrip() + "  # line num =" + str(displayed_line_index) + '\n'
        if not is_blank_line(line.strip()) and not (is_elif_statement(line) or is_else_statement(line)):
            lines.insert(i, get_indent(line) + "display_lines(canvas, " + str(displayed_line_index) + ", HIGHLIGHT)")
            displayed_line_index += 1
            i += 1
        elif is_elif_statement(line) or is_else_statement(line):
            if is_elif_statement(line) and not is_else_in_sequence(lines, i, get_num_indents(line)):
                add_fake_else(lines, i, get_num_indents(line))

            display_elif_at_next_else(lines, i, displayed_line_index)
            displayed_line_index += 1

        if is_var_declaration(line) and not operators_present(line):
            name = line[:line.find("=")].strip()
            i += translate_var(lines, i, name)
            # if its under the current for loop
            if get_num_indents(line) > parent_indent and name not in Info.var_names:
                j = i+1
                # finds where to delete a variable that was declared inside of the loop
                while j < len(lines) and (get_num_indents(lines[j]) >= get_num_indents(line) or is_blank_line(lines[j])
                                          or starts_with_comment(lines[j])):
                    j += 1
                name = line[:line.find('=')].strip()
                if name not in already_deleted:
                    lines.insert(j, get_num_indents(line)*INDENT + "del " + name + "_copy")
                already_deleted.append(name)
            Info.var_names.append(name)

            # will have to do += 4 or something to deal with the exception handling
        elif operators_present(line) or is_index_redefinition(line):
            i += translate_operator(lines, i)
        elif is_list_method(line):
            i += translate_list_method(lines, i)
        elif is_loop(line):
            Info.loop_count += 1
            # if the loop is not nested - it's a parent loop
            if get_num_indents(line) <= parent_indent or Info.loop_count == 1:
                nested_count = 0
                parent_indent = get_num_indents(line)
                insert_loop_here = i
                already_deleted = []
            else:
                nested_count += 1
                Info.nested_loop_lines.append(i)
            add_del_loop_statement(lines, i, parent_indent)
            data = get_loop_declaration(lines, i)
            declaration = INDENT*parent_indent + data[0]

            # marks the index of the list/string
            visit = data[1]
            if not is_each_loop(line):
                lines.insert(insert_loop_here + nested_count, declaration)
                i += 1
                lines.insert(i+1, get_indent(line) + INDENT + visit)
                i += 1
                if is_while_loop(line):
                    lines.insert(i + 1, get_indent(line) + INDENT + "display_lines(canvas, " +
                                 str(displayed_line_index - 1) + ", 'pale green')")
                    i += 1
            else:
                dec1 = declaration
                dec2 = data[3]
                name = data[4]
                lines.insert(insert_loop_here, parent_indent*INDENT + "if '" + name + "' in Info.small_vars or '" + name +
                             "' in Info.big_vars:")
                lines.insert(insert_loop_here+1, parent_indent*INDENT + INDENT + dec1)
                lines.insert(insert_loop_here+2, parent_indent*INDENT + "else:")
                lines.insert(insert_loop_here+3, parent_indent*INDENT + INDENT + dec2)
                i += 4
                insert_loop_here += 4
                # updates the variable being iterated over
                lines.insert(i+1, data[2])  # already indented when extracted
                i += 2
                lines.insert(i, get_indent(line) + INDENT + visit)

        # in case the for loop is inside of an if statement
        elif is_if_statement(line):
            lines.insert(i+1, get_indent(line) + INDENT + "display_lines(canvas, " + str(displayed_line_index - 1) +
                         ", 'pale green')")
            i += 1

        i += 1

    return lines


def add_finished_statement(lines, j, parent_indent):
    i = j
    while i < len(lines)-1 and (get_num_indents(lines[i]) > parent_indent or should_skip(lines[i])):
        i += 1
    lines.insert(i, parent_indent*INDENT + "l" + str(Info.loop_count) + ".finished()")


# adds the delete statement that deletes the loop after it's completed
def add_del_loop_statement(lines, j, parent_indent):
    i = j
    i += 1
    line = lines[i-1]
    if is_while_loop(line):
        add_finished_statement(lines, i, get_num_indents(lines[j]))
    while i < len(lines) and (get_num_indents(lines[i]) > parent_indent or should_skip(lines[i])):
        i += 1
    lines.insert(i, parent_indent*INDENT + "l" + str(Info.loop_count) + ".__del__()")


# returns the declaration of a loop
def get_loop_declaration(lines, i):
    line = lines[i]

    if is_range_loop(line):
        return get_range_loop_declaration(line)
    elif is_each_loop(line):
        return get_each_loop_declaration(lines, i)
    elif is_while_loop(line):
        return get_while_loop_declaration(lines, i)


# extracts the important variable info from the for loop
def get_range_loop_vitals(line):
    var = line[line.find(" for ")+5:line.find(" in ")]
    line = line.rstrip()
    lines = line.split(",")

    if len(lines) == 1:
        start = 0
        step = 1
        open_p = 1
        closed = 0
        i = 0
        parse = line[line.find("range(")+6:]
        while i < len(parse):
            if open_p == closed and open_p > 0:
                break
            if parse[i] == "(":
                open_p += 1
            elif parse[i] == ")":
                closed += 1
            i += 1
        stop = parse[:i-1].strip()

    elif len(lines) == 2:
        start = line[line.find("range(") + 6: line.find(",")].strip()
        stop = lines[1].strip(" ):")
        step = 1
    else:
        start = line[line.find("range(") + 6: line.find(",")].strip()
        stop = lines[1].strip()
        step = lines[2].strip(" ):")
    return var, start, stop, step


# returns the declaration of a range loop
def get_range_loop_declaration(line):
    data = get_range_loop_vitals(line)
    var = data[0]
    start = data[1]
    stop = data[2]
    step = data[3]
    declaration = "l" + str(Info.loop_count) + " = ForLoopRange(canvas, " + "'" + var + "', " + str(start) + ", " + \
                  str(stop) + ", " + str(step) + ", " + "'" + clip_comment(line.strip()) + "'" + ")"
    visit = "l" + str(Info.loop_count) + ".visit_index(" + var + ")"
    return declaration, visit


# returns the declaration of a for-each loop
def get_each_loop_declaration(lines, i):
    line = clip_comment(lines[i].rstrip())
    var = line[line.find(" for ") + 5:line.find(" in ")].strip()
    col = line.find(":")
    iteration = line[line.find(" in ") + 4:col].strip()
    fid = "l" + str(Info.loop_count)
    indent = get_indent(lines[i])
    saved = iteration
    reverse = False

    if "reversed(" in saved:
        iteration = iteration.strip("reversed(")[:-1]
        reverse = True
        saved = iteration

    declaration1 = fid + " = ForEachLoop(canvas, '" + var + "', " + "'" + saved + "', " + iteration + ", " + \
                  str(reverse) + ", '" + line.strip() + "')"
    declaration2 = fid + " = ForEachLoop(canvas, '" + var + "', " + "'" + saved + "', ' ', " + \
                  str(reverse) + ", '" + line.strip() + "')"
    visit = fid + ".visit_next()"
    update = indent + INDENT + fid + ".update(" + saved + ")"
    return declaration1, visit, update, declaration2, iteration


# returns the declaration of a while loop
def get_while_loop_declaration(lines, i):
    line = clip_comment(lines[i].rstrip())
    condition = line.strip()
    declaration = "l" + str(Info.loop_count) + " = WhileLoop(canvas, '" + condition + "')"
    visit = "l" + str(Info.loop_count) + ".mark()"
    return declaration, visit


# returns true if there is some sort of variable in the token
def var_in_token(token):
    for var in Info.small_vars:
        if var in token:
            return var
    for var in Info.big_vars:
        if var in token:
            return var
    return ""


# returns true if the token should be translated
def is_legit(token, var):
    found = token.find(var)
    if "." in token:
        return False
    elif found == 0:
        return not token[len(var)].isalpha()
    else:
        return not token[found - 1].isalpha() and (
                    found + len(var) == len(token) or not token[found + len(var)].isalpha())


# puts the translated tokens into a single line
def reconstruct_line(line, tokens):
    new_line = get_indent(line)
    for token in tokens:
        new_line += token + ' '
    return new_line.rstrip()


def check_for_untranslated_vars(lines, i):
    line = lines[i]
    if is_obj_declaration(line) or line == '\n':
        return

    tokens = line.split()
    for j in range(len(tokens)):
        token = tokens[j]
        var = var_in_token(token)
        if var != "" and var in token:
            if token == var or is_legit(token, var):
                tokens[j] = token.replace(var, var + ".val")

    lines[i] = reconstruct_line(line, tokens)


def translate_pop(line):
    return line[:line.find("pop(")+4] + "-1)"


def translate_list_method(lines, i):
    original = lines[i]
    line = clip_comment(lines[i])
    name = line[:line.find(".")].strip()
    copy = line.replace(name + ".", name + "_copy.", 1)
    if ".pop()" in line:
        copy = translate_pop(copy)
    lines[i] = get_indent(line) + "try:"
    lines.insert(i+1, INDENT + original)
    lines.insert(i+2, INDENT + copy)
    lines.insert(i+3, get_indent(line) + "except Exception:")
    lines.insert(i+4, INDENT + copy)
    return 4


def is_range_loop(line):
    return "range(" in line and ":" in line  # line.strip('\n')[-1] == ":"


def is_each_loop(line):
    return not is_if_statement(line) and "range(" not in line and line.lstrip()[:4] == "for " and ":" in line


def is_while_loop(line):
    return line.lstrip()[:6] == "while " and ":" in line


def is_if_statement(line):
    return (line.lstrip()[:3] == "if " or line.lstrip()[:3] == "if(") and ":" in line


def is_elif_statement(line):
    return line.lstrip()[:5] == "elif " or line.lstrip()[:5] == "elif(" and ":" in line


def is_else_statement(line):
    line = clip_comment(line)
    return line.lstrip()[:4] == "else" and line.strip()[-1] == ":"


def is_blank_line(line):
    return line == '\n' or len(line.strip()) == 0


def is_obj_declaration(line):
    return "SmallVar(" in line or "List(" in line or "WhileLoop(" in line or "ForEachLoop(" in line or "ForLoopRange(" \
            in line


def is_comment(line):
    if line == '\n' or len(line) == 0:
        return False
    elif starts_with_comment(line):
        return True
    else:
        for i in range(len(line)):
            if line[i] == "#":
                return True
            if line[i].isalnum():
                return False


# returns True if there are operators in the line, False if not
def operators_present(line):
    return "+=" in line or "-=" in line or "*=" in line or "/=" in line or "//=" in line


def is_index_redefinition(line):
    if "=" in line and not operators_present(line) and "==" not in line:
        name = line[:line.find('=')]
        return is_index_of_list(name)


# returns true if the line is declaring a new variable
def is_var_declaration(line):
    if "=" in line and not is_print_statement(line) and "==" not in line:
        name = line[:line.find('=')]
        if is_index_of_list(name):
            return False
        return not operators_present(line) and "[" not in name and not is_if_statement(line) and not is_while_loop(line)
    return False


def is_try_or_exception(line):
    return "try:" in line or "Exception as e:" in line or "e.__class__.__name__" in line


# returns True if a variable 'declaration' is actually an index of a list - ex) words[0] =
def is_index_of_list(name):
    return "[" in name and "]" in name


def is_delete_statement(line):
    return " del " in line or "__del__()" in line


def is_pause_statement(line):
    return "pause(" in line


def is_print_statement(line):
    return "print(" in line


def is_list_method(line):
    for method in Info.list_methods:
        if method in line:
            return True
    return False


# returns true if the line is a for loop
def is_loop(line):
    if line == '\n':
        return False
    return is_range_loop(line) or is_each_loop(line) or is_while_loop(line)


def starts_with_comment(line):
    return line.strip().find("#") == 0


def clip_comment(line):
    com = line.find("#")
    if starts_with_comment(line):
        return '\n'
    elif com != -1:
        return line[:com]
    return line


def should_skip(line):
    return is_comment(line) or is_delete_statement(line) or is_blank_line(line) or is_pause_statement(line) or\
           is_try_or_exception(line) or "finished()" in line or 'display_lines(' in line or "try:" in line or \
           "temp1999x" in line


# returns which type, big or small, a variable is
def get_var_type(val):
    if "[" in val and "]" in val:
        found = val.find("[")
        if not val[found-1].isalpha():
            return "big"
    return "small"


# returns the spaces equivalent to the index of the line
def get_indent(line):
    if line == '\n':
        return ''
    else:
        return INDENT*get_num_indents(line)


# returns the number of indents on the given line
def get_num_indents(line):
    for i in range(len(line)):
        if line[i].isalpha():
            return int(i/len(INDENT))
    return 0


def should_animate(lines, i):
    line = lines[i]
    if operators_present(line) or is_var_declaration(line) or is_print_statement(line) or is_redeclaration(lines, i) \
            or is_list_method(line) or is_loop(line):
        return "True"
    return "False"
