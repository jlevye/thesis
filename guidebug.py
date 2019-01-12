import easygui
import sys
option = easygui.choicebox(choices = ("A","B","C"))

if option is None:
    print("choose something!")
    sys.exit()
else:
    toggle = option

if toggle is "A":
    print("you picked the first thing")
elif toggle is "B":
    print("You picked the second thing")
else:
    print("You picked something else")
