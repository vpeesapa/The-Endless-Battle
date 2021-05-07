#!usr/bin/python3.6

# Dictionaries that stores the button mappings for several controllers
ps4_controller = {
    "x":0,
    "circle":1,
    "square":2,
    "triangle":3,
    "l1":4,
    "r1":5,
    "l2":6,
    "r2":7,
    "share":8,
    "options":9,
    "l3":10,
    "r3":11,
    "ps":12,
    "touchpad":13
}

# 0:left analog horizontal,1:left analog vertical,
# 3: right analog horizontal,4:right analog vertical,
# 2:L2,5:R2
ps4_analog = {
    0:0,
    1:0,
    2:-1,
    3:0,
    4:0,
    5:-1
}

xbox_controller = {
    "a":0,
    "b":1,
    "x":2,
    "y":3,
    "lb":4,
    "rb":5,
    "back":6,
    "start":7,
    "left_press":8,
    "right_press":9,
    "guide":10
}

# 0:left analog horizontal,1:left analog vertical
# 3:right analog horizontal,4:right analog horizontal
# 2:LT,5:RT
xbox_analog = {
    0:0,
    1:0,
    2:-1,
    3:0,
    4:0,
    5:-1
}