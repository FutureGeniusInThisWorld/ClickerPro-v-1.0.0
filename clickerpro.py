
from tkinter import *
import threading as th
import time
import ctypes
from tkinter import PhotoImage


try:
    is_running = False
    click_interval = 0
    hotkey_start = "F6"
    hotkey_stop = "F7"
    hotkey_toggle = "F8"


    def mouse_click():
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)


    def click_loop():
        global is_running, click_interval
        while is_running:
            mouse_click()
            if click_interval > 0:
                time.sleep(click_interval)
            else:
                time.sleep(0.001)


    def toggle_clicking(event=None):
        global is_running
        if is_running:
            stop_click_loop()
        else:
            start_clicking()


    def start_clicking(event=None):
        global is_running, click_interval
        if not is_running:
            try:
                interval_str = delay_entry.get()
                if interval_str:
                    click_interval = float(interval_str)
                    if click_interval < 0:
                        click_interval = 0
                else:
                    click_interval = 0
            except:
                click_interval = 0
                delay_entry.delete(0, END)
                delay_entry.insert(0, "0")

            is_running = True
            th.Thread(target=click_loop, daemon=True).start()
            status_label.config(text="Status: RUNNING", fg="green")


    def stop_click_loop(event=None):
        global is_running
        is_running = False
        status_label.config(text="Status: STOPPED", fg="red")


    #окно
    my_win = Tk()
    my_win.title("Auto Clicker")
    my_win.geometry("400x320")
    my_win.config(bg='black')

    try:
        my_win.iconbitmap('a_icon.ico')
        print("Иконка ICO успешно загружена!")
    except Exception as e:
        print(f"Не удалось загрузить ICO иконку: {e}")

        try:
            from tkinter import PhotoImage

            my_icon = PhotoImage(file="icon.png")
            my_win.iconphoto(True, my_icon)
            print("Иконка PNG загружена как fallback")
        except:
            print("Иконка не загружена, будет стандартная")




    #Горячие клавиши
    my_win.bind(f'<{hotkey_start}>', start_clicking)
    my_win.bind(f'<{hotkey_stop}>', stop_click_loop)
    my_win.bind(f'<{hotkey_toggle}>', toggle_clicking)


    Button(my_win, text="START", bg='#2B2B2B', fg='white',
           font=('Consolas', 12, 'bold'), command=start_clicking,
           width=8).place(x=20, y=20)

    Button(my_win, text="STOP", bg='#2B2B2B', fg='white',
           font=('Consolas', 12, 'bold'), command=stop_click_loop,
           width=8).place(x=120, y=20)

    Button(my_win, text='EXIT', bg='#2B2B2B', fg='white',
           font=('Consolas', 12, 'bold'), command=my_win.destroy,
           width=8).place(x=280, y=20)


    delay_entry = Entry(my_win, bg='#2B2B2B', fg='white',
                        font=('Consolas', 10, 'bold'), width=15)
    delay_entry.place(x=200, y=100)
    delay_entry.insert(0, "0")

    Label(my_win, text="Interval (seconds):", bg='black', fg='white',
          font=('Consolas', 10, 'bold')).place(x=30, y=100)

    Label(my_win, text="Enter interval in seconds (e.g., 0.5 for half second)",
          bg='black', fg='gray', font=('Consolas', 8)).place(x=30, y=130)


    status_label = Label(my_win, text="Status: STOPPED", bg='black', fg='red',
                         font=('Consolas', 10, 'bold'))
    status_label.place(x=30, y=180)


    Label(my_win, text=f"Hotkeys: {hotkey_start}=Start, {hotkey_stop}=Stop, {hotkey_toggle}=Toggle",
          bg='black', fg='yellow', font=('Consolas', 9, 'bold')).place(x=30, y=220)

    Label(my_win, text="Note: Hotkeys work only when window is focused",
          bg='black', fg='orange', font=('Consolas', 8)).place(x=30, y=250)

    my_win.focus_force()
    my_win.mainloop()

except Exception:
    pass