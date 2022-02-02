#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Wordly game by Christofer Tibbelin
import os
import time
from dataclasses import dataclass
from typing import List
from random import randint
from getch import *
from drawbox import *

escape_ansi = '\033['
escape_utf = '\u001b['
escape_char = escape_utf
color_reset = f"{escape_char}0m"

retries_allowed = 6

class Color:
    f_red = '31'
    f_green = '32'
    f_blue = '34'
    f_purple = '35'
    f_gray = '90'
    f_white = '37'
    b_red = '41'
    b_green = '42'
    b_blue = '44'
    b_purple = '45'
    b_gray = '100'

rainbow = ['31','32','33','34','35','36']

alphabet ="abcdefghijklmnopqrstuvxyz"
qwerty = [
    ['q','w','e','r','t','y','u','i','o','p'],
    ['a','s','d','f','g','h','j','k','l'],
    ['z','x','c','v','b','n','m']
 ]

word_lists = [
    [4,'4 letter hard!', 'words/4_letters_master.txt'],
    [5,'5 letter simple', 'words/5_letters_simple.txt'],
    [5,'5 letter medium', 'words/5_letters_medium.txt'],
    [5,'5 letter hard!', 'words/5_letters_master.txt'],
    [6,'6 letter medium', 'words/6_letters_medium.txt'],
    [6,'6 letter hard!', 'words/6_letters_master.txt'],
    [7,'7 letter hard!', 'words/7_letters_master.txt']
    ]

master_lists = {
    4:'words/4_letters_master.txt',
    5:'words/5_letters_master.txt',
    6:'words/6_letters_master.txt',
    7:'words/7_letters_master.txt'
}


# Pos keyboard
keyb_line_start = 6
keyb_column_start = 10

table_row_start = 4
table_col_start = 2

def print_rainbow(text:str,is_bold:bool=True,end:bool=True)->None:
    i = 0
    for char in text:
        print(f"{escape_char}{1 if is_bold else 0};{rainbow[i]}m{char}{color_reset}",end='')
        if char != ' ':
            i+=1
        if i >= len(rainbow):
            i = 0
    print('')
  
def printc(color:str,text:str,is_bold:bool=True,end:bool=True)->None:
    print(f"{escape_char}{1 if is_bold else 0};{color}m{text}{color_reset}",end=('\n' if end else ''))
    
def printp(text:str,line:int,column:int,is_bold:bool=True,end:bool=True)->None:
    print(f"{escape_char}{str(line)};{str(column)}H{text}",end=('\n' if end else ''))

def printcp(color:str,text:str,line:int,column:int,is_bold:bool=True,end:bool=True)->None:
    print(f"{escape_char}{str(line)};{str(column)}H{escape_char}{1 if is_bold else 0};{color}m{text}{color_reset}",end=('\n' if end else ''))

def move_home():
    print(f"{escape_char}H",end='')

def move_console(line:int,column:int):
    print(f"{escape_char}{str(line)};{str(column)}H",end='')

def del_line():
    print(f"{escape_char}J",end='')

@dataclass
class Player:
    """[a instance of a player]
    """    
    def __init__(self, name: str):
        self.name = name
        self.total_score: int = 0

    def __repr__(self) -> str:
        return self.name


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def normalize(string: str) -> str:
    """[removes spaces and stuff in string]

    Args:
        string (str): [any string]

    Returns:
        str: [string without spaces or -_]
    """    
    string = string.replace(' ', '')
    string = string.replace('-', '')
    string = string.replace('_', '')
    return string.lower()


def process_file(filename:str) ->List[str]:
    try:
        with open(filename, "r") as f:
            word_list = [line.rstrip() for line in f]
        f.close()
        return word_list
    except IOError: 
        print("Error: File does not appear to exist.")
        return []


def convert_to_list(string:str) -> List[str]:
    string2 = normalize(string)
    return [a for a in str(string2)]

def print_welcome():
    cls()
    move_home()
    draw_menu(3,11,Borders1)
    move_console(2,4)
    print("Welcome")
    move_console(4,6)
    print("To")
    move_console(6,4)
    print_rainbow("Wordley")
    move_console(8,0)
    time.sleep(2.0)


def print_menu() -> int:
    cls()
    move_home()
    print("Select difficulty with ",end='')
    printc(Color.b_gray,'Up',True,False)
    print(" and ",end='')
    printc(Color.b_gray,'Down',True,False)
    print(" Arrows.")
    print("Press Enter to accept:")
    draw_menu(len(word_lists),17,Borders1)
    select_row = 0
    key_input = ''
    while (key_input != '\n' and key_input != '\r'):
        for i, difficulty in enumerate(word_lists):
            move_console(4+(i*2),3)
            if i == select_row: printc(Color.b_gray,difficulty[1])
            else: print(difficulty[1])
        move_console(2,23)
        key_input = getArrow()
        if key_input == 'up': select_row -= 1
        elif key_input == 'down': select_row += 1
        if select_row > len(word_lists)-1: select_row = 0
        elif select_row < 0: select_row = len(word_lists)-1
    return select_row


