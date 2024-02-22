import pyautogui
import time

time_1 = time.time()


def move(x, y, button, window, pixels_cell):
    x0, y0 = window.get_location()
    x_m = x0 + x * pixels_cell + pixels_cell // 2
    y_m = y0 + (window.height - y * pixels_cell) - pixels_cell // 2
    key = 'left' if button == 1 else 'right'
    pyautogui.click(x=x_m, y=y_m, duration=0.5, button=key)


def print_time(text=''):
    global time_1
    time_2 = time.time()
    print(time_2 - time_1, text)
    time_1 = time_2
