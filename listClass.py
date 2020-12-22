
from allPurpose import *
from smallVarClass import SmallVar
from finderClass import Finder
import sys
import time

# A List is just a normal python list, but it animates each
# of the default 11 built-in methods, as well as some more
# that I created.


class List(Finder):

    def __init__(self, canvas, name, l):
        if Info.BIG_VAR_COUNT == 3:
            not_supported(canvas, "Sorry, we can only display 3 lists on the screen at a time!")
        Info.BIG_VAR_COUNT += 1
        Info.big_vars.append(name)
        self.canvas = canvas
        self.name = name
        self.val = l
        self.vid = Info.BIG_VAR_COUNT
        self.text_height = START_Y + (self.vid-1)*GAP
        self.index_height = self.text_height - OFFSET_Y
        self.fs = FONT_SIZE
        self.char_len = self.fs/1.7
        if self.vid > 3:
            not_supported(self.canvas, "Sorry, due to space we only support 3 lists in the window at a time.")
            return
        self.index_cords = {}
        self._draw_list()
        self.label = label_big_var(self.canvas, self.name, self.text_height)
        pause(self.canvas, SPEED/2)

    def __del__(self):
        Info.BIG_VAR_COUNT -= 1
        Info.big_vars.remove(self.name)
        self.canvas.create_rectangle(0, self.text_height-GAP/2, VAR_SECTION_X-2, self.text_height+GAP/2, fill='black')

    # adds the given value to the end of the list
    def append(self, value):
        if Info.ERROR:
            return
        if not APPEND:
            self.val.append(value)
            self.update_list()
            return
        if not FOR_LOOP_PRESENT:
            pause(self.canvas, SPEED/2)
        self.val.append(value)
        self._draw_list()
        self._show_addition(len(self.val)-1)

    # clears the list
    def clear(self):
        if Info.ERROR:
            return
        pause(self.canvas, SPEED)
        self.val.clear()
        self.update_list()

    # returns a copy of the list
    def copy(self):
        if Info.ERROR:
            return
        pause(self.canvas, SPEED)
        return self.val.copy()

    # returns the number of times that val is in the list
    def count(self, val):
        if Info.ERROR:
            return
        if not COUNT:
            return self.val.count(val)
        pause(self.canvas, SPEED/2)
        count = SmallVar(self.canvas, "count", 0, FLASH, True)
        pause(self.canvas, SPEED/2)
        finder = Finder(self, val, 0)
        if val not in self.val:
            end = self._find_index_x(len(self.val))
            finder.move_to(end)
            pause(self.canvas, SPEED)
            finder.delete_search_bar()
            return 0

        for i in range(len(self.val)+1):
            found = self._find_index_x(i)
            finder.move_to(found)
            if i < len(self.val) and self.val[i] == val:
                finder.mark_found_index(i)
                marked_i = self._label_index(i, SEARCH_COLOR)
                count.plus_equals(1)
                self.canvas.itemconfigure(finder.top_bar, width=FONT_SIZE/25)
                self.canvas.itemconfigure(finder.bot_bar, width=FONT_SIZE/25)
                self.canvas.delete(marked_i)

        pause(self.canvas, SPEED/2)
        finder.delete_search_bar()
        ret = count.val
        del count
        pause(self.canvas, SPEED/2)
        return ret

    # adds each element in value to the end of the list
    def extend(self, value):
        if Info.ERROR:
            return
        if type(value) == int:
            throw_error(self.canvas, "TypeError: Your extend() parameter must be iterable. An integer (" + str(value)
                        + ") is not iterable \n (you can't loop through it). Examples of iterable types include: "
                          "string, list, and tuple.", False)
            return
        if not EXTEND:
            self.val.extend(value)
            self.update_list()
            return
        else:
            prev_size = len(self.val)
            self.val.extend(value)
            self._draw_list()
            for i in range(0, len(value)):
                self._show_addition(prev_size+i)
            pause(self.canvas, SPEED/2)

    # highlights the value at the given index and that index in the given color
    def highlight_val_at_index(self, index, color):
        if Info.ERROR:
            return
        pause(self.canvas, SPEED/2)
        if self._is_invalid_index(index):
            self._segfault(index, "IndexError: The index you are trying to highlight (" + str(index) +
                           ") does not exist.\n The value must be be on the interval from " + "[" +
                           str(-len(self.val)) + ", " + str(len(self.val) - 1) + "]")
            return

        x = self._find_index_x(index)
        length = get_item_length(self.val[index], self.fs)
        blackout = self.canvas.create_rectangle(x, self.text_height-FONT_SIZE/2, x + length,
                                                self.text_height+FONT_SIZE/2, fill='black')
        val = self.val[index]
        if type(self.val[index]) == str:
            val = "'" + self.val[index] + "'"

        tex = self.canvas.create_text(x - CHAR_LEN*.15, self.text_height, text=str(val), fill=color,
                                      font=("Courier", self.fs, 'bold'), anchor=tkinter.W)
        label = self._label_index(index, color)
        self.canvas.itemconfigure(label, font=("Courier", INDEX_FONT_SIZE, 'bold'))
        pause(self.canvas, SPEED)
        self.canvas.delete(blackout)
        self.canvas.delete(tex)
        self.canvas.delete(label)
        pause(self.canvas, SPEED/2)

    # returns the index where the value 'val' is located in the list
    def index(self, val):
        if Info.ERROR:
            return
        if val not in self.val:
            if INDEX:
                finder = Finder(self, val, 0)
                end = self._find_index_x(len(self.val))
                finder.move_to(end)
                finder.mark_ob("ValueError: The value '" + str(finder.search_for) + "' is not in " + self.name +
                               ". Therefore, no index can be returned.", True)
                tkinter.mainloop()
            else:
                throw_error(self.canvas, "ValueError: The value '" + str(val) +
                            "' is not in " + self.name + ". Therefore, no index can be returned.", False)
            return NOT_IN_LIST
        else:
            finder = Finder(self, val, 0)
            found = self.val.index(val)
            x = self._find_index_x(found)
            finder.move_to(x)
            box = finder.box_index(found, SEARCH_COLOR)
            finder.delete_search_bar()
            pause(self.canvas, SPEED)
            self.canvas.delete(box)
            return found

    # inserts val at the specified index in the list
    def insert(self, index, value):
        if Info.ERROR:
            return
        if not INSERT:
            self.val.insert(index, value)
            self.update_list()
            return
        pause(self.canvas, SPEED/2)
        self.val.insert(index, value)
        self._draw_list()
        self._show_addition(index)

    def pop(self, index):
        if Info.ERROR:
            return
        if self._is_invalid_index(index):
            if POP and not FOR_LOOP_PRESENT:
                pause(self.canvas, SPEED / 2)
            # popping an empty list has different error message
            if len(self.val) == 0:
                self._segfault(index, "IndexError: You cannot call pop() on an empty list.")
                return
            else:
                self._segfault(index, "IndexError: The index you are trying to pop ("
                               + str(index) + ") does not exist.\nThe value must be be on the interval " +
                               "[" + str(-len(self.val)) + ", " + str(len(self.val) - 1) + "].")
                tkinter.mainloop()

        if not POP:
            ret = self.val.pop(index)
            self.update_list()
            return ret

        # actually animate it
        if not FOR_LOOP_PRESENT:
            pause(self.canvas, SPEED / 2)
        self._draw_x_at_index(index)
        val = self.val.pop(index)
        self.update_list()
        return val

    # removes the value 'val' from the list
    def remove(self, val):
        if Info.ERROR:
            return
        if val not in self.val:
            if REMOVE:
                pause(self.canvas, SPEED / 2)
                finder = Finder(self, val, 0)
                end = self._find_index_x(len(self.val))
                finder.move_to(end)
                finder.mark_ob("ValueError: The value (" + str(val) + ") is not in " + self.name + ".", False)
            else:
                throw_error(self.canvas, "ValueError: The value (" + str(val) + ") is not in " + self.name + ".", False)
        else:
            if not REMOVE:
                self.val.remove(val)
                self.update_list()
                return
            # actually animate it
            pause(self.canvas, SPEED / 2)
            finder = Finder(self, val, 0)
            found = self.val.index(val)
            x = self._find_index_x(found)
            finder.move_to(x)
            finder.mark_found_index(found)
            pause(self.canvas, SPEED/4)
            self.pop(found)

    # reverses the list
    def reverse(self):
        if Info.ERROR:
            return
        pause(self.canvas, SPEED/2)
        self.val.reverse()
        self.update_list()

    # sets the value at index i in the list to val; ----> list[i] = val
    def set_index_to(self, i, val):
        if Info.ERROR:
            return
        if self._is_invalid_index(i):
            self._segfault(i, "IndexError: The index you are trying to change (" + str(i) + ") does not exist.")
            return
        self.val[i] = val
        self.update_list()

    # sets the value at index ii in index i to val; ---> list[i][ii] = val
    def set_index_of_index_to(self, i, ii, val):
        if Info.ERROR:
            return
        if self._is_invalid_index(i):
            self._segfault(i, "IndexError: The index you are trying to change (" + str(i) + ") does not exist.")
            return
        if ii < -len(self.val[i]) or ii >= len(self.val[i]):
            throw_error(self.canvas, "IndexError: The index you are trying to change (" + str(ii) +
                        ") does not exist in the list at index " + str(i) + ".", False)
            return
        self.val[i][ii] = val
        self.update_list()

    # redefines the list
    def reset_to(self, val):
        if Info.ERROR:
            return
        self.val = val
        self.update_list()
        pause(self.canvas, SPEED/2)

    # sorts the list alphabetically/numerically
    def sort(self):
        if Info.ERROR:
            return
        pause(self.canvas, SPEED/2)
        if self._not_same_types():
            return
        self.val.sort()
        self.update_list()
        pause(self.canvas, SPEED/2)

    # redraws the updated list; made for aesthetic purposes
    def update_list(self):
        if Info.ERROR:
            return
        self._draw_list()
        pause(self.canvas, SPEED/2)

    def update(self, val):
        self.val = val
        self._draw_list()
        pause(self.canvas, SPEED/2)

    # returns True if all elements in the list are the same type, False if otherwise; used to error check .sort()
    def _not_same_types(self):
        seen = set()
        for item in self.val:
            t = get_type(item)
            if t not in seen:
                seen.add(t)
        if len(seen) > 1:
            throw_error(self.canvas, "TypeError: " + self.name + " cannot be sorted because it contains more than one"
                                                                 " variable type \n" + str(seen) + ".", False)
            return True
        return False

    # blacks out the list so that a new list can be drawn
    def _clear_list(self):
        self.canvas.create_rectangle(START_X, self.index_height-INDEX_FONT_SIZE/2, VAR_SECTION_X-2,
                                     self.text_height + 1.1*FONT_SIZE, fill=BACKGROUND, outline=BACKGROUND)

    # draws the list
    def _draw_list(self):
        self._clear_list()
        self.fs = get_font_size(str(self.val), FONT_SIZE, VAR_SECTION_X-START_X)
        self.char_len = self.fs/1.7
        self._label_indexes()
        self.canvas.create_text(START_X, self.text_height, text=str(self.val), fill=DEFAULT,
                                font=("Courier", self.fs), anchor=tkinter.W)

    # draws a red 'x' over the index being removed
    def _draw_x_at_index(self, index):
        x1 = self._find_index_x(index)
        if len(self.val) > 0:
            x2 = x1 + get_item_length(self.val[index], self.fs)
        else:
            x2 = x1
        y1 = self.text_height - self.fs*.8
        y2 = self.text_height + self.fs*.8
        mid_x = x1 + (x2-x1)/2
        mid_y = y1 + (y2-y1)/2
        self.canvas.create_line(x1, y1, mid_x, mid_y, x1, y2, mid_x, mid_y, x2, y1, mid_x, mid_y, x2, y2, mid_x,
                                mid_y, fill='red', width=FONT_SIZE/9)
        pause(self.canvas, SPEED*.75)

    # illuminates an index that is too far off the screen to accurately depict proportionally
    def _edge_segfault(self, index):
        self.canvas.create_text(VAR_SECTION_X - 10, self.text_height, text="...[ ]", fill='red',
                                font=("Courier", self.fs), anchor=tkinter.E)
        midpoint = self.char_len * len('...[ ]') * .75
        self.canvas.create_text(VAR_SECTION_X - midpoint/2, self.index_height, text=index, fill='red',
                                font=("Courier", int(self.fs/2)))

    # flashes an object and blacks it out afterwards
    def _flash_obj(self, obj, color):
        for i in range(0, 2):
            pause(self.canvas, SPEED / 9)
            self.canvas.itemconfigure(obj, fill=BACKGROUND)
            pause(self.canvas, SPEED / 9)
            self.canvas.itemconfigure(obj, fill=color)

    # flashes two objects simultaneously, leave boolean False if you want to delete the objects afterwards
    def _flash_pair(self, left, right, color):
        for i in range(0, 2):
            pause(self.canvas, SPEED / 6)
            self.canvas.itemconfigure(left, fill=BACKGROUND)
            self.canvas.itemconfigure(right, fill=BACKGROUND)
            pause(self.canvas, SPEED / 6)
            self.canvas.itemconfigure(left, fill=color)
            self.canvas.itemconfigure(right, fill=color)

    # returns the font size for a list so that it can fit on the screen
    def _get_list_font_size(self):
        i = 0
        while True:
            f = tkinter.font.Font(font=("Courier", self.fs - i))
            if START_X + f.measure(str(self.val)) + self.char_len < VAR_SECTION_X:
                return self.fs-i
            i += 1

    def _is_invalid_index(self, index):
        return index < -len(self.val) or index >= len(self.val) or len(self.val) == 0

    # draws the specified index in the specified color in the list
    def _label_index(self, i, color):
        x = self._find_index_x(i)
        middle = get_item_length(self.val[i], self.fs)/2
        self.index_cords[i] = x + middle
        return self.canvas.create_text(x+middle, self.index_height, text=i, fill=color,
                                       font=("Courier", INDEX_FONT_SIZE))

    # draws each index of a list
    def _label_indexes(self):
        for i in range(len(self.val)):
            self._label_index(i, DEFAULT)

    # illuminates where the out-of-bounds index would be in red
    def _segfault(self, index, message):
        x = self._find_index_x(index)
        if x < VAR_SECTION_X - get_item_length("...[ ]", self.fs):
            self.canvas.create_text(x, self.text_height, text="[    ]", fill='red', font=("Courier", self.fs),
                                    anchor=tkinter.W)
            midpoint = self.char_len*len('[    ]')/2
            self.canvas.create_text(x + midpoint, self.index_height, text=index, fill='red',
                                    font=("Courier", INDEX_FONT_SIZE))
        else:
            self._edge_segfault(index)

        throw_error(self.canvas, message, False)
        pause(self.canvas, SPEED)

    # flashes two arrows at the given index
    def _show_addition(self, i):
        # edge case for .insert()
        if i < 0:
            i = -1*i + 1
        if i > len(self.val)-1:
            i = len(self.val)-1
        start = self._find_index_x(i)
        length = get_item_length(self.val[i], self.fs)
        end = start + length
        # graphics booster for integers and two-letter strings
        if type(self.val[i]) != list and len(str(self.val[i])) < 3:
            start -= self.char_len
            end += self.char_len
            length += self.char_len * 2
        left_arrow = self.canvas.create_line(start, self.index_height-FONT_SIZE*.6, self.index_cords[i]-length*.1,
                                             self.index_height, fill=ARROW_COLOR, arrow=tkinter.LAST,
                                             width=self.fs/25)
        right_arrow = self.canvas.create_line(end, self.index_height-FONT_SIZE*.6, self.index_cords[i]+length*.1,
                                              self.index_height, fill=ARROW_COLOR, arrow=tkinter.LAST,
                                              width=self.fs/25)
        self._flash_pair(left_arrow, right_arrow, ARROW_COLOR)
        self.canvas.delete(left_arrow)
        self.canvas.delete(right_arrow)

    # underlines the value at the given index, sync boolean doesn't sleep if True
    def _underline_index(self, index, color, sync):
        if index >= len(self.val) or index < -1*len(self.val) or Info.ERROR:
            return
        x = self._find_index_x(index)
        line = self.canvas.create_line(x, self.text_height+FONT_SIZE*.8, x+get_item_length(self.val[index], self.fs),
                                       self.text_height+FONT_SIZE*.8, fill=color)
        if not sync:
            pause(self.canvas, SPEED)
            self.canvas.delete(line)
        self.canvas.update()

    # handles the case when accessing a single index from the list causes an error
    def handle_single_index_error(self, i, name, error):
        if Info.ERROR:
            return
        error = str(error)

        # self._underline_index(i, 'red', True)
        if name == "IndexError":
            self._segfault(i, "IndexError: The index you are trying to change (" + str(i) + ") does not exist.")
            return
        elif name == "TypeError":
            if "/=" in str(error):
                throw_error(self.canvas, "TypeError: You cannot divide a list by anything.", False)
            if "multiply" in error:
                found = error.find("type")
                bad_type = error[found+6:-1]
                throw_error(self.canvas, "TypeError: You can only multiply a list by an int (not a " + bad_type + ").",
                            False)
            if "-=" in error:
                found1 = error.find(" and")
                first = error[found1+6:-1]
                found2 = error.find("-=")
                second = error[found2+5:found1-1]
                art1 = "a"
                art2 = "a"
                if first == "int":
                    art1 = "an"
                if second == "int":
                    art2 = "an"
                throw_error(self.canvas, "TypeError: You cannot subtract " + art1 + " " + first + " from " + art2 + " "
                            + second + ".", False)
            if "+=" in error:
                found1 = error.find(" and")
                first = error[found1+6:-1]
                found2 = error.find("+=")
                second = error[found2+5:found1-1]
                art1 = "a"
                art2 = "a"
                if first == "int":
                    art1 = "an"
                if second == "int":
                    art2 = "an"
                throw_error(self.canvas, "TypeError: You cannot add " + art1 + " " + first + " to " + art2 + " "
                            + second + ".", False)
            if "iterable" in error:
                throw_error(self.canvas, "You can't add a type that is not iterable (ex: int) to a list via +=.", False)
            else:
                throw_error(self.canvas, "TypeError: You " + error, False)
        elif name == "AttributeError":
            f1 = error.find("attribute")
            method = error[f1+11:-1]
            found1 = error.find("'")
            found2 = error.find(" object")
            obj = error[found1+1:found2-1]
            art = "a"
            if obj == "int":
                art = "an"
            if method in Info.list_methods:
                throw_error(self.canvas, "You can only call " + method + "()" + " on a list, not " + art + " " + obj +
                            ".", False)
            else:
                throw_error(self.canvas, "The method " + method + "() does not exist.", False)
        elif name == "ValueError":
            f1 = error.find(":")
            f2 = error.find(" is")
            val = error[f1+1:f2]
            self._underline_index(i, 'red', True)
            throw_error(self.canvas, val + " is not in the list at index " + str(i) + " of the list '" + self.name
                        + "'.", False)
        else:
            throw_error(self.canvas, error, False)

        Info.ERROR = True

    # handles the case when accessing an index from within an index from the list causes an error
    def handle_double_index_error(self, i, ii, name, e):
        if self._is_invalid_index(i):
            self._segfault(i, "IndexError: The index you are trying to change (" + str(i) + ") does not exist.")
        else:
            self._underline_index(i, 'red', True)
            throw_error(self.canvas, "IndexError: The index you are trying to change (" + str(ii) +
                        ") does not exist at index " + str(i) + " of list '" + self.name + "'.", False)


