# LOCK SCREEN

# check all processes on pc [psutil]
import psutil

# do spmething before pc shut down 
import atexit

import ctypes
#lock screen
#ctypes.windll.user32.LockWorkStation()

# Error message
#ctypes.windll.user32.MessageBoxW(0, u"Error", u"Sup", 3)

# timer
import time

# get foreground window
import win32gui

def get_foreground():
    w = win32gui
    return w.GetWindowText(w.GetForegroundWindow())
    print(w.GetForegroundWindow())
    return w.GetForegroundWindow()


def exit_handler():
    with open('textfile.txt', 'w') as file:
        file.write('done!')
    print('my application is ending!')


def get_apps():
    import subprocess
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if line.rstrip():
            # only print lines that are not empty
            # decode() is necessary to get rid of the binary string (b')
            # rstrip() to remove `\r\n`
            print(line.decode().rstrip())


def timer(time_in_minutes=10):
    while time_in_minutes:
        time.sleep(1)
        time_in_minutes -= 1
    print('Time out!')

def all_processes(pid):
    for proc in psutil.process_iter():
        try:
            #print(f'{proc.name()} ::: {proc.pid}')
            if proc.pid == pid:
                print(proc.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def raw_timer():
    while True:
        time_in_minutes = int(input('Enter time in minutes: '))
        timer(time_in_minutes)
        ctypes.windll.user32.LockWorkStation()

def main():
    # raw_timer()
    #get_apps()

    print(get_foreground())
    all_processes(get_foreground())

    # exit handler
    #atexit.register(exit_handler)
    


if __name__=="__main__":
    main()
