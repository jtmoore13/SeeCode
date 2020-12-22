
from allPurpose import *

# This module contains the classes for the three different types of loops,
# for-range, for-each, and while.

# A ForLoopRange is a grid that slides down from the top of the screen
# and tracks the progression of a for loop range loop, such as
# for i in range(10):


class ForLoopRange:

    def __init__(self, canvas, var, start, stop, step, line):
        Info.FOR_LOOP_COUNT += 1
        Info.active_loops += 1
        if Info.active_loops > 3:
            not_supported(canvas, "Sorry, due to space we can only display 3 loops at a time.")
        if type(start) != int or type(stop) != int or type(step) != int:
            throw_error(canvas, "The parameters for your for-range-loop must be integers.", False)
        self.reverse = False
        if "reversed(" in line or (int(start) > int(stop) and int(step) < 0):
            self.reverse = True
        self.canvas = canvas
        self.var_name = var
        self.start = start
        self.stop = stop
        self.step = step
        self.line = line
        self.first_index = 0
        self.end_index = stop-start-1
        self.will_run = True
        self.figure_out_start_end(start, stop, step)

        self.fid = Info.FOR_LOOP_COUNT
        self.start_x = FOR_START_X + (self.fid-1)*FOR_OFFSET
        self.box_width = self._get_side_length(abs(stop-start))
        self.box_height = .6*self.box_width
        self.squares = []
        self.tag = "tag" + str(Info.FOR_LOOP_COUNT)
        self.cords = []
        if not self.will_run:
            self.cords.append(self.start_x+self.box_width/2)
        self._draw_grid()
        self.box_level = self._slide_down()
        self.ground = self.box_level + self.box_height
        self.label = self._create_label()
        self.marked = self.first_index
        self.visited = False
        self.nested = False
        self.type = "range"
        Info.for_map[self.fid] = self
        if self.fid > 1:
            self.nested = True
            self.prev = Info.for_map[self.fid-1]
            cords = self.canvas.coords(self.label)
            self.tracker = self.canvas.create_line(self.prev.cords[self.prev.first_index], self.prev.ground,
                                                   cords[0], cords[1]-6, fill=GRID_COLOR, dash=(4, 4))
        pause(self.canvas, SPEED/2)

    # causes the grid to slide back up off the screen
    def __del__(self):
        if Info.ERROR:
            return
        Info.active_loops -= 1
        if self.nested:
            self.canvas.delete(self.tracker)
        Info.for_map.pop(self.fid)
        Info.FOR_LOOP_COUNT -= 1
        while True:
            self.canvas.update()
            pos = self.canvas.coords(self.tag)[1]
            self.canvas.move(self.tag, 0, -15)
            self.canvas.move(self.label, 0, -15)
            if pos < -30:
                break
        self.canvas.delete(self.tag)

    # configures the data for a for loop
    def figure_out_start_end(self, start, stop, step):
        # if 'reversed' is in the loop
        if self.reverse and step > 0:  # or (self.start < self.stop and self.step < 0):
            self.first_index = self.stop-self.start-1
            self.end_index = 0
        # if it's reversed via a negative step but no 'reversed' in the line
        elif step < 0:  # and (start < step):
            self.start = stop+1
            self.stop = start+1
            self.first_index = self.stop - self.start - 1
            self.end_index = 0
        # if the loop isn't going to run
        elif (start < stop and step < 0) or (start > stop and step > 0):
            self.first_index = 0
            self.end_index = 0
            self.will_run = False
        elif self.reverse and start > stop and step < 0:
            self.reverse = False
            self.start = stop + 1
            self.stop = start+1
            self.step = -step
            self.first_index = 0
            self.end_index = self.stop-self.start-1
            self.will_run = False
        if start == 0 and stop == 0:
            self.will_run = False

    # highlights an index of the for loop grid
    def visit_index(self, i):
        if Info.ERROR:
            return
        if self.visited:
            self.undo_prev()
        # blinks when restarting a loop
        if self.nested and (not self.reverse and self.visited and i == self.start) or\
                (self.reverse and self.visited and self.marked == self.end_index):
            self._restart_loop()
        # makes last item/tracker/label of next loop gray because this outer-loop has completed an iteration
        if self.fid+1 in Info.for_map and i != self.first_index and self.visited:  # not visited
            nex = Info.for_map[self.fid + 1]
            self.canvas.itemconfigure(nex.tracker, fill=GRID_COLOR)
            self.canvas.itemconfigure(nex.label, fill=GRID_COLOR)
            if nex.type == "range" and nex.will_run:
                self.canvas.itemconfigure(nex.squares[nex.marked][0], fill=GRID_COLOR)
                self.canvas.itemconfigure(nex.squares[nex.marked][1], fill='black')
            elif nex.type == "while":
                # re-draws the tracker line for the next loop when this loop iterates
                if i < len(self.cords):
                    self.canvas.delete(nex.tracker)
                    nex.tracker = self.canvas.create_line(self.cords[i], self.ground, nex.cords[0],
                                                          nex.text_level-nex.fs/2, fill=TRACKER_COLOR, dash=(4, 4))
            else:
                nex.undo_prev()

        # highlights new the square at index i
        self._slide_to_index(i)
        # i-start in case self.start > 0; self.marked is an index
        self.marked = i-self.start
        self.visited = True
        pause(self.canvas, SPEED/2)

    # creates the variable of the for loop such as 'i' or 'j'
    def _create_label(self):
        return self.canvas.create_text(self.start_x + self.box_width/2 + (self.first_index*self.box_width),
                                       self.box_level-self.box_height/2, text=self.var_name, fill=GRID_COLOR,
                                       font=("Courier", 15, 'bold'))

    # makes the grid that will track the for loop progress
    def _draw_grid(self):
        i = 0
        if self.start > self.stop:
            for num in range(self.stop, self.start):
                self._draw_square(i, num)
                i += 1
        else:
            for num in range(self.start, self.stop):
                self._draw_square(i, num)
                i += 1

        fs = get_font_size(self.line, 18, self.start_x - self.box_width*.5)
        self.canvas.create_text(self.start_x - self.box_width / 3, -self.box_height / 2,
                                text=self.line, font=("Courier", fs, 'italic'),
                                fill=GRID_COLOR, tag=self.tag, anchor=tkinter.E)

    def _draw_square(self, i, num):
        square = self.canvas.create_rectangle(self.start_x + i*self.box_width, -self.box_height, self.start_x +
                                              self.box_width + i*self.box_width, 0, outline=GRID_COLOR, width=2,
                                              tag=self.tag)
        fs = get_font_size(i, FOR_LOOP_VAL_SIZE, self.box_width)
        text = self.canvas.create_text(self.start_x + self.box_width/2 + i*self.box_width,
                                       -self.box_height/2, text=num, font=("Courier", fs),
                                       fill=GRID_COLOR, tag=self.tag)
        self.squares.append((square, text))
        self.cords.append(self.start_x + i*self.box_width + self.box_width/2)
        i += 1

    # finds the x-coordinate of the given index i on the grid
    def _find_index_x(self, i):
        return self.start_x + self.box_width*(i-self.start)

    # finds the side length for each box of the grid so that it doesn't go out of the screen
    def _get_side_length(self, size):
        i = 0
        while True:
            if self.start_x + (BOX_HEIGHT-i)*(size+1) < CODE_SECTION_X:
                if BOX_HEIGHT-i < 30:
                    not_supported(self.canvas, "Sorry, there are too many iterations in this loop for us to display "
                                               "nicely!")
                return BOX_HEIGHT-i
            i += 1

    # flashes the beginning index when the for loop is repeating itself
    def _restart_loop(self):
        self.canvas.delete(self.label)
        self.label = self.canvas.create_text(self.start_x + self.box_width/2 + self.first_index*self.box_width,
                                             self.box_level-self.box_height/2, text=self.var_name,
                                             fill=FOR_LOOP_VAR_COLOR, font=("Courier", 15, 'bold'))
        self.canvas.delete(self.tracker)
        # flashes beginning index if the grid already been looped through
        self.canvas.itemconfigure(self.squares[self.marked][1], fill=GRID_COLOR)
        self.canvas.itemconfigure(self.squares[self.first_index][0], fill=TRACKER_COLOR)
        pause(self.canvas, .1)
        self.canvas.itemconfigure(self.squares[self.first_index][0], fill=BACKGROUND)
        pause(self.canvas, .1)
        self.canvas.itemconfigure(self.squares[self.first_index][0], fill=TRACKER_COLOR)

    # animates the for loop grid sliding down from the top of the screen
    def _slide_down(self):
        while True:
            pos = self.canvas.coords(self.tag)[1]
            if pos > FOR_START_Y + (self.fid-1)*FOR_GAP:
                return pos
            self.canvas.move(self.tag, 0, 20)
            self.canvas.update()

    # un-highlights the previously marked index
    def undo_prev(self):
        if self.will_run:
            self.canvas.itemconfigure(self.squares[self.marked][0], fill=BACKGROUND)
            self.canvas.itemconfigure(self.squares[self.marked][1], fill=GRID_COLOR)

    # moves the variable label as well as the tracker line, if applicable, to the desired index
    def _slide_to_index(self, i):
        j = 0
        speed = FOR_LOOP_SPEED
        if self.reverse:
            speed = -FOR_LOOP_SPEED
        while True:
            # moves the tracker line, if the for loop is inside of another for loop
            if self.nested:
                self.canvas.delete(self.tracker)
                cords = self.canvas.coords(self.label)
                self.tracker = self.canvas.create_line(self.prev.cords[self.prev.marked], self.prev.ground, cords[0],
                                                       cords[1]-6, fill=TRACKER_COLOR, dash=(4, 4))
                j += speed
            pos = self.canvas.coords(self.label)[0]
            if not self.reverse:  # i > self.marked or i == 0:
                if pos - self.box_width/2 + speed > self._find_index_x(i):
                    # highlights the new index it has just arrived at
                    self.canvas.itemconfigure(self.label, fill=FOR_LOOP_VAR_COLOR)
                    self.canvas.itemconfigure(self.squares[i - self.start][0], fill=TRACKER_COLOR)
                    self.canvas.itemconfigure(self.squares[i - self.start][1], fill=BACKGROUND)
                    return
            else:
                if pos - self.box_width/2 + speed < self._find_index_x(i):
                    # highlights the new index it has just arrived at
                    self.canvas.itemconfigure(self.label, fill=FOR_LOOP_VAR_COLOR)
                    self.canvas.itemconfigure(self.squares[i - self.start][0], fill=TRACKER_COLOR)  # self.marked
                    self.canvas.itemconfigure(self.squares[i - self.start][1], fill=BACKGROUND)
                    return

            self.canvas.move(self.label, speed, 0)
            self.canvas.update()


