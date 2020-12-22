
import os
from fileHandlers import *
from allPurpose import *


def main():
    add_starter_code()
    user = open("input.py", 'r')
    lines = user.readlines()
    original = lines.copy()

    translate_file(lines)
    add_user_code(lines, original)
    add_ending_code()

    user.close()
    os.system("python3 translated.py")


if __name__ == '__main__':
    main()
