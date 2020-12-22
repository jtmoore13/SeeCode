
from settings import *
from infoClass import Info
import time, sys, os
import tkinter.font
from fileHandlers import *


def handle_operator_errors(canvas, name, error):
    if Info.ERROR:
        return
    error = str(error)

    if name == "TypeError":
        if "/=" in str(error):
            throw_error(canvas, "TypeError: You cannot divide a list by anything.", True)
        if "multiply" in error:
            found = error.find("type")
            bad_type = error[found + 6:-1]
            throw_error(canvas, "TypeError: You can only multiply a list by an int (not a " + bad_type + ").", True)
        if "-=" in error:
            found1 = error.find(" and")
            first = error[found1 + 6:-1]
            found2 = error.find("-=")
            second = error[found2 + 5:found1 - 1]
            art1 = "a"
            art2 = "a"
            if first == "int":
                art1 = "an"
            if second == "int":
                art2 = "an"
            throw_error(canvas, "TypeError: You cannot subtract " + art1 + " " + first + " from " + art2 + " "
                        + second + ".", True)
        if "+=" in error:
            found1 = error.find(" and")
            first = error[found1 + 6:-1]
            found2 = error.find("+=")
            second = error[found2 + 5:found1 - 1]
            art1 = "a"
            art2 = "a"
            if first == "int":
                art1 = "an"
            if second == "int":
                art2 = "an"
            throw_error(canvas, "TypeError: You cannot add " + art1 + " " + first + " to " + art2 + " "
                        + second + ".", True)
            if "iterable" in error:
                throw_error(canvas, "You can't add a type that is not iterable (ex: int) to a list via +=.", True)
            else:
                throw_error(canvas, "TypeError: You " + error, True)
    elif name == "AttributeError":
        f1 = error.find("attribute")
        method = "." + error[f1 + 11:-1]
        found1 = error.find("'")
        found2 = error.find(" object")
        obj = error[found1 + 1:found2 - 1]
        art = "a"

        if obj == "int":
            art = "an"
        if method in Info.list_methods:
            throw_error(canvas, "You can only call " + method + "()" + " on a list, not " + art + " " + obj +
                        ".", True)
        else:
            throw_error(canvas, "The " + method + "() method does not exist for the variable type " + obj + ".", True)


def has_operators(line):
    return "+=" in line or "-=" in line or "*=" in line or "/=" in line or "//=" in line


def handle_all_errors(canvas, line, e):
    line_num = int(line[line.find("line num =") + 10:].strip())
    canvas.itemconfigure(Info.displayed_lines_map[line_num], fill=ERROR_FONT_COLOR)
    name = str(e.__class__.__name__)

    if has_operators(str(e)) or "iterable" in str(e) or "AttributeError" in name:
        handle_operator_errors(canvas, name, e)
    throw_error(canvas, name + ': ' + str(e), True)


def show_lines(canvas, lines):
    max_fs = 18
    if len(lines) <= 15:
        max_fs = 18
    elif len(lines) <= 17:
        max_fs = 16
    elif len(lines) <= 19:
        max_fs = 14
    elif len(lines) <= 21:
        max_fs = 13
    elif len(lines) <= 22:
        max_fs = 12
    elif len(lines) <= 24:
        max_fs = 11
    elif len(lines) <= 26:
        max_fs = 10
    else:
        Info.TOO_MANY_LINES = True
        not_supported(canvas, "You have too many lines of code! It's going to get hard to display in the code section.")

    fs = get_font_size(get_biggest_line(lines), max_fs, CANVAS_WIDTH-CODE_SECTION_X)
    text_height = tkinter.font.Font(font=('Courier', fs)).metrics('linespace')
    for i in range(len(lines)):
        line = lines[i]
        Info.displayed_lines_map[i] = canvas.create_text(CODE_SECTION_X + 10, 60 + i*text_height, text=line,
                                                         fill=TRACKER_COLOR, font=("Courier", fs), anchor=tkinter.W)


