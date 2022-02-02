#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Built on code from https://stackoverflow.com/users/355230/martineau 

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        test = msvcrt.getch()
        if test == b'\x00' or test == b'\xe0':
            test += msvcrt.getch()
        return test

def getArrow()-> str:
    inkey = _Getch()
    escape = False
    while(1):
        k=inkey()
        if escape == True:
            if k==b'H':
                    return 'up'
            elif k==b'P':
                    return 'down'
        if k==b'\xe0': escape = True
        elif k==b'\x00': escape = True
        elif k==b'\x00P': return 'down'
        elif k==b'\x00H': return 'up'
        elif k==b'\n':
            return '\n'
        elif k==b'\r':
            return '\n'


getch = _Getch()