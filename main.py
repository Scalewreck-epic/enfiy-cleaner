import enum
import os
import shutil
import time
import platform
from tkinter import *
from tkinter.ttk import *

system_name = platform.system()
system_version = platform.version()
login = os.getlogin()

user_file = f"C:\\Users\\{login}"
desktop_file = "C:\\Windows"
library_file = "Users\\Library"

useless_files_Windows = [
    f"{user_file}\\AppData\\Local\\Temp",
    f"{user_file}\\AppData\\Local\\Microsoft\\Windows\\Explorer",
    f"{desktop_file}\\Temp",
    f"{desktop_file}\\prefetch",
    f"{desktop_file}\\SoftwareDistribution\\Download",
    f"{desktop_file}\\Logs",
]

useless_files_Mac = [
    f"{library_file}\\Developer\\Xcode\\DerivedData",
    f"{library_file}\\Logs\\CoreSimulator",
    f"{library_file}\\Developer\\Xcode\\iOS DeviceSupport",
    f"{library_file}\\Caches\\com.apple.dt.XCode",
]

sf: int = 0
fr: int = 0
fp: int = 0
total_file_size_KB: int = 0
total_file_size_MB: int = 0
total_file_size_GB: int = 0
total_file_size_TB: int = 0
total_file_size_Bytes: int = 0
wait_time = 0.01
scanning: bool = False
auto_scanning: bool = False
break_auto_scan: bool = True


class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4
    TB = 5


