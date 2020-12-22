

class Finder:

    def __init__(self, canvas, l,  name, text_height, index_height, start_x, value):
        self.canvas = canvas
        self.list = l
        self.name = name
        self.line_height = text_height+ARR_FONT_SIZE*.8
        self.index_height = index_height
        self.search_for = value
        self.length = ARR_FONT_SIZE*1.5
        self.start_x = start_x
        self.val = value
        self.top_bar = self._create_top_bar(start_x, self.length)
        self.bot_bar = self._create_bot_bar(start_x, self.length)

    # moves the search bar to the given x-value
    def move_to(self, des):
        while True:
            self.canvas.move(self.top_bar, 6.5/SPEED, 0)
            self.canvas.move(self.bot_bar, 6.5/SPEED, 0)
            self.canvas.update()
            pos = self.canvas.coords(self.bot_bar)
            if abs(pos[0] - 5) > des:
                return

    # highlights the index, conforms the underline to shortly the item, returns reference to the highlighted index
    def highlight_index(self, found):
        x = self._find_index_x(found)
        length = get_num_chars(self.list[found])*CHAR_LEN
        self.delete_search_bar()
        self.top_bar = self._create_top_bar(x, length)
        self.bot_bar = self._create_bot_bar(x, length)
        self.canvas.itemconfigure(self.top_bar, width=3)
        self.canvas.itemconfigure(self.bot_bar, width=3)

    # boxes the specified index in the given color
    def box_index(self, i, color):
        side_length = 1.5 * INDEX_FONT_SIZE
        y = self.index_height
        if i >= len(self.list):
            x = self._find_index_x(i) + CHAR_LEN + self.length/2
            self.canvas.create_rectangle(x, y-side_length/2, x+side_length, y+side_length/2, outline=color, width=1)
            self.canvas.create_text(x + side_length / 2, y, text="X", fill='red')
        else:
            midpoint = get_num_chars(self.list[i])*CHAR_LEN*.5
            x = self._find_index_x(i) + midpoint - side_length/2
            return self.canvas.create_rectangle(x, y-side_length/2, x+side_length, y+side_length/2, outline=color,
                                                width=3)

    # handles the case when the actual .index() function returns an error because the val was not in the list
    def mark_ob(self, message, box):
        x = self._find_index_x(len(self.list)) + CHAR_LEN
        self.move_to(x)
        self.canvas.itemconfigure(self.top_bar, fill='red')
        self.canvas.itemconfigure(self.bot_bar, fill='red')
        if box:
            self.box_index(len(self.list), 'red')
        show_message(self.canvas, message)
        throw_error(self.canvas)
        pause(self.canvas, SPEED)

    # deletes the search bars
    def delete_search_bar(self):
        self.canvas.delete(self.top_bar)
        self.canvas.delete(self.bot_bar)

    # creates the top yellow search bar
    def _create_top_bar(self, x, length):
        return self.canvas.create_line(x, self.line_height-1.5*ARR_FONT_SIZE, x+length,
                                       self.line_height-1.5*ARR_FONT_SIZE, fill='yellow')

    # creates the bottom yellow search bar
    def _create_bot_bar(self, x, length):
        return self.canvas.create_line(x, self.line_height, x+length, self.line_height, fill='yellow')



