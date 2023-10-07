import customtkinter
import subprocess
import threading
import time
import atexit
import signal
import datetime
import sys

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

root.geometry("700x500")
root.resizable(False, False)
root.title("Relay Control")


def run_command(action, port):
    command = f'CommandApp_USBRelay QAAMZ {action} {port}'
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def off(port):
    run_command("close", port)

def main_switch(port):
    hours = hours_to_set1.get()
    minutes = min_to_set1.get()
    start_in_minutes = spustit_za_min1.get()

    total_minutes = hours * 60 + minutes
    total_seconds1 = total_minutes * 60 + start_in_minutes * 60

    countdown_thread1 = threading.Thread(target=update_countdown_text1, args=(total_seconds1,))
    countdown_thread1.start()
    on_all_thread1 = threading.Thread(target=on_all_thread, args=())
    on_all_thread1.start()

    green_frame1.configure(fg_color="yellow")
    sviti_text1.configure(text="SVITI")


def main_switch2(port):
    hours = hours_to_set2.get()
    minutes = min_to_set2.get()
    start_in_minutes = spustit_za_min2.get()

    total_minutes = hours * 60 + minutes
    total_seconds2 = total_minutes * 60 + start_in_minutes * 60

    countdown_thread2 = threading.Thread(target=update_countdown_text2, args=(total_seconds2,))
    countdown_thread2.start()
    on_all_thread_sec = threading.Thread(target=on_all_thread2, args=())
    on_all_thread_sec.start()

    green_frame2.configure(fg_color="yellow")
    sviti_text2.configure(text="SVITI")

def stop_countdown_and_close_ports():
    global stop_threads1
    global stop_threads2
    stop_threads1 = True
    stop_threads2 = True
    run_command("close", "01")  # Close the first port
    run_command("close", "02")  # Close the second port
    # Add code to close other ports if needed


def on_all_thread():
    run_command("open", "01")
    time.sleep(8)
    run_command("open", "02")  # Zapnout druhý relé
    time.sleep(2)  # Počkat 2 sekundy
    run_command("close", "01")
    time.sleep(1)
    run_command("close", "02")  # Vypnout oba relé

def on_all_thread2():
    run_command("open", "05")
    time.sleep(8)
    run_command("open", "06")  # Zapnout druhý relé
    time.sleep(2)  # Počkat 2 sekundy
    run_command("close", "05")
    time.sleep(1)
    run_command("close", "06")  # Vypnout oba relé

def log_elapsed_time_to_file(elapsed_time, filename="elapsed_time.txt"):
    with open(filename, "a") as file:
        file.write(f"Uplynulo: {elapsed_time} sekund\n{datetime.datetime.now()}\n")  # Opravený zápis

elapsed_time1 = 0
elapsed_time2 = 0

# Globální proměnné pro zastavení časovačů
stop_threads1 = False
stop_threads2 = False

def update_countdown_text1(total_seconds1):
    global elapsed_time1
    global stop_threads1
    while total_seconds1 > 0 and not stop_threads1:
        minutes, seconds = divmod(total_seconds1, 60)
        countdown_text1.configure(text=f"Zbyva: {minutes} minut {seconds} sekund")
        total_seconds1 -= 1
        elapsed_time1 += 1
        time.sleep(1)
    if not stop_threads1:
        countdown_text1.configure(text="Cas vyprsel!")
        green_frame1.configure(fg_color="black")
        sviti_text1.configure(text="")

        log_elapsed_time_to_file(elapsed_time1, "elapsed_time1.txt")

def update_countdown_text2(total_seconds2):
    global elapsed_time2
    global stop_threads2
    while total_seconds2 > 0 and not stop_threads2:
        minutes, seconds = divmod(total_seconds2, 60)
        countdown_text2.configure(text=f"Zbyva: {minutes} minut {seconds} sekund")
        total_seconds2 -= 1
        elapsed_time2 += 1
        time.sleep(1)
    if not stop_threads2:
        countdown_text2.configure(text="Cas vyprsel!")
        green_frame2.configure(fg_color="black")
        sviti_text2.configure(text="")

        log_elapsed_time_to_file(elapsed_time2, "elapsed_time2.txt")

# Funkce pro zastavení časovačů
def stop_countdown1():
    global stop_threads1
    stop_threads1 = True

def stop_countdown2():
    global stop_threads2
    stop_threads2 = True

# Signal handler pro zachycení ukončení aplikace
def handle_exit(signum, frame):
    stop_countdown1()
    stop_countdown2()
    sys.exit(0)

# Registrace signal handleru pro SIGINT (Ctrl+C) a SIGTERM (standardní signál ukončení)
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

#Variables for first room
hours_to_set1 = customtkinter.IntVar()
min_to_set1 = customtkinter.IntVar()
spustit_za_min1 = customtkinter.IntVar()

#Variables for second room
hours_to_set2 = customtkinter.IntVar()
min_to_set2 = customtkinter.IntVar()
spustit_za_min2 = customtkinter.IntVar()

#Initialization of main window
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=10, padx=10, fill="both", expand=True)

#First room control
game_length_label = customtkinter.CTkLabel(master=frame, width=30, height=30, text="DÉLKA HRY - Hala 1", font=("Arial", 20))
game_length_label.grid(row=0, column=0, pady=12, padx=60, sticky="ew")

hours_to_set1_label = customtkinter.CTkLabel(master=frame, width=30, height=30, text="HODINY")
hours_to_set1_label.grid(row=1, column=0)

