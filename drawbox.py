#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Built on https://tipsfordev.com/printing-extended-ascii-characters-in-python

class TableBorder:
    def __init__ (self, top_left, top_split, top_right,
        mid_left, mid_split, mid_right,
        low_left, low_split, low_right,
        horizontal, vertical, horizontal_up,horizontal_down):
        self.top_left = top_left
        self.top_split = top_split
        self.top_right = top_right
        self.mid_left = mid_left
        self.mid_split = mid_split
        self.mid_right = mid_right
        self.low_left = low_left
        self.low_split = low_split
        self.low_right = low_right
        self.horizontal = horizontal
        self.vertical = vertical
        self.horizontal_up = horizontal_up
        self.horizontal_down = horizontal_down

Borders0 = TableBorder ('+', '+', '+', '+', '+', '+', '+', '+', '+', '-', '|','+','+')
Borders1 = TableBorder (u'\u250c',u'\u252C',u'\u2510',u'\u251C',u'\u253C',u'\u2524',u'\u2514',u'\u2534',u'\u2518',u'\u2500',u'\u2502',u'\u2534',u'\u252c')
Borders2 = TableBorder (u'\u2554',u'\u2566',u'\u2557',u'\u2560',u'\u256C',u'\u2563',u'\u255a',u'\u2569',u'\u255d',u'\u2550',u'\u2551',u'\u2569',u'\u2566')

def draw_box (width:int, height:int, box:TableBorder):
    span = width-2
    line = box.horizontal * (span)
    print (box.top_left + line + box.top_right)
    body = box.vertical + (' '*span) + box.vertical
    for _ in range (height-1):
        print (body)
    print (box.low_left + line + box.low_right)
    
def draw_table (rows:int, cols:int, has_header:bool, box:TableBorder):
    span = (cols * 2) -1
    if has_header:
    # Table header 
        print (box.top_left + (box.horizontal * span) + box.top_right) # TOP Line 
        print(box.vertical + (' '*span) + box.vertical) #Header Body
        print(box.mid_left,end='') # Header bottom start
        for _ in range (cols-1):
            print(box.horizontal + box.horizontal_down,end='') # Header bottom
        print(box.horizontal,end='') # Header last bottom
        print(box.mid_right) # Header bottom end
    else:
        # Table Top no header
        print(box.top_left,end='') # Header bottom start
        for _ in range (cols-1):
            print(box.horizontal + box.horizontal_down,end='') # Header bottom
        print(box.horizontal,end='') # Header last bottom
        print(box.top_right) # Header bottom end
    
    # Table Cells
    for _ in range (rows-1):
        print(box.vertical,end='')
        for _ in range (cols-1):
            print(' '+box.vertical,end='')
        print(' ' + box.vertical)
        
        print(box.mid_left,end='')
        for _ in range (cols-1):
            print(box.horizontal + box.mid_split,end='')
        print(box.horizontal + box.mid_right)
    
    # Table last cell Row
    print(box.vertical,end='')
    for _ in range (cols-1):
        print(' '+box.vertical,end='')
    print(' ' + box.vertical)
    
    # Table last line
    print(box.low_left,end='') # bottom start
    for _ in range (cols-1):
        print(box.horizontal + box.horizontal_up,end='') # bottom
    print(box.horizontal,end='') # last bottom
    print(box.low_right) # bottom end
    
    
def draw_menu (rows:int, width:int, box:TableBorder):
    span = width
    line = box.horizontal * (span)
    print (box.top_left + line + box.top_right)
    body = box.vertical + (' '*span) + box.vertical
    seperator = box.mid_left + (box.horizontal*span) + box.mid_right
    for _ in range (rows-1):
        print (body)
        print (seperator)
    print (body)
    print (box.low_left + line + box.low_right)

#draw_menu (4, 2, Borders1)