def get_biggest_line(lines):
    biggest = 0
    index = 0
    for i in range(len(lines)):
        line = lines[i]
        if len(line) > biggest:
            biggest = len(line)
            index = i
    if biggest > 0:
        return lines[index]
    return 0


def display_lines(canvas, i, color):
    if color == HIGHLIGHT:
        pause(canvas, SPEED/2)
    if i not in Info.lines_shown:
        Info.lines_shown.append(i)
    canvas.itemconfigure(Info.displayed_lines_map[Info.curr_line], fill=DEFAULT)
    if color == HIGHLIGHT:
        canvas.itemconfigure(Info.displayed_lines_map[i], fill=BACKGROUND)
        pause(canvas, .08)
    canvas.itemconfigure(Info.displayed_lines_map[i], fill=color)
    if color == HIGHLIGHT:
        pause(canvas, SPEED/2)
    Info.curr_line = i
    pause(canvas, SPEED/2)


# labels a big variable with the given name
def label_big_var(canvas, name, text_height):
    font_size = get_font_size(name, FONT_SIZE, START_X*.8)
    label = canvas.create_text(START_X / 2 + 5, text_height, text=name, fill=VAR_COLOR,
                               font=("Courier", font_size, 'bold'))
    pause(canvas, .15)
    canvas.delete(label)
    pause(canvas, .15)
    label = canvas.create_text(START_X / 2 + 5, text_height, text=name, fill=VAR_COLOR, font=("Courier", font_size,
                                                                                              'bold'))
    return label


# returns the font size for the text, given the max font size and the length restriction
def get_font_size(text, max_fs, max_length):
    i = 0
    while True:
        f = tkinter.font.Font(font=("Courier", max_fs - i))
        char_len = (max_fs-i)/1.7
        if f.measure(str(text)) + char_len < max_length:
            return max_fs-i
        i += 1


# returns the number of chars that a value in a list is
def get_num_chars(value):
    if type(value) == str:
        return 2 + len(value)
    elif type(value) == int:
        return len(str(value))
    return 0


def is_already_a_var(var):
    return var in Info.small_vars or var in Info.big_vars


def is_big_var(var):
    return var in Info.big_vars


def is_small_var(var):
    return var in Info.small_vars


# returns the pixel length of the item displayed in the font size on the canvas
def get_item_length(item, font_size):
    f = tkinter.font.Font(font=("Courier", font_size))
    if type(item) == list:
        return f.measure(str(item))
    elif type(item) == str:
        return f.measure("'" + item + "'")
    return f.measure(item)


# returns the y-value of the big variable, given the vid
def get_text_level(vid):
    return (START_Y + SIDE_HEIGHT / 2) + GAP * (vid - 1)


# returns the type of the val as a string
def get_type(val):
    if type(val) == str:
        return "str"
    if type(val) == int:
        return "int"
    if type(val) == list:
        return "list"
    if type(val) == bool:
        return "bool"
    if type(val) == float:
        return "float"
    if type(val) == tuple:
        return "tuple"
    return "missed something"


# lets the user know that this feature is not supported by visuals
def not_supported(canvas, message):
    Info.ERROR = True
    canvas.create_line(0, ERROR_SECTION_Y, CANVAS_WIDTH, ERROR_SECTION_Y, fill='deep sky blue', dash=(4, 4))
    canvas.create_rectangle(1, ERROR_SECTION_Y + 1, CANVAS_WIDTH, CANVAS_HEIGHT - 1, fill=BACKGROUND)
    canvas.create_text(CANVAS_WIDTH / 2, (CANVAS_HEIGHT + ERROR_SECTION_Y) / 2, text=message, fill='deep sky blue',
                       font=("Courier", 18, 'italic'), justify='center', width=CANVAS_WIDTH*.75)
    set_state(canvas, "Sorry", False)
    tkinter.mainloop()


def check_for_else_syntax_error(lines):
    for i in range(len(lines)):
        line = lines[i]
        if (is_else_statement(line) or is_elif_statement(line)) and i+1 < len(lines) and get_num_indents(line) >= \
                get_num_indents(lines[i+1]):
            return i
    return -1