def print_keyboard(line,column):
    for row in qwerty:
        move_console(line,column)
        line += 1
        column += 1
        for char in row:
            printc(Color.b_gray,' '+char.upper()+' ',True,False)
            print(' ',end='')
        print('')

def print_table_key(text:bytes):
    printc(Color.f_white,text.upper(),True,False)


def color_qwerty(chars:List[str], correct:List[str]):
    for i, char in enumerate(chars):
        for x, row in enumerate(qwerty):
            if char in row:
                index = row.index(char)
                line = keyb_line_start + x
                column = keyb_column_start + (index * 4) + x + len(correct)
                move_console(line,column)
                if char == correct[i]: color = Color.b_green
                elif char in correct: color = Color.b_blue
                else: color = Color.f_white
                printc(color,' '+char.upper()+' ',True,False)

def move_table(row,col):
    curr_row = table_row_start+(row*2)
    curr_col = table_col_start+(col*2)
    move_console(curr_row,curr_col)

def color_table(user_word:List[str],selected_word_list:List[str],table_row:int):
    table_col = 0
    for i, char in enumerate(user_word):
        move_table(table_row,table_col)
        if char == selected_word_list[i]: color = Color.b_green
        elif char in selected_word_list: color = Color.b_blue
        else: color = Color.f_gray
        printc(color,char.upper(),True,False)
        table_col+=1       
    table_row +=1
    color_qwerty(user_word,selected_word_list)

def main():
    print_welcome()
    dict_number = print_menu()
    selected_dictionary = process_file(word_lists[dict_number][2])
    selected_word = selected_dictionary[randint(0,len(selected_dictionary))].lower()
    selected_word_list = convert_to_list(selected_word)
    word_lenght = word_lists[dict_number][0]
    master_list = process_file(master_lists[word_lenght])
    cls()
    draw_table(retries_allowed,word_lenght,True,Borders1)
    move_console(2,2 + (word_lenght-4))
    print_rainbow("Wordly")
    print_keyboard(keyb_line_start,keyb_column_start+word_lenght)
    user_word:List[str] = []
    table_row = 0
    table_col = 0
    while(1):
        move_table(table_row,table_col)
        keypress = getch()
        try:
            string_keypress = keypress.decode('utf8')
        except:
            string_keypress = ''
        if keypress == b'\x08': #Backspace
            if table_col == 0:    
                print(' ',end='')
                user_word = []
            elif table_col == word_lenght-1:
                if len(user_word) == word_lenght:
                    user_word.pop()
                print(' ',end='')
                table_col -= 1
                move_table(table_row,table_col)
                print(' ',end='')
                user_word.pop()
            elif table_col > 0 and table_col < word_lenght-1:
                if table_col <= len(user_word) - 1:
                    user_word.pop()
                print(' ',end='')
                table_col -= 1
                move_table(table_row,table_col)
                print(' ',end='')
                user_word.pop()
        elif keypress == b'\n' or keypress == b'\r':
            if len(user_word) == word_lenght:
                test_word = ''.join(user_word).lower()
                if test_word.casefold() in (word.casefold() for word in master_list):
                    if user_word == selected_word_list:
                        color_table(user_word,selected_word_list,table_row)                         
                        move_console(4,word_lenght + 10)
                        print("Correct Guess!!")
                        break
                    if table_row < retries_allowed-1:
                        color_table(user_word,selected_word_list,table_row)
                        table_col = 0
                        table_row += 1
                        test_word = ''
                        user_word = []
                    else:
                        color_table(user_word,selected_word_list,table_row)
                        move_console(3,word_lenght + 10)
                        printc(Color.f_red,"Sorry you Lost",True,False)
                        move_console(4,word_lenght + 10)
                        printc(Color.f_white,"The word was: ",True,False)
                        printc(Color.b_purple,selected_word.upper(),True,False)
                        break
                else:
                    move_console(4,word_lenght + 10)
                    print("Word don't exist")
                    time.sleep(1.0)
                    move_console(4,word_lenght + 10)
                    print("                ")
        elif keypress == b'\x1b': #Escape
            move_console(3,word_lenght + 10)
            printc(Color.f_red,"Sorry you Lost",True,False)
            move_console(4,word_lenght + 10)
            printc(Color.f_white,"The word was: ",True,False)
            printc(Color.b_purple,selected_word.upper(),True,False)
            break
        elif string_keypress.isalpha():
            if table_col <= word_lenght-1:
                if len(user_word) < word_lenght:
                    print_table_key(string_keypress)
                    user_word.append(string_keypress.lower())
            if table_col < word_lenght-1:
                table_col += 1
                move_table(table_row,table_col)
                
    move_console(retries_allowed * 3,0)

    



if __name__ == "__main__":
    main()