def get_geometry(desired_window, window_x, window_y):
    window_width = desired_window.winfo_width()
    window_height = desired_window.winfo_height()

    monitor_x = (desired_window.winfo_screenwidth() // 2) - (window_width // 2)
    monitor_y = (desired_window.winfo_screenheight() // 2) - (window_height // 2)
    desired_window.resizable(False, False)

    return desired_window.geometry("{}x{}+{}+{}".format(window_x, window_y, monitor_x, monitor_y))


def convert_unit(size_in_bytes, unit):
    divide_rate = 1000

    if unit == SIZE_UNIT.KB:
        return size_in_bytes / divide_rate
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes / (divide_rate * divide_rate)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes / (divide_rate * divide_rate * divide_rate)
    elif unit == SIZE_UNIT.TB:
        return size_in_bytes / (divide_rate * divide_rate * divide_rate * divide_rate)
    else:
        return size_in_bytes


def file_fully_removed(file_size):
    global total_file_size_KB, total_file_size_MB, total_file_size_GB, total_file_size_Bytes, total_file_size_TB, fr
    fr += 1

    tb_size_file = round(convert_unit(file_size, SIZE_UNIT.TB))
    kb_size_file = round(convert_unit(file_size, SIZE_UNIT.KB))
    mb_size_file = round(convert_unit(file_size, SIZE_UNIT.MB))
    gb_size_file = round(convert_unit(file_size, SIZE_UNIT.GB))
    bytes_size_file = round(convert_unit(file_size, SIZE_UNIT.BYTES))

    total_file_size_TB += tb_size_file
    total_file_size_KB += kb_size_file
    total_file_size_MB += mb_size_file
    total_file_size_GB += gb_size_file
    total_file_size_Bytes += bytes_size_file


def delete(path):
    try:
        file_size = os.path.getsize(path)
    except FileNotFoundError:
        return
    except OSError:
        return
    else:
        if os.path.isfile(path) or os.path.islink(path):
            try:
                os.remove(path)
            except OSError:
                return
            else:
                file_fully_removed(file_size)
                return
        elif os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except OSError:
                return
            else:
                file_fully_removed(file_size)
                return
        else:
            print(f"Unknown path link: {path}")
            return


def wait(time_limit, desired_window):
    count = 0

    while count < time_limit:
        desired_window.update()
        count += 0.01
        time.sleep(0.01)


def remove_file_content(file, file_list):
    global sf, fr, total_file_size_KB, total_file_size_GB, total_file_size_MB, total_file_size_Bytes, scanning, fp

    for file_name in file_list:
        wait(wait_time, window)
        file_scanning = f"{file}\\{file_name}"

        delete(file_scanning)
        sf += 1

        fsl_val.set(f"Files Scanned: {str(sf)}")
        frl_val.set(f"Files Removed: {str(fr)}")

        if total_file_size_TB > 0:
            total_file_size_val.set(f"{str(total_file_size_TB)} TB saved")
        if total_file_size_GB > 0 and total_file_size_TB < 1:
            total_file_size_val.set(f"{str(total_file_size_GB)} GB saved")
        if total_file_size_MB > 0 and total_file_size_GB < 1:
            total_file_size_val.set(f"{str(total_file_size_MB)} MB saved")
        if total_file_size_KB > 0 and total_file_size_MB < 1:
            total_file_size_val.set(f"{str(total_file_size_KB)} KB saved")
        if total_file_size_Bytes > 0 and total_file_size_KB < 1:
            total_file_size_val.set(f"{str(total_file_size_Bytes)} Bytes saved")


def scan_pc():
    global sf, fr, total_file_size_KB, total_file_size_GB, total_file_size_MB, total_file_size_Bytes, total_file_size_TB, scanning

    if not scanning:
        scanning = True
        sf = 0
        fr = 0
        total_file_size_KB = 0
        total_file_size_MB = 0
        total_file_size_GB = 0
        total_file_size_TB = 0
        total_file_size_Bytes = 0

        window.update()

        useless_files = None

        if system_name == "Windows":
            useless_files = useless_files_Windows
        elif system_name == "Mac":
            useless_files = useless_files_Mac
        else:
            print(f'{system_name}v{system_version} is not compatible for Enfiy Cleaner.')

        if useless_files:
            for useless_file in useless_files:
                try:
                    file_list = os.listdir(useless_file)
                except FileNotFoundError:
                    print("File Not Found " + useless_file)
                    pass
                except OSError:
                    pass
                else:
                    show_file = Label(window, text=f'Scanning {os.path.basename(useless_file)} File.')
                    show_file.place(x=0, y=0)

                    fsl.place(x=0, y=25)
                    frl.place(x=0, y=50)
                    tfs_v.place(x=0, y=75)

                    remove_file_content(useless_file, file_list)
                    show_file.place_forget()
        else:
            scanning = False

        window.update()

        finished_label = Label(window, text="Scan finished.")
        finished_label.place(x=0, y=0)

        wait(3, window)
        fsl.place_forget()
        frl.place_forget()
        tfs_v.place_forget()
        finished_label.place_forget()

        scanning = False
    else:
        new_window = Tk()
        new_window.iconbitmap(f"favicon.ico")
        new_window.title("Error")
        new_window.resizable(False, False)
        Label(new_window, text="Scan on cooldown.").pack()


def auto_scan():
    global auto_scanning, break_auto_scan

    if not auto_scanning and not scanning:
        break_auto_scan = False
        auto_scanning = False

        warn_window = Toplevel()
        warn_window.title("NOTE")
        warn_window.resizable(False, False)
        warn_window.iconbitmap(f"favicon.ico")
        Label(warn_window, text="Auto scan started").pack()

        while True:
            if break_auto_scan:
                break
            window.update()
            scan_pc()
    else:
        break_auto_scan = True
        auto_scanning = False
        warn_window = Toplevel()

        warn_window.title("NOTE")
        warn_window.resizable(False, False)
        warn_window.iconbitmap(f"favicon.ico")
        Label(warn_window, text="Auto scan ended.").pack()


window = Tk()
get_geometry(window, 250, 250)
window.title("Enfiy Cleaner")
window.iconbitmap(f"favicon.ico")

start_scan = Button(window, text="Start Scan", command=scan_pc)
auto_btn = Button(window, text="Auto Scan", command=auto_scan)

fsl_val = StringVar()
frl_val = StringVar()
total_file_size_val = StringVar()

fsl = Label(window, textvariable=fsl_val)
frl = Label(window, textvariable=frl_val)
tfs_v = Label(window, textvariable=total_file_size_val)

fsl.place_forget()
frl.place_forget()
tfs_v.place_forget()

start_scan.place(x=55, y=220)
auto_btn.place(x=130, y=220)

window.mainloop()
