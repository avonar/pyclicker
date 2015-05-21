#!/usr/bin/python
# -*- coding: utf-8 -*-

import pythoncom
import pyHook
import win32api, win32con
import time
import sys
import random


class mclicker():
    # R and CTRL = start rec
    # S and CTRL = stop rec
    # G and CTRL = start\stop click
    def sleeptime(self, timeout):
        s = timeout - random.uniform(0, 3)
        print s
        if s < 0:
            time.sleep(-s)
        else:
            time.sleep(s)

    def click(self, x,y):
        win32api.SetCursorPos([x, y])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    def OnKeyboardEvent(self, event):
        # проверяем статусы клавиш-модификаторов
        # 0 или 1 - клавиша отжата
        # (-127) или (-128) - клавиша нажата
        ALT     = win32api.GetKeyState(0x12)
        CTRL    = win32api.GetKeyState(0x11)
        G   = win32api.GetKeyState(0x47)
        X    = win32api.GetKeyState(0x58)
        S = win32api.GetKeyState(0x53)
        R = win32api.GetKeyState(0x52)
        MLEFT = win32api.GetKeyState(0x01)
        if R<0 and CTRL<0:
            print "starting rec"
            self.start_rec()
        elif S<0 and CTRL<0:
            print 'stopping rec'
            print self.click_array
            self.stop = True
        elif G<0 and CTRL<0:
            if self.start:
                print "stopping click"
                self.start = False
                self.stop_click = False
            else:
                print "starting click"
                self.stop_click = False
                self.start = True
                self.start_click()
        elif X<0 and CTRL<0:
            sys.exit()
        return True

    def onclick(self, event):
        if not self.stop:
            print win32api.GetCursorPos()
            self.click_array.append((win32api.GetCursorPos(), time.time() - self.start_time))
            self.start_time = time.time()
        return True


    def start_rec(self):
        self.stop = False
        self.click_array = []
        self.start_time = time.time()

    def start_click(self):
        while not self.stop_click:
            for a, b in self.click_array:
                x, y = a
                print x, ' ', y, ' ', b
                self.click(x, y)
                pythoncom.PumpMessages()
                self.sleeptime(b)
                #time.sleep(b)

    def __init__(self):
        print """
        R and CTRL = start rec
        S and CTRL = stop rec
        F and CTRL = start\stop click
        X and CTRL = exit from app
        """
        self.stop = True
        self.start = False
        self.hm = pyHook.HookManager()       # создание экземпляра класса HookManager
        self.hm.KeyAll = self.OnKeyboardEvent     # отслеживаем нажатия клавиш
        self.hm.SubscribeMouseAllButtonsDown(self.onclick)
        self.hm.HookMouse()
        self.hm.HookKeyboard()               # вешаем хук
        pythoncom.PumpMessages()        # ловим сообщения+


mclicker()