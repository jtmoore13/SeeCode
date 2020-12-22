

class Info:

    BIG_VAR_COUNT = 0
    SMALL_VAR_COUNT = 0
    ERROR = False
    TOO_MANY_LINES = False

    FOR_LOOP_COUNT = 0
    for_map = {}

    list_methods = [".append(", ".clear(", ".copy(", ".count(", ".extend(", ".index(", ".insert(", ".pop(", ".remove(",
                    ".reverse(", ".sort("]
    nested_loop_lines = []

    big_vars = []
    small_vars = []
    loop_count = 0
    active_loops = 0

    displayed_lines_map = {}
    curr_line = 0

    adjectives = ["amazing", "wonderful", "genius", "incredible", "marvelous", "awesome", "sensational",
                  "impressive", "remarkable", "brilliant", "spectacular", "phenomenal", "exceptional", "outstanding",
                  "profound"]
    c = 0
    state = 0
    button = 0
    var = 0

    lines_shown = []
    var_names = []