# A ForEachLoop is a list that slides down from the top of the screen and tracks
# the progression of a for-each loop, such as 'for word in words:'.

class ForEachLoop:

    def __init__(self, canvas, var_name, name, val, reverse, line):
        Info.FOR_LOOP_COUNT += 1
        Info.active_loops += 1
        if Info.active_loops > 3:
            not_supported(canvas, "Sorry, due to space we can only display 3 loops at a time.")
        self.nested = False
        self.canvas = canvas
        self.var_name = var_name
        self.name = name
        self.val = val
        self.reverse = reverse
        self.line = line.strip()
        self.iterations = 0
        self.will_run = True
        if len(val) == 0:
            self.will_run = False
        # copy of original val because if val == str, we change it by adding spaces
        self.val_copy = val
        self.fid = Info.FOR_LOOP_COUNT
        self.start_x = FOR_START_X + (self.fid-1)*FOR_OFFSET
        self.fs = FOR_LOOP_FONT_SIZE
        self.start_height = -10
        self.tag = "tag" + str(self.fid)
        self.first_index = 0
        self.end_index = len(self.val)-1
        self.step = 1
        if self.reverse:
            self.first_index = len(self.val)-1
            self.end_index = 0
            self.step = -1

        if type(self.val) == str:  # was above
            self._make_str_bigger()

            # if type(self.val) == str:
            #     self.first_index *= 2
        self.label = self._create_label()
        self.pair = self._slide_down()
        self.text_level = self.pair[0]
        self.val_text = self.pair[1]
        self.ground = self.text_level + self.fs*.8 + 20
        self.marked = self.first_index
        self.visited = False
        self.next = self.first_index
        self.type = "each"
        self.cords = self._get_cords()
        Info.for_map[self.fid] = self

        if self.fid > 1:
            self.nested = True
            self.prev = Info.for_map[self.fid-1]
            cords = self.canvas.coords(self.label)
            self.tracker = self.canvas.create_line(self.prev.cords[self.prev.first_index], self.prev.ground,
                                                   cords[0], cords[1]-6, fill=GRID_COLOR, dash=(4, 4))
        pause(self.canvas, SPEED/2)

    # slides the list/string back up off the screen and deletes all of its animations
    def __del__(self):
        if Info.ERROR:
            return
        Info.active_loops -= 1
        self.undo_prev()
        if self.nested:
            self.canvas.delete(self.tracker)
        Info.for_map.pop(self.fid)
        Info.FOR_LOOP_COUNT -= 1
        while True:
            self.canvas.update()
            pos = self.canvas.coords(self.tag)[1]
            self.canvas.move(self.tag, 0, -15)
            self.canvas.move(self.label, 0, -15)
            if pos < -100:
                break
        self.canvas.delete(self.tag)

    # deletes the previously highlighted value's highlighting
    def undo_prev(self):
        self.canvas.delete('hi'*self.fid)

    # updates the variable that is being iterated through, in case it was modified during an iteration
    def update(self, new):
        self.val = new
        if self.fs <= MIN_FONT_SIZE:
            # self.undo_prev()
            not_supported(self.canvas, "The list '" + self.name + "' is getting too big to display! Sorry about "
                                                                  "that.")
            return
        self.fs = get_font_size(self.val, FOR_LOOP_FONT_SIZE, CODE_SECTION_X-self.start_x)

        self.val_copy = self.val
        if type(self.val_copy) == str:
            self._make_str_bigger()

        if self.reverse and len(self.val) > 0 and self.iterations < 1:
            self.first_index = len(self.val_copy)-1
            self.marked = self.first_index
            self.next = self.marked
            self.end_index = 0
            self.step = -1
            self.iterations += 1

        self.canvas.itemconfigure(self.val_text, text=str(self.val), font=("Courier", self.fs))
        self.cords = self._get_cords()

        # slightly updates the tracker line at the beginning if the list was changed at all
        if self.nested and not self.visited and self.marked == 0:
            self.canvas.delete(self.tracker)
            self.canvas.delete(self.label)
            self.label = self.canvas.create_text(self._find_index_x(self.first_index), self.start_height,
                                                 text=self.var_name, fill=GRID_COLOR, font=("Courier", 15, 'bold'),
                                                 tag=self.tag)
            cords = self.canvas.coords(self.label)
            # protects against previous list becoming empty
            if len(self.prev.cords) == 0:
                self.prev.cords.append(self.prev.start_x + get_item_length("[]", self.prev.fs)/4)
            self.tracker = self.canvas.create_line(self.prev.cords[self.prev.marked], self.prev.ground,
                                                   cords[0], cords[1]-6, fill=GRID_COLOR, dash=(4, 4))
        # fixes the highlighting if the string/list has been changed
        elif not self.nested:
            self.undo_prev()
            self.canvas.delete(self.label)
            if self.marked > len(self.val)-1:
                self.marked = -1
            if len(self.val) != 0:
                self.label = self.canvas.create_text(self._find_index_x(self.marked), self.start_height,
                                                     text=self.var_name, fill=FOR_LOOP_VAR_COLOR,
                                                     font=("Courier", 15, 'bold'), tag=self.tag)
                self._highlight_item(self.marked)

            # updates tracker location of the next for loop in case anything in this loop was changed
            if self.fid+1 in Info.for_map:
                nex = Info.for_map[self.fid+1]
                self.canvas.delete(nex.tracker)
                cords = self.canvas.coords(nex.label)
                if len(self.cords) == 0:
                    self.cords.append(self.start_x + get_item_length("[]", self.fs)/4)
                nex.tracker = self.canvas.create_line(self.cords[self.marked], self.ground, cords[0], cords[1]-6,
                                                      fill=GRID_COLOR, dash=(4, 4))

        self.canvas.update()
        # only pauses at the beginning of the very first iteration, because tracker might have shifted
        # if not self.visited:
        #     pause(self.canvas, SPEED/2)

    # highlights the next item in the list/string being iterated over
    def visit_next(self):
        print(self.next)
        if Info.ERROR:
            return
        self.marked = self.next
        if self.visited:
            self.undo_prev()
        # blinks when restarting a loop
        if self.visited and self.marked == self.first_index and self.nested:
            self._restart_loop()

        # makes the tracker and label gray when inactive at end of loop
        if self.fid+1 in Info.for_map:  # and self.marked != self.first_index:
            nex = Info.for_map[self.fid + 1]
            self.canvas.itemconfigure(nex.tracker, fill=GRID_COLOR)   # ALSO HEREE
            self.canvas.itemconfigure(nex.label, fill=GRID_COLOR)
            if nex.type == "range" and nex.will_run:
                self.canvas.itemconfigure(nex.squares[nex.end_index][0], fill=GRID_COLOR)  # HEREE
            elif nex.type == "each":
                nex.undo_prev()

        # highlights new the square at index i
        self._slide_to_index(self.next)
        self.next += self.step

        if not self.reverse:
            if self.next >= len(self.val_copy):
                self.next = self.first_index
        else:
            if self.next < 0:
                self.next = self.first_index
        self.visited = True
        pause(self.canvas, SPEED/2)

    # creates the variable of the for loop such as 'num' or 'word'
    def _create_label(self):
        self.fs = get_font_size(self.val, FOR_LOOP_FONT_SIZE, CODE_SECTION_X - self.start_x)
        return self.canvas.create_text(self._find_index_x(self.first_index), self.start_height-26, text=self.var_name,
                                       fill=GRID_COLOR, font=("Courier", 15, 'bold'), tag=self.tag)

    # finds the x-value where the midpoint of the index is in the list
    def _find_index_x(self, index):
        x = self.start_x + self.fs/1.7
        if not self.will_run:
            return x
        if index < 0:
            return self._find_index_x(len(self.val)+index)
        if type(self.val) == list:
            for i in range(index):
                x += get_item_length(self.val[i], self.fs) + get_weird_spacing(self.fs)
            return x + get_item_length(self.val[index], self.fs) / 2
        elif type(self.val) == str:
            x += get_item_length(self.val_copy[0], self.fs)/6
            for i in range(index):
                x += get_item_length(self.val[i] + " ", self.fs)/2 - i*self._get_weird_loop_spacing(i)
            return x
        else:
            not_supported(self.canvas, "Sorry, we currently only support visuals for iterating over strings and lists.")

    # stupid bug that makes it very difficult to find the space between each char
    def _get_weird_loop_spacing(self, i):
        if self.fs == 30:
            return .15
        elif self.fs == 29:
            return .025
        elif self.fs == 28:
            if i < 10:
                return .1
            return .02
        elif self.fs == 27:
            if i < 10:
                return .05
            return .002
        elif self.fs == 26:
            if i < 9:
                return .09
            return .01
        elif self.fs == 25:
            if i < 12:
                return .1
            return .025
        elif self.fs == 24:
            if i < 9:
                return .09
            return .005
        elif self.fs == 23:
            if i < 12:
                return .08
            if i < 16:
                return .005
            else:
                return .027
        elif self.fs == 22:
            if i < 8:
                return .06
            if i < 13:
                return -.004
            else:
                return .002
        elif self.fs == 21:
            if i < 8:
                return .07
            if i < 13:
                return .05
            else:
                return .012
        elif self.fs == 20:
            if i < 13:
                return .1
            if i < 17:
                return .003
            else:
                return .025
        else:
            not_supported(self.canvas, "Sorry, " + self.name + " is too long to be iteratively animated.")
            return 0

    # puts the x-coordinate of every centered item in the list into a list
    def _get_cords(self):
        cords = []
        for i in range(len(self.val)):
            cords.append(self._find_index_x(i))
        return cords

    # highlights the value at the given index in the tracker color
    def _highlight_item(self, i):
        left = self._find_index_x(i)-get_item_length(self.val_copy[i], self.fs)/2
        right = self._find_index_x(i)+get_item_length(self.val_copy[i], self.fs)/2
        if type(self.val) == str:
            left += self.fs/2
            right -= self.fs/2
        x = self._find_index_x(i)
        text = self.val_copy[i]
        if type(self.val) == list and type(self.val_copy[i]) == str:
            text = "'" + text + "'"
        self.canvas.create_rectangle(left, self.start_height+10, right, self.ground, fill=BACKGROUND,
                                     outline=BACKGROUND, tag='hi'*self.fid)
        self.canvas.create_text(x, self.start_height+26, text=str(text),
                                font=("Courier", self.fs), fill=TRACKER_COLOR, tag='hi'*self.fid)

    # when restarting the loop, the item at index 0 blinks
    def _restart_loop(self):
        self.canvas.delete(self.label)
        self.label = self.canvas.create_text(self._find_index_x(self.first_index), self.start_height, text=self.var_name,
                                             fill=FOR_LOOP_VAR_COLOR, font=("Courier", 15, 'bold'), tag=self.tag)
        self.canvas.delete(self.tracker)
        self._highlight_item(self.marked)
        pause(self.canvas, .1)
        self.canvas.delete("hi"*self.fid)
        pause(self.canvas, .1)
        self._highlight_item(self.marked)
        pause(self.canvas, .1)

    # puts spaces in between characters in a string so it's easier to see the iterations
    def _make_str_bigger(self):
        new = "'"
        for i in range(len(self.val)):
            new += self.val[i]
            if i != len(self.val)-1:
                new += " "
        self.val = new + "'"

    # makes and animates the for loop grid sliding down from the top of the screen
    def _slide_down(self):
        val = self.canvas.create_text(self.start_x, self.start_height, text=str(self.val),
                                      font=("Courier", self.fs), fill=GRID_COLOR, anchor=tkinter.W, tag=self.tag)
        self.canvas.create_text(self.start_x - 20, self.start_height+2, text=self.line,
                                font=("Courier", get_font_size(self.line, 18, self.start_x*.9), 'italic'),
                                fill=GRID_COLOR, tag=self.tag, anchor=tkinter.E)

        while True:
            pos = self.canvas.coords(self.tag)[1]
            if pos > FOR_START_Y + (self.fid-1)*FOR_GAP:
                self.start_height = pos
                return self.start_height, val
            self.canvas.move(self.tag, 0, 20)
            self.canvas.update()

    # moves the variable label as well as the tracker line, if applicable, to the desired index
    def _slide_to_index(self, i):
        j = 0
        while True:
            # moves the tracker line, if the for loop is inside of another for loop
            if self.nested:
                self.canvas.delete(self.tracker)
                cords = self.canvas.coords(self.label)
                self.tracker = self.canvas.create_line(self.prev.cords[self.prev.marked], self.prev.ground, cords[0],
                                                       cords[1]-6, fill=TRACKER_COLOR, dash=(4, 4))
                j += FOR_LOOP_SPEED
            pos = self.canvas.coords(self.label)[0]

            # when the font changes and the tracker needs to go backwards
            if pos > self.cords[i] and j == FOR_LOOP_SPEED:
                self.canvas.delete(self.tracker)
                self.canvas.delete(self.label)
                self.label = self.canvas.create_text(self.cords[self.marked], self.start_height, text=self.var_name,
                                                     fill=FOR_LOOP_VAR_COLOR, font=("Courier", 15, 'bold'),
                                                     tag=self.tag)
                cords = self.canvas.coords(self.label)
                self.tracker = self.canvas.create_line(self.prev.cords[self.prev.marked], self.prev.ground, cords[0],
                                                       self.text_level - self.fs / 2, fill=TRACKER_COLOR, dash=(4, 4))
                self._highlight_item(i)
                break

            if self.reverse:
                if pos - .75*FOR_LOOP_SPEED < self.cords[i]:
                    # highlights the new index
                    self.canvas.itemconfigure(self.label, fill=FOR_LOOP_VAR_COLOR)
                    self._highlight_item(self.marked)
                    # moves the tracker for the next while loop if applicable
                    if self.fid+1 in Info.for_map:
                        nex = Info.for_map[self.fid + 1]
                        if nex.type == "while":
                            self.canvas.delete(nex.tracker)
                            nex.tracker = self.canvas.create_line(self.cords[self.marked], self.ground, nex.cords[0],
                                                                  nex.text_level - nex.fs / 2,
                                                                  fill=TRACKER_COLOR, dash=(4, 4))
                    return
                self.canvas.move(self.label, -FOR_LOOP_SPEED, 0)
                self.canvas.update()
            else:
                if pos + FOR_LOOP_SPEED > self.cords[i]:
                    # highlights the new index
                    self.canvas.itemconfigure(self.label, fill=FOR_LOOP_VAR_COLOR)
                    self._highlight_item(self.marked)
                    # moves the tracker for the next while loop if applicable
                    if self.fid+1 in Info.for_map:
                        nex = Info.for_map[self.fid + 1]
                        if nex.type == "while":
                            self.canvas.delete(nex.tracker)
                            nex.tracker = self.canvas.create_line(self.cords[self.marked], self.ground, nex.cords[0],
                                                                  nex.text_level - nex.fs / 2,
                                                                  fill=TRACKER_COLOR, dash=(4, 4))
                    return
                self.canvas.move(self.label, FOR_LOOP_SPEED, 0)
                self.canvas.update()


