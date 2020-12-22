

# canvas dimensions
CANVAS_WIDTH = 1400
CANVAS_HEIGHT = 750


# small variable box dimensions based on the variable section x-value
VAR_SECTION_X = CANVAS_WIDTH - 175      # [CONTROL]   # x-value of where the dashed line separates the small variables
SIDE_WIDTH = (CANVAS_WIDTH-VAR_SECTION_X) * .85     # width of the small variable box
SIDE_HEIGHT = SIDE_WIDTH/2                            # height of the small variable box
CORNER_SQUARE_X = VAR_SECTION_X + .1125*SIDE_WIDTH    # where the small variable box starts on the x-axis


CODE_SECTION_X = int(CANVAS_WIDTH*.75)


# the max font sizes that each font can be
FONT_SIZE = 30                                # [CONTROL]      # starting font size of a big variable
INDEX_FONT_SIZE = FONT_SIZE//2                                 # font size of the indexes
VAR_NAME_FONT_SIZE = int(SIDE_WIDTH*.16)                       # font size of a small variable name
VAR_VAL_FONT_SIZE = int(SIDE_WIDTH/4)                          # initial font size of a small variable value
FOR_LOOP_VAL_SIZE = 15
FOR_LOOP_FONT_SIZE = 20


# big variable location/dimensions
GAP = FONT_SIZE*3.4                       # vertical distance between adjacent big variables
CONTAINER_SECTION_Y = CANVAS_HEIGHT*.45
START_X = 175                             # x-value of where the big variable data starts
START_Y = CONTAINER_SECTION_Y + GAP*.8    # y-value of initial big variable text
CHAR_LEN = FONT_SIZE/1.7                  # pixel-length of one character
OFFSET_Y = FONT_SIZE*1.25                 # vertical distance between index label and index value
VAR_SECTION_Y = CONTAINER_SECTION_Y       # where the first small variable box is on the y-axis


# for loop grid information
FOR_START_X = 250
FOR_START_Y = 75
BOX_HEIGHT = 60                  # [CONTROL]
BOX_WIDTH = 1.6*BOX_HEIGHT
FOR_GAP = BOX_HEIGHT*1.4         # vertical distance between nested for-loops
FOR_OFFSET = BOX_WIDTH           # horizontal difference between starting points of nested for-loops
FOR_LOOP_PRESENT = True          # list animations go quicker if there is a for loop involved

# font colors
BACKGROUND = 'black'
HIGHLIGHT = 'yellow'
SEARCH_COLOR = 'yellow'          # Finder search bar color
DEFAULT = 'white'                # default text color
VAR_COLOR = 'PaleTurquoise1'     # variable name color
ARROW_COLOR = 'PaleGreen1'       # color of flashing arrows
ERROR_FONT_COLOR = 'firebrick1'      # color of error message
SEGFAULT_COLOR = 'red'           # color that errors from pop(), etc. illuminate at the out-of-bound index
GRID_COLOR = 'gray55'            # color for the for loop grids
TRACKER_COLOR = 'white'          # color of the line that tracks nested for loop paths
SMALL_VAR_FRAME_COLOR = 'white'  # color of the small variable box frame
FOR_LOOP_VAR_COLOR = VAR_COLOR


# animation speed
ULTRA = .15
FAST = .25
MEDIUM = .75
SLOW = 1.25
ARE_YOU_KIDDING_ME = 1.75
SPEED = MEDIUM             # [CONTROL]

FOR_LOOP_SPEED = 1.6/FAST       # [CONTROL]


# animation preferences
APPEND = True
COUNT = True
EXTEND = True
INDEX = True
INSERT = True
POP = True
REMOVE = True

FLASH = 1         # constant for a small variable to flash its name upon instantiation
NO_FLASH = 0      # won't flash upon instantiation


# error values
ERROR_SECTION_Y = CANVAS_HEIGHT-65
NOT_IN_LIST = 888
MIN_FONT_SIZE = 15

