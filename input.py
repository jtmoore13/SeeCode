
# Welcome to SeeCode!

# SeeCode is a tool that helps beginning Python programmers visualize what their code is doing.

# SeeCode supports animations for a variety of simple Python code, such as:

#   - list methods
#       - .append(), .clear(), .copy(), .count(), .extend(), .index(), .insert(), .pop(), .remove(), .reverse(), .sort()
#           - please note that animations for these methods are only shown when called directly, and not
#             passed in as a parameter, or on the right side of an expression

#           - WILL show animation:
#               - words.pop(1)
#               - fruits.index("banana")
#           - will NOT show animation:
#               - last_word = words.pop()
#               - num = nums.pop(nums.index(1))
#               - apple_index += fruits.index("apple")
#
#   - variable declarations of types: list, int, float, str, bool
#   - changing or updating any variable

#   - for loops (range and each) and while loops
#       - up to 3 nested loops
#       - break statements
#
#   - if/elif/else statements


# Attempts to do the following will likely result in a crash or inaccurate animations:
#       - make functions
#       - return values
#       - use of lambda
#       - I/o streams
#       - opening/reading/writing files
#       - images
#       - error catching/exceptions


# Note that syntax errors will cause the program to crash immediately.
# Coding that causes errors such as segfaults, etc. will be caught and displayed on the screen.


# Simply type your code in the proper place below, and run the program. A window displaying your code
# should pop up. You can pause and play the animations via the buttons in the top-right of the window.
# When you are finished, just exit out of the window or stop the program to re-enter more code.


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# --------------- # TYPE YOUR CODE BELOW # ---------------- #


# --------------------------------------------------------- #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


# There are examples of several example programs below that you can un-comment and run!


# --------------------- EXAMPLES --------------------- #


# # 1) basic list methods
# words = []
# words.append("hello")
# words.append("world")
# words.extend("python")
# words.pop()
# words.pop(2)
# words.index("world")
# words.reverse()
# words.sort()
# words.insert(1, "inserted!")


# # 2) basic range loop with if-statement
# for i in range(4):
#     print(i)
#     if i == 2:
#         print("yay, i = 2")


# # 3) basic while loop
# i = 0
# i_values = []
# while i < 5:
#     i_values.append(i)
#     i += 1


# # 4) nested for-each loops
# fruits = ["apple", "plum", "grape", "banana", "peach"]
# for fruit in fruits:
#     for char in fruit:
#         print(char)


# # 5) counting number of 'l's
# l_count = 0
# for char in reversed("hello"):
#     if char == "l":
#         l_count += 1


# # 5) find max and min of a list of numbers
# nums = [10, -4, 200, -57, 2, 0]
# biggest = nums[0]
# smallest = nums[0]
#
# for i in range(len(nums)):
#     if nums[i] > biggest:
#         biggest = nums[i]
#     elif nums[i] < smallest:
#         smallest = nums[i]
# print("Smallest =", smallest)
# print("Biggest =", biggest)


# # 6) Changing values in a list
# words = ["hi", "hey", "hello"]
# words[0] = "HI!!!"
# words[1] = "HEY!!!"
# words[2] = "HELLO!!!"


# ------------------ EXAMPLE ERRORS ------------------ #


# # 7) Pop invalid index
# words = ["hi", "hey", "hello"]
# words.pop(len(words))


# # 8) Popping invalid index of a shrinking list
# words = ["hi", "hey", "hello"]
# for i in range(len(words)):
#     words.pop(i)


# # 9) Adding different types together
# word = 4
# word += "hi"


# # 10) Trying to change index that does not exist
# words = ["hi", "hey", "hello"]
# words[0] = "HI!!!"
# words[8] = "HEY!!!"
# words[2] = "HELLO!!!"


# # 11) List of lists indexing error
# two = [[1, 2], [2, 4]]
# two[0][1] = 10
# two[0][2] = 59


# # 12) For loop going too far
# listy = [1,2,3]
# for i in range(len(listy)+1):
#     if listy[i] == 2:
#         print(2)