# A WhileLoop is simply a text that comes down and displays the current
# status of the while loop condition (True or False)

class WhileLoop:

    def __init__(self, canvas, condition):
        Info.FOR_LOOP_COUNT += 1
        Info.active_loops += 1
        if Info.active_loops > 3:
            not_supported(canvas, "Sorry, due to space we can only display 3 loops at a time.")
        self.canvas = canvas
        self.condition = condition
        self.fid = Info.FOR_LOOP_COUNT
        self.start_x = FOR_START_X + (self.fid - 1) * FOR_OFFSET
        self.fs = FOR_LOOP_FONT_SIZE
        self.message = "True?"
        self.start_height = -10
        self.tag = "tag" + str(self.fid)
        self.state_tag = "stag" + str(self.fid)
        self.visited = False
        self.nested = False
        self.type = "while"
        self.text_level = self._slide_down()
        self.ground = self.text_level + self.fs/2
        self.cords = [self.start_x + get_item_length(self.message, self.fs)/2 - self.fs/2.5]
        self.marked = 0
        self.label = self.state_tag
        self.first_index = 0
        Info.for_map[self.fid] = self

        if self.fid > 1:
            self.nested = True
            self.prev = Info.for_map[self.fid-1]
            self.tracker = self.canvas.create_line(self.prev.cords[self.prev.first_index], self.prev.ground,
                                                   self.cords[self.first_index], self.text_level-self.fs/2,
                                                   fill=GRID_COLOR, dash=(4, 4))
        pause(self.canvas, SPEED/2)

    def __del__(self):
        if Info.ERROR:
            return
        Info.active_loops -= 1
        # pause(self.canvas, SPEED)
        Info.for_map.pop(self.fid)
        Info.FOR_LOOP_COUNT -= 1
        if self.nested:
            self.canvas.delete(self.tracker)
        while True:
            self.canvas.update()
            pos = self.canvas.coords(self.tag)[1]
            self.canvas.move(self.state_tag, 0, -15)
            self.canvas.move(self.tag, 0, -15)
            if pos < -100:
                break
        self.canvas.delete(self.tag)

    # called after the while loop condition has been exhausted and is now false
    def finished(self):
        self.message = "False"
        self.canvas.itemconfigure(self.state_tag, text=self.message, fill='light coral')
        # makes last item/tracker/label of next loop gray because this outer-loop has completed an iteration
        if self.fid+1 in Info.for_map:
            nex = Info.for_map[self.fid + 1]
            self.canvas.itemconfigure(nex.tracker, fill=GRID_COLOR)
            self.canvas.itemconfigure(nex.label, fill=GRID_COLOR)
            if nex.type == "range":
                self.canvas.itemconfigure(nex.squares[nex.end_index][0], fill=GRID_COLOR)
            elif nex.type == "each":
                self.canvas.itemconfigure(nex.label, fill=GRID_COLOR)
                nex.undo_prev()
            elif nex.type == "while":
                self.canvas.itemconfigure(nex.label, fill=GRID_COLOR)
        pause(self.canvas, SPEED)

    # makes the while loop true, called at the beginning of each loop iteration
    def mark(self):
        self.canvas.delete(self.state_tag)
        self.message = "True"
        self.canvas.create_text(self.start_x + self.fs/1.7, self.text_level, font=("Courier", self.fs, 'italic'),
                                text=self.message, fill='pale green', tag=self.state_tag, anchor=tkinter.W)
        if self.nested:
            self.canvas.itemconfigure(self.tracker, fill=TRACKER_COLOR)

        # makes last item/tracker/label of next loop gray because this outer-loop has completed an iteration
        if self.fid+1 in Info.for_map:
            nex = Info.for_map[self.fid + 1]
            self.canvas.itemconfigure(nex.tracker, fill=GRID_COLOR)
            self.canvas.itemconfigure(nex.label, fill=GRID_COLOR)
            if nex.type == "range" and nex.will_run and nex.marked == nex.end_index:
                self.canvas.itemconfigure(nex.squares[nex.end_index][0], fill=GRID_COLOR)
            elif nex.type == "each":
                self.canvas.itemconfigure(nex.label, fill=GRID_COLOR)
                nex.undo_prev()
            elif nex.type == "while":
                self.canvas.itemconfigure(nex.label, fill=GRID_COLOR)
        pause(self.canvas, SPEED/2)

    # blinks True at the beginning of each iteration
    def _blink(self):
        self.canvas.itemconfigure(self.state_tag, fill=BACKGROUND)
        pause(self.canvas, .1)
        self.canvas.itemconfigure(self.state_tag, fill='pale green')

    # has the 'while clause' slide down from the top of the screen to its starting position
    def _slide_down(self):
        self.canvas.create_text(self.start_x, -10, text=self.condition, fill=GRID_COLOR,
                                font=("Courier", 18), tag=self.tag, anchor=tkinter.E)
        self.state = self.canvas.create_text(self.start_x + self.fs / 1.7, -10, font=("Courier", self.fs, 'italic'),
                                             text=self.message, fill=GRID_COLOR, tag=self.tag, anchor=tkinter.W)
        while True:
            pos = self.canvas.coords(self.tag)[1]
            if pos - 15 > FOR_START_Y + (self.fid-1)*FOR_GAP:
                self.start_height = pos
                self.canvas.itemconfigure(self.state, tag=self.state_tag)
                return self.start_height
            self.canvas.move(self.tag, 0, 20)
            self.canvas.update()
