from allPurpose import *
from listClass import List
from settings import *
from infoClass import Info
from smallVarClass import SmallVar
from loopsClass import ForEachLoop
from loopsClass import ForLoopRange
from loopsClass import WhileLoop
import signal, os, sys
from tkinter import *
from random import randint
from fileHandlers import *


# makes the canvas for the animation
def make_canvas(width, height):
    top = tkinter.Tk()
    top.title('SeeCode')
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.configure(bg=BACKGROUND)
    canvas.create_line(VAR_SECTION_X, CONTAINER_SECTION_Y, VAR_SECTION_X, CANVAS_HEIGHT, fill='gray20', dash=(4, 4))
    canvas.create_text((CANVAS_WIDTH+VAR_SECTION_X)/2, VAR_SECTION_Y-10, text='str/int/bool',
                       font=("Courier", 17, 'italic'), fill='gray35')
    canvas.create_line(0, CONTAINER_SECTION_Y, CANVAS_WIDTH, CONTAINER_SECTION_Y, fill='gray20', dash=(4, 4))
    canvas.create_text(15, CONTAINER_SECTION_Y-10, text='lists', font=("Courier", 17, 'italic'),
                       fill='gray35', anchor=tkinter.W)
    canvas.create_text(15, 58, text='loops', font=("Courier", 17, 'italic'),
                       fill='gray35', anchor=tkinter.W)
    canvas.create_line(CODE_SECTION_X, 0, CODE_SECTION_X, VAR_SECTION_Y, fill='gray20', dash=(4, 4))
    word = Info.adjectives[randint(0, len(Info.adjectives)-1)]
    canvas.create_text(CODE_SECTION_X+10, 20, text='Your ' + word + ' code', font=('Courier', 17, 'italic'),
                       fill='gray50', anchor=tkinter.W)
    canvas.pack()
    var = tkinter.IntVar()
    Info.var = var
    pause_button = Button(text="Pause", command=pause_b, activeforeground='red', anchor=CENTER, relief=FLAT, borderwidth=14)
    pause_button.configure(width=5, relief=FLAT)
    canvas.create_window(CANVAS_WIDTH - 93, 20, anchor=CENTER, window=pause_button)
    Info.state = canvas.create_oval(CANVAS_WIDTH - 16, 15, CANVAS_WIDTH - 6, 25, fill='green2', outline='green2')
    Info.button = pause_button
    play_button = Button(text="Play", command=lambda: Info.var.set(1), activeforeground='green4', anchor=CENTER)
    play_button.configure(width=4, activebackground="#33B5E5", relief=FLAT)
    canvas.create_window(CANVAS_WIDTH - 43, 20, anchor=CENTER, window=play_button)
    return canvas


def pause_b():
    if Info.ERROR:
        return
    Info.c.itemconfigure(Info.state, fill='red', outline='red')
    Info.button.wait_variable(Info.var)
    Info.c.itemconfigure(Info.state, fill='green2', outline='green2')


def handler(signum, frame):
    pass


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    Info.c = canvas
    set_state(canvas, "Running...", False)
    pause(canvas, SPEED/2)

    # USER CODE BELOW #

    lines_1999 = ['listy = [1,2,3]\n', 'for i in range(len(listy)+1):\n', '    if listy[i] == 2:\n', '        print(2)\n']
    show_lines(canvas, lines_1999)
    if check_for_else_syntax_error(lines_1999) != -1:
        display_lines(canvas, check_for_else_syntax_error(lines_1999), 'red')
        throw_error(canvas, 'SyntaxError: There must be code inside an else/elif statement.', True)
    pause(canvas, SPEED/2)

    try:
        pass
        display_lines(canvas, 0, HIGHLIGHT)
        temp1999x = [1,2,3]
        listy = temp1999x  # line num =0
        if type(listy) == list:
            if not is_already_a_var('listy'):
                listy_copy = List(canvas, 'listy', temp1999x.copy())
            elif is_small_var('listy'):
                del listy_copy
                listy_copy = List(canvas, 'listy', temp1999x.copy())
            elif is_big_var('listy'):
                listy_copy.reset_to(listy)
        elif type(listy) == int or type(listy) == float or type(listy) == str or type(listy) == bool:
            if not is_already_a_var('listy'):
                listy_copy = SmallVar(canvas, 'listy', listy, FLASH, False)
            elif is_big_var('listy'):
                del listy_copy
                listy_copy = SmallVar(canvas, 'listy', listy, FLASH, False)
            elif is_small_var('listy'):
                listy_copy.reset_to(listy)
        elif 'NoneType' in str(type(listy)):
            not_supported(canvas, 'The right side of your expression does not return anything! Therefore, the variable "listy" cannot be set to anything.')
        else:
            not_supported(canvas, 'Sorry, we only support animations for variables of type: int, float, str, bool, list!')
        display_lines(canvas, 1, HIGHLIGHT)
        l1 = ForLoopRange(canvas, 'i', 0, len(listy)+1, 1, 'for i in range(len(listy)+1):  ')
        for i in range(len(listy)+1):  # line num =1
            l1.visit_index(i)
            display_lines(canvas, 2, HIGHLIGHT)
            if listy[i] == 2:  # line num =2
                display_lines(canvas, 2, 'pale green')
                display_lines(canvas, 3, HIGHLIGHT)
                print(2)  # line num =3
        l1.__del__()

    # USER CODE ABOVE #

        if len(lines_1999) > 0:
            display_lines(canvas, 0, DEFAULT)
            pause(canvas, SPEED/2)

    except Exception as e:
        ln = int(format(sys.exc_info()[-1].tb_lineno))
        this_file = open('translated.py', 'r')
        lines = this_file.readlines()
        while "line num =" not in lines[ln-1]:
            ln += 1
        error_line = lines[ln-1]
        last_shown = Info.lines_shown.pop()
        j = ln
        while "line num =" + str(last_shown) not in lines[j]:
            j -= 1
        line = lines[ln-1]
        line_num = int(line[line.find("line num =") + 10:].strip())
        while "line num =" + str(line_num) not in lines[j]:
            if get_num_indents(lines[j]) == get_num_indents(error_line) and is_elif_statement(lines[j]) \
                    and "line num =" in lines[j]:
                
                temp = lines[j]
                curr_line_num = int(temp[temp.find("line num =") + 10:].strip())
                display_lines(canvas, curr_line_num, HIGHLIGHT)
            j += 1
        if is_elif_statement(error_line):
            display_lines(canvas, int(error_line[error_line.find("line num =") + 10:].strip()), HIGHLIGHT)
        handle_all_errors(canvas, error_line, e)

    if not Info.ERROR:
        pause(canvas, FAST)
        set_state(canvas, 'Done', False)
        show_lines(canvas, lines_1999)
    tkinter.mainloop()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    main()
