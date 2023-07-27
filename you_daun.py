from tkinter import *
from tkinter import messagebox
from random import randint
import keyboard
from threading import Thread
import time


def key_exit():
    global flag
    print('нажали')
    flag = False


def start():
    root = Tk()
    root.geometry('600x400')

    button_no = Button(root, text='Нет', font='Arial 20 bold')
    label = Label(root, text='Ты даун?', font='Arial 20 bold', bg='white')
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqwidth()) / 2
    root.wm_geometry('+%d+%d' % (x, y))
    root.title(' ')
    root.resizable(width=False, height=False)
    root['bg'] = 'white'
    label.pack()
    button_no.place(x=170, y=100)
    button_no.bind('<Enter>',
                   lambda x: button_no.place(x=randint(100, 500), y=randint(100, 300)))
    Button(root, text='Да', font='Arial 20 bold',
           command=lambda: [messagebox.showinfo(' ', 'Я так и знал'), exit()]).place(x=350, y=100)
    root.mainloop()


keyboard.add_hotkey('ctrl+esc', key_exit)

if __name__ == '__main__':
    flag = True
    task1 = Thread(target=start)
    task1.start()
    while True:
        if not task1.is_alive() and flag:
            print('Start again')
            task1 = Thread(target=start)
            time.sleep(3)
            task1.start()
        if not flag:
            break
        time.sleep(0.5)
