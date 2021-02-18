import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import os

default_bg = "#D0D0D0"

def set_globals(args):
    global student_file
    global room_file
    student_file = args.student
    room_file = args.seats

def set_student_fname():
    global student_file
    student_file = askopenfilename()

def set_room_fname():
    global room_file
    room_file = askopenfilename()

def update_gui():
    global window
    global student_file
    global room_file

    window.configure(background=default_bg)

    tk.Label(text=os.path.basename(student_file), font=tkFont.Font(size=15), bg=default_bg).grid(row=4, column=1, sticky="W", padx=10)
    tk.Label(text=os.path.basename(room_file), font=tkFont.Font(size=15), bg=default_bg).grid(row=5, column=1, sticky="W", padx=10)

    window.after(1000, update_gui)

def close_gui():
    global window
    window.destroy()

def start_gui(args):
    global window
    set_globals(args)

    window = tk.Tk()
    window.title("LupSeat")

    csv_chart_name = tk.StringVar(value=args.out)
    graphic_chart_name = tk.StringVar(value=args.g_chart)
    graphic_chart_size = tk.StringVar(value=args.g_chart_size)
    graphic_room_name = tk.StringVar(value=args.g_room)
    graphic_room_size = tk.StringVar(value=args.g_room_size)
    format_string = tk.StringVar(value=args.fmt)
    seed = tk.StringVar(value=args.seed)
    algorithm = tk.StringVar(value=args.algorithm)

    tk.Label(text="LupSeat", font=tkFont.Font(size=30), bg=default_bg).grid(row=0, column=0, columnspan=3, padx=30, pady=30)

    tk.Label(text="CSV chart name", font=tkFont.Font(size=15), bg=default_bg).grid(row=1, column=0, padx=10, pady=5, sticky="W")
    tk.Entry(textvariable=csv_chart_name).grid(row=1, column=1)

    tk.Label(text="Graphic chart name/size", font=tkFont.Font(size=15), bg=default_bg).grid(row=2, column=0, padx=10, pady=5, sticky="W")
    tk.Entry(textvariable=graphic_chart_name).grid(row=2, column=1)
    tk.Entry(textvariable=graphic_chart_size).grid(row=2, column=2)

    tk.Label(text="Graphic room name/size", font=tkFont.Font(size=15), bg=default_bg).grid(row=3, column=0, padx=10, pady=5, sticky="W")
    tk.Entry(textvariable=graphic_room_name).grid(row=3, column=1, padx=10)
    tk.Entry(textvariable=graphic_room_size).grid(row=3, column=2, padx=10)

    tk.ttk.Button(text="Set student file", command=set_student_fname).grid(row=4, column=0, padx=10, pady=5, sticky="W")
    tk.ttk.Button(text="Set room layout file", command=set_room_fname).grid(row=5, column=0, padx=10, pady=5, sticky="W")

    tk.Label(text="Format String", font=tkFont.Font(size=15), bg=default_bg).grid(row=6, column=0, padx=10, pady=5, sticky="W")
    tk.Entry(textvariable=format_string).grid(row=6, column=1)

    tk.Label(text="Seed", font=tkFont.Font(size=15), bg=default_bg).grid(row=7, column=0, padx=10, pady=5, sticky="W")
    tk.Entry(textvariable=seed).grid(row=7, column=1)

    tk.Label(window, text="Choose the algorithm:", font=tkFont.Font(size=15), bg=default_bg).grid(row=8, column=0, padx=10, pady=5, sticky="W")
    tk.Radiobutton(window, text="ConsecDivide", variable=algorithm, value="consecdivide", bg=default_bg).grid(row=9, column=0, padx=20, sticky="W")
    tk.Radiobutton(window, text="ChunkIncrease", variable=algorithm, value="chunkincrease", bg=default_bg).grid(row=10, column=0, padx=20, sticky="W")
    tk.Radiobutton(window, text="RandomAssign", variable=algorithm, value="randomassign", bg=default_bg).grid(row=11, column=0, padx=20, sticky="W")

    tk.ttk.Button(text="Run Lupseat", command=close_gui).grid(row=12, column=0, pady=30, columnspan=3)

    update_gui()
    window.mainloop()

    [args.out, args.g_chart, args.g_chart_size, args.g_room, args.g_room_size, args.fmt, args.seed, args.algorithm]= list(map(lambda x: x.get(), 
        [csv_chart_name, graphic_chart_name, graphic_chart_size, graphic_room_name, graphic_room_size, format_string, seed, algorithm]))

    args.student = student_file
    args.seats = room_file

    return args


