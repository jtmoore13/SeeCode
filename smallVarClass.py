
from allPurpose import *

# A SmallVar is just a variable that is of type int, str, or bool.
# SmallVars are displayed on the right hand side of the screen, and can
# be added, removed, and have their value changed whenever the caller wants.


class SmallVar:

    def __init__(self, canvas, name, val, flash, built_in):
        if Info.SMALL_VAR_COUNT == 3:
            not_supported(canvas, "Sorry, we can only display 3 simple variables on the screen at a time!")
        Info.SMALL_VAR_COUNT += 1
        Info.small_vars.append(name)
        self.canvas = canvas
        self.name = name
        self.vid = Info.SMALL_VAR_COUNT
        self.val = val
        self.flash = flash
        self.prev = self.val
        self.built_in = built_in
        self.fs = VAR_VAL_FONT_SIZE
        self.text_level = VAR_SECTION_Y + .2*SIDE_HEIGHT + SIDE_HEIGHT*(self.vid - 1) * 1.5
        # for list methods like count, the temp variable will be in top right of screen
        if built_in:
            self.text_level = CONTAINER_SECTION_Y - BOX_HEIGHT*2.1
        data = self._create_var(val)
        self.val_label = data[0]
        self.var_name = data[1]
        self.frame = data[2]
        self.border = self._make_inner_border()
        pause(self.canvas, SPEED/2)

    def __del__(self):
        self.remove_var()

    # updates the variable, equivalent to var /= val
    def divide_by_int(self, val):
        if Info.ERROR or self._type_error(val, "divide"):
            return
        if get_type(val) != "int":
            throw_error(self.canvas, "You can only divide integers by one another.", False)
            return
        color = self._get_color(self.val//val)
        self.fs = get_font_size(self.val//val, VAR_VAL_FONT_SIZE, SIDE_WIDTH)
        self.canvas.itemconfigure(self.val_label, text=str(self.val//val), font=("Courier", self.fs))
        self.val //= val
        self.prev = self.val
        self.canvas.itemconfigure(self.border, outline=color)
        pause(self.canvas, SPEED/2)
        self.canvas.itemconfigure(self.border, outline=BACKGROUND)
        pause(self.canvas, SPEED)

    # updates the variable, equivalent to var //= val
    def divide_by_float(self, val):
        if Info.ERROR or self._type_error(val, "divide"):
            return
        if get_type(val) != "int":
            throw_error(self.canvas, "You can only divide integers by one another.", False)
            return
        color = self._get_color(self.val/val)
        self.prev = self.val
        self.fs = get_font_size(self.val/val, VAR_VAL_FONT_SIZE, SIDE_WIDTH)
        self.canvas.itemconfigure(self.val_label, text=str(self.val/val), font=("Courier", self.fs))
        self.val /= val
        self.prev = self.val
        self.canvas.itemconfigure(self.border, outline=color)
        pause(self.canvas, SPEED/2)
        self.canvas.itemconfigure(self.border, outline=BACKGROUND)
        pause(self.canvas, SPEED)

    # updates the variable, equivalent to var -= val
    def minus_equals(self, val):
        if Info.ERROR or self._type_error(val, "subtract"):
            return
        if get_type(val) != "int":
            throw_error(self.canvas, "TypeError: You can only subtract integers from one another.", False)
            return
        color = self._get_color(self.val - val)
        self.fs = get_font_size(self.val-val, VAR_VAL_FONT_SIZE, SIDE_WIDTH)
        self.canvas.itemconfigure(self.val_label, text=str(self.val - val), font=("Courier", self.fs))
        self.val -= val
        self.prev = self.val
        self.canvas.itemconfigure(self.border, outline=color)
        pause(self.canvas, SPEED/2)
        self.canvas.itemconfigure(self.border, outline=BACKGROUND)
        pause(self.canvas, SPEED)

    # updates the variable, equivalent to var *= val
    def multiply_by(self, val):
        # updates the variable, equivalent to var /= val
        if Info.ERROR or self._type_error(val, "multiply"):
            return
        if get_type(val) != "int":
            throw_error(self.canvas, "You can only multiply a str or int by another int.", False)
            return
        color = self._get_color(self.val * val)
        self.prev = self.val
        self.fs = get_font_size(self.val*val, VAR_VAL_FONT_SIZE, SIDE_WIDTH)
        self.canvas.itemconfigure(self.val_label, text=str(self.val * val), font=("Courier", self.fs))
        self.val *= val
        self.prev = self.val
        self.canvas.itemconfigure(self.border, outline=color)
        pause(self.canvas, SPEED / 2)
        self.canvas.itemconfigure(self.border, outline=BACKGROUND)
        pause(self.canvas, SPEED)

    # updates the variable, equivalent to var += val
    def plus_equals(self, val):
        if Info.ERROR or self._type_error(val, "add"):
            return
        color = self._get_color(self.val + val)
        self.fs = get_font_size(self.val+val, VAR_VAL_FONT_SIZE, SIDE_WIDTH)
        self.canvas.itemconfigure(self.val_label, text=str(self.val + val), font=("Courier", self.fs))
        self.val += val
        self.prev = self.val
        self.canvas.itemconfigure(self.border, outline=color)
        pause(self.canvas, SPEED/2)
        self.canvas.itemconfigure(self.border, outline=BACKGROUND)
        pause(self.canvas, SPEED)

    # removes the variable from the screen
    def remove_var(self):
        pause(self.canvas, SPEED/4)
        Info.SMALL_VAR_COUNT -= 1
        Info.small_vars.remove(self.name)
        # self._slide_out()
        self.canvas.delete(self.val_label)
        self.canvas.delete(self.var_name)
        self.canvas.delete(self.frame)
        pause(self.canvas, SPEED/4)

    # redefines/resets the variable; equivalent to var = new_val
    def reset_to(self, new_val):
        if Info.ERROR:
            return
        color = self._get_color(new_val)
        # so it displays 'True' and 'False' instead of 1, 0
        if type(new_val) == bool:
            new_val = self._convert_bool(new_val)
        self.fs = get_font_size(new_val, VAR_VAL_FONT_SIZE, SIDE_WIDTH)
        self.canvas.itemconfigure(self.val_label, text=str(new_val), font=("Courier", self.fs))
        self.val = new_val
        # flashes the inner border
        self.canvas.itemconfigure(self.border, outline=color)
        pause(self.canvas, SPEED/2)
        self.canvas.itemconfigure(self.border, outline=BACKGROUND)
        pause(self.canvas, SPEED)

    # updates the variable on the screen after the user's code changes it
    def update(self):
        # if type(self.val) == bool:
        #     self.val = self._convert_bool(self.val)
        color = self._get_color(self.val)
        self.prev = self.val
        self.fs = get_font_size(self.val, VAR_VAL_FONT_SIZE, SIDE_WIDTH)
        quotes = ""
        if type(self.val) == str:
            quotes = "'"
        self.canvas.itemconfigure(self.val_label, text=quotes+str(self.val)+quotes, font=('Courier', self.fs))
        self.canvas.itemconfigure(self.border, outline=color)
        pause(self.canvas, SPEED/2)
        self.canvas.itemconfigure(self.border, outline=BACKGROUND)

    # returns True if the new value is a different type than the previous value; error checking for several functions
    def _type_error(self, new_val, operator):
        if operator == "multiply" and get_type(self.val) == "str" and get_type(new_val) == "int":
            return False
        if get_type(self.val) == "float" and get_type(new_val) == "int":
            return False
        if get_type(self.val) == "int" and get_type(new_val) == "float":
            return False

        if get_type(new_val) != get_type(self.val):
            art1 = "a"
            art2 = "a"
            if get_type(new_val) == "int":
                art1 = "an"
            if get_type(self.val) == "int":
                art2 = "an"
            if operator == "subtract":
                throw_error(self.canvas, "TypeError: You cannot subtract " + art1 + " " +
                            get_type(new_val) + " from " + art2 + " " + get_type(self.val) + ".", False)
            elif operator == 'add':
                throw_error(self.canvas, "TypeError: You cannot add " + art1 + " " +
                            get_type(new_val) + " to " + art2 + " " + get_type(self.val) + ".", False)
            elif operator == "multiply":
                throw_error(self.canvas, "TypeError: You cannot multiply " + art2 + " " +
                            get_type(self.val) + " by " + art1 + " " + get_type(new_val) + ".", False)
            elif operator == "divide":
                throw_error(self.canvas, "TypeError: You cannot divide " + art2 + " " +
                            get_type(self.val) + " by " + art1 + " " + get_type(new_val) + ".", False)
            return True
        return False

    # converts a boolean value to a 'True' of 'False' string
    @staticmethod
    def _convert_bool(val):
        return "True" if val else "False"

    # creates and labels the variable box, and returns a reference to the variable's value text
    def _create_var(self, val):
        if type(val) == bool:
            val = self._convert_bool(val)
        if self.built_in:
            frame = self.canvas.create_rectangle(CORNER_SQUARE_X, self.text_level, CORNER_SQUARE_X + SIDE_WIDTH,
                                                 self.text_level + SIDE_HEIGHT, outline='grey',
                                                 width=SIDE_HEIGHT / 25, dash=(2, 5))
        else:
            frame = self.canvas.create_rectangle(CORNER_SQUARE_X, self.text_level, CORNER_SQUARE_X + SIDE_WIDTH,
                                                 self.text_level + SIDE_HEIGHT, outline=SMALL_VAR_FRAME_COLOR,
                                                 width=SIDE_HEIGHT/25)
        name_fs = get_font_size(self.name, VAR_NAME_FONT_SIZE, SIDE_WIDTH)
        name = self.canvas.create_text(CORNER_SQUARE_X + SIDE_WIDTH/2, self.text_level+SIDE_HEIGHT*1.2, text=self.name,
                                       fill=VAR_COLOR, font=("Courier", name_fs, 'bold'))
        val_fs = get_font_size(val, self.fs, SIDE_WIDTH*.8)
        quotes = ""
        if type(self.val) == str:
            quotes = "'"
        value = self.canvas.create_text(CORNER_SQUARE_X + SIDE_WIDTH/2, self.text_level + SIDE_HEIGHT/2,
                                        text=quotes+str(val)+quotes, fill=DEFAULT, font=("Courier", val_fs))
        if self.flash:
            self._flash_name(name, name_fs)
        return value, name, frame

    # determines the color that the variable box lights up when the value changes
    def _get_color(self, new_val):
        prev = self.prev
        if type(self.val) == bool and new_val < prev:
            return 'red'
        if (type(self.val) == int and type(new_val) == int or type(self.val) == float) and new_val < prev:
            return 'red'
        elif type(self.val) == str and len(new_val) < len(prev):
            return 'red'
        elif type(prev) != type(new_val) or prev == new_val:
            return 'gray55'
        return 'green'

    # creates the inner border that will flash a color when the variable's value changes
    def _make_inner_border(self):
        y_offset = SIDE_HEIGHT/25
        x_offset = y_offset + 1
        return self.canvas.create_rectangle(CORNER_SQUARE_X + x_offset, self.text_level + y_offset +
                                            (Info.SMALL_VAR_COUNT-1)*.25 + 1, CORNER_SQUARE_X + SIDE_WIDTH -
                                            x_offset, self.text_level + SIDE_HEIGHT - y_offset, outline=BACKGROUND,
                                            width=SIDE_HEIGHT/20)

    # flashes the name label of newly created small variable
    def _flash_name(self, name, name_fs):
        pause(self.canvas, .15)
        self.canvas.itemconfigure(name, font=("Courier", name_fs, 'bold'), fill=BACKGROUND)
        pause(self.canvas, .15)
        self.canvas.itemconfigure(name, font=("Courier", name_fs, 'bold'), fill=VAR_COLOR)

    # animates the small variable sliding out of the screen
    def _slide_out(self):
        while True:
            pos = self.canvas.coords(self.frame)[0]
            self.canvas.move(self.border, 10, 0)
            self.canvas.move(self.frame, 10, 0)
            self.canvas.move(self.var_name, 10, 0)
            self.canvas.move(self.val_label, 10, 0)
            self.canvas.update()
            if pos > CANVAS_WIDTH:
                return




