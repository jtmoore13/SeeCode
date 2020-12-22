
from allPurpose import *

# A Finder is a search bar that finds where a value or index is
# in the list. It can perform several operations such as highlighting,
# underlining, and flashing certain canvas objects to animate certain
# list methods.


class Finder:

    def __init__(self, list_obj, value, start_x):
        self.canvas = list_obj.canvas
        self.val = list_obj.val
        self.line_height = list_obj.text_height+list_obj.fs*.8
        self.index_height = list_obj.index_height
        self.search_for = value
        self.fs = list_obj.fs
        self.char_len = list_obj.char_len
        self.length = get_item_length(value, self.fs)
        self.index_cords = list_obj.index_cords
        self.top_bar = self._create_top_bar(start_x, self.length)
        self.bot_bar = self._create_bot_bar(start_x, self.length)

    # boxes the specified index in the specified color
    def box_index(self, i, color):
        side_length = 1.5 * INDEX_FONT_SIZE
        y = self.index_height
        if i > len(self.val)-1:
            x = self._find_index_x(i + self.char_len + self.length/2)
            self.canvas.create_rectangle(x, y-side_length/2, x+side_length, y+side_length/2, outline=color, width=1)
            self.canvas.create_text(x + side_length / 2, y, text="X", fill=SEGFAULT_COLOR)
        else:
            x = self.index_cords[i] - side_length/2
            box = self.canvas.create_rectangle(x, y-side_length/2, x+side_length, y+side_length/2, outline=color,
                                               width=INDEX_FONT_SIZE/4)
            return box

    # deletes the two search bars
    def delete_search_bar(self):
        self.canvas.delete(self.top_bar)
        self.canvas.delete(self.bot_bar)

    # highlights the index and conforms the bold underline to fit the item length
    def mark_found_index(self, found):
        self.delete_search_bar()
        x = self._find_index_x(found)
        length = get_item_length(self.val[found], self.fs)
        self.top_bar = self._create_top_bar(x, length)
        self.canvas.itemconfigure(self.top_bar, width=3*self.fs/25)
        self.bot_bar = self._create_bot_bar(x, length)
        self.canvas.itemconfigure(self.bot_bar, width=3*self.fs/25)

    # handles the case when the actual .index() call returns an error because val was not in the list
    def mark_ob(self, message, box):
        x = self._find_index_x(len(self.val)) + self.char_len
        self.move_to(x)
        self.canvas.itemconfigure(self.top_bar, fill=SEGFAULT_COLOR)
        self.canvas.itemconfigure(self.bot_bar, fill=SEGFAULT_COLOR)
        if box:
            self.box_index(len(self.val), SEGFAULT_COLOR)
        throw_error(self.canvas, message, False)
        pause(self.canvas, SPEED)

    # moves the search bar horizontally to the given x-value destination
    def move_to(self, des):
        while True:
            self.canvas.move(self.top_bar, 5/SPEED, 0)
            self.canvas.move(self.bot_bar, 5/SPEED, 0)
            self.canvas.update()
            pos = self.canvas.coords(self.top_bar)
            if abs(pos[0] - 5) > des:
                return

    # creates and returns reference to the top search bar
    def _create_top_bar(self, start_x, length):
        return self.canvas.create_line(start_x, self.line_height-1.5*self.fs, start_x+length,
                                       self.line_height-1.5*self.fs, fill=SEARCH_COLOR, width=self.fs/25)

    # creates and returns reference to the bottom search bar
    def _create_bot_bar(self, start_x, length):
        return self.canvas.create_line(start_x, self.line_height, start_x+length, self.line_height, fill=SEARCH_COLOR,
                                       width=self.fs/25)

    # finds the x-value where the value at index is in the list
    def _find_index_x(self, index):
        # deals with negative indexes
        index = int(index)
        if index < 0:
            return self._find_index_x(len(self.val)+index)

        x = START_X + self.char_len
        for i in range(0, index):
            if i < len(self.val):
                x += get_item_length(self.val[i], self.fs) + get_weird_spacing(self.fs)
        # for indexes out of bounds
        if index >= len(self.val):
            separation = (index - len(self.val)-self.fs/180) * self.fs*3.75
            return x + separation
        return x