# pauses the animations for the given time
def pause(canvas, secs):
    canvas.update()
    time.sleep(secs)


# displays either 'Running', 'Done', or 'Error' in the upper left corner
def set_state(canvas, state, caught):
    canvas.create_rectangle(1, 1, 170, 50, fill=BACKGROUND, outline=BACKGROUND)
    if state == "Done":
        Info.ERROR = True
        Info.c.itemconfigure(Info.state, fill='grey', outline='grey')
        canvas.create_text(15, 25, text=state, fill='green2', font=("Courier", 25, 'bold'), anchor=tkinter.W)
        canvas.create_line(87, 23, 93, 32, 107, 12, fill='green2', width=3)
        tkinter.mainloop()
    elif state == "Error":
        Info.ERROR = True
        Info.c.itemconfigure(Info.state, fill='grey', outline='grey')
        if not caught:
            canvas.itemconfigure(Info.displayed_lines_map[Info.curr_line], fill=ERROR_FONT_COLOR)

        canvas.create_text(15, 25, text=state, fill=ERROR_FONT_COLOR, font=("Courier", 25, 'bold'), anchor=tkinter.W)
        tkinter.mainloop()
    elif state == "Sorry":
        Info.ERROR = True
        Info.c.itemconfigure(Info.state, fill='grey', outline='grey')
        canvas.create_text(15, 25, text=state, fill='deep sky blue', font=("Courier", 25), anchor=tkinter.W,)
        if not Info.TOO_MANY_LINES:
            canvas.itemconfigure(Info.displayed_lines_map[Info.curr_line], fill='deep sky blue')
        canvas.update()
        tkinter.mainloop()
    else:
        canvas.create_text(15, 25, text=state, fill='gray55', font=("Courier", 25, 'italic'),
                           anchor=tkinter.W)


# displays an error message at the bottom of the canvas
def show_message(canvas, message):
    canvas.create_rectangle(1, ERROR_SECTION_Y+1, CANVAS_WIDTH, CANVAS_HEIGHT-1, fill=BACKGROUND)
    canvas.create_text(CANVAS_WIDTH/2, (CANVAS_HEIGHT + ERROR_SECTION_Y)/2, text=message, fill=ERROR_FONT_COLOR,
                       font=("Courier", 18, 'italic'), justify='center')


# displays the current line of code at the top righ of the canvas
def show_line(canvas, line, animate):
    if Info.ERROR:
        return
    pause(canvas, .25)
    if not animate:
        pause(canvas, .08)
    canvas.create_text(CANVAS_WIDTH - 10, 20, text=line, fill='white', font=("Courier", 18), anchor=tkinter.E)
    pause(canvas, SPEED)
    if animate:
        canvas.create_text(CANVAS_WIDTH - 10, 20, text=line, fill='grey', font=("Courier", 18), anchor=tkinter.E)


# sets the state to 'Error' and displays the error message
def throw_error(canvas, message, caught):
    Info.ERROR = True
    canvas.create_line(0, ERROR_SECTION_Y, CANVAS_WIDTH, ERROR_SECTION_Y, fill='red2', dash=(4, 4))
    show_message(canvas, message)
    set_state(canvas, "Error", caught)
    canvas.update()
    tkinter.mainloop()


# accounts for super weird bug that makes the space between list elements non-linear in relation to font size
# most noticeable in lists of single characters
def get_weird_spacing(fs):
    if fs <= 16:
        return get_item_length("", fs)
    elif fs <= 18:
        return get_item_length("", fs) * .95
    elif fs == 19:
        return get_item_length("", fs) * .95
    elif fs == 20:
        return get_item_length("", fs) * .92
    elif fs <= 22:
        return get_item_length("", fs) * .96
    elif fs == 24:
        return get_item_length("", fs) * .96
    elif fs == 25:
        return get_item_length("", fs) * .95
    elif fs <= 28:
        return get_item_length("", fs) * .96
    else:
        return get_item_length("", fs) * .95