hours_to_set1_menu = customtkinter.CTkOptionMenu(master=frame, values=["1", "2","3","4","5","6","7","8","9","10","11","12"], width=40, height=10, variable=hours_to_set1)
hours_to_set1_menu.grid(row=2, column=0, pady=(0,25))

min_to_set1_label = customtkinter.CTkLabel(master=frame, width=30, height=30, text="MINUTY")
min_to_set1_label.grid(row=3, column=0)

min_to_set1_menu = customtkinter.CTkOptionMenu(master=frame, values=["5", "10", "15", "20","25", "30", "35", "40", "45"], width=40, height=10, variable=min_to_set1)
min_to_set1_menu.grid(row=4, column=0, pady=(0,25))

game_length_label = customtkinter.CTkLabel(master=frame, width=30, height=30, text="SPUSTIT ZA", font=("Arial", 20))
game_length_label.grid(row=5, column=0, pady=12, padx=10, sticky="ew")

spustit_za_min_menu1 = customtkinter.CTkOptionMenu(master=frame, values=["5 min", "10 min", "15 min", "20 min","25 min", "30 min"], width=40, height=10, variable=spustit_za_min1)
spustit_za_min_menu1.grid(row=6, column=0, pady=(0,25))

countdown_text1 = customtkinter.CTkLabel(master=frame, width=30, height=10, text="Zbyvajici cas", font=("Arial", 15), text_color="White")
countdown_text1.grid(row=8, column=0)

button_zapnout = customtkinter.CTkButton(master=frame, text="ZAPNOUT", fg_color="green", width=70, height=30, command=lambda: main_switch(1))
button_zapnout.grid(row=7, column=0, pady=12, padx=60, sticky="ew")

green_frame1 = customtkinter.CTkFrame(master=frame, fg_color="black", width=50, height=50)
green_frame1.grid(row=9, column=0, pady=12, padx=60, sticky="ew")

sviti_text1 = customtkinter.CTkLabel(master=green_frame1, width=30, height=30, text="", font=("Arial", 20), text_color="black")
sviti_text1.pack(anchor="center")

button_vypnout1 = customtkinter.CTkButton(master=frame, text="VYPNOUT", fg_color="red" ,width=70, height=30, command=stop_countdown_and_close_ports)
button_vypnout1.grid(row=10, column=0, pady=12, padx=60, sticky="ew")

#Second room control
game_length_label2 = customtkinter.CTkLabel(master=frame, width=30, height=30, text="DÉLKA HRY - Hala 2", font=("Arial", 20))
game_length_label2.grid(row=0, column=1, pady=12, padx=60, sticky="ew")

hours_to_set1_label2 = customtkinter.CTkLabel(master=frame, width=30, height=30, text="HODINY")
hours_to_set1_label2.grid(row=1, column=1)

hours_to_set1_menu2 = customtkinter.CTkOptionMenu(master=frame, values=["1", "2","3","4","5","6","7","8","9","10","11","12"], width=40, height=10, variable=hours_to_set2)
hours_to_set1_menu2.grid(row=2, column=1, pady=(0,25))

min_to_set1_label2 = customtkinter.CTkLabel(master=frame, width=30, height=30, text="MINUTY")
min_to_set1_label2.grid(row=3, column=1)

min_to_set1_menu2 = customtkinter.CTkOptionMenu(master=frame, values=["5", "10", "15", "20","25", "30", "35", "40", "45"], width=40, height=10, variable=min_to_set2)
min_to_set1_menu2.grid(row=4, column=1, pady=(0,25))

game_length_label2 = customtkinter.CTkLabel(master=frame, width=30, height=30, text="SPUSTIT ZA", font=("Arial", 20))
game_length_label2.grid(row=5, column=1, pady=12, padx=10, sticky="ew")

spustit_za_min_menu2 = customtkinter.CTkOptionMenu(master=frame, values=["5 min", "10 min", "15 min", "20 min","25 min", "30 min"], width=40, height=10, variable=spustit_za_min2)
spustit_za_min_menu2.grid(row=6, column=1, pady=(0,25))

countdown_text2 = customtkinter.CTkLabel(master=frame, width=30, height=10, text="Zbyvajici cas", font=("Arial", 15), text_color="White")
countdown_text2.grid(row=8, column=1)

button_zapnout2 = customtkinter.CTkButton(master=frame, text="ZAPNOUT", fg_color="green", width=70, height=30, command=lambda: main_switch2(1))
button_zapnout2.grid(row=7, column=1, pady=12, padx=60, sticky="ew")

green_frame2 = customtkinter.CTkFrame(master=frame, fg_color="black", width=50, height=50)
green_frame2.grid(row=9, column=1, pady=12, padx=60, sticky="ew")

sviti_text2 = customtkinter.CTkLabel(master=green_frame2, width=30, height=30, text="", font=("Arial", 20), text_color="black")
sviti_text2.pack(anchor="center")

button_vypnout2 = customtkinter.CTkButton(master=frame, text="VYPNOUT", fg_color="red" ,width=70, height=30, command=lambda: main_switch2(1))
button_vypnout2.grid(row=10, column=1, pady=12, padx=60, sticky="ew")

atexit.register(lambda: log_elapsed_time_to_file(elapsed_time1, "elapsed_time1.txt"))
atexit.register(lambda: log_elapsed_time_to_file(elapsed_time2, "elapsed_time2.txt"))

root.mainloop()