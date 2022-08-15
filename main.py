import ctypes
import time
import tkinter as tk


def get_time_window():
    window = tk.Tk()
    window.title('Limit')
    window.geometry('250x100')

    tk_input = tk.Entry()
    tk_input.pack()
    def return_time(event):
        return tk_input.get()
        

    button = tk.Button(text='OK')
    button.bind('<Button-1>',return_time)
    button.pack()

    window.mainloop()
    window.destroy()

def timer(time_in_minutes=10):
    while time_in_minutes:
        time.sleep(1)
        time_in_minutes -= 1
    print('Time out!')


def main():
    print(get_time_window())

    while True:
        time_in_minutes = int(input('Enter time in minutes: '))
        timer(time_in_minutes)
        ctypes.windll.user32.LockWorkStation()


if __name__=="__main__":
    main()
