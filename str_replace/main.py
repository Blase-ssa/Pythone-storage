#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import json


flag_folder = False
file_array = []
allowed_ext = [".xml", ".txt", ".svg", ".json"]

def get_replcment_list_fron_json(filename) -> dict:
    # check if file exist
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return(json.load(file))
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла {filename}: {e}")

def choose_file() -> None:
    global flag_folder, file_array
    path = filedialog.askopenfilename()
    if path:
        entry_var.set(path)
        flag_folder=False
        file_array = [path]


def choose_folder() -> None:
    global flag_folder, file_array
    path = filedialog.askdirectory()
    if path:
        entry_var.set(path)
        flag_folder=True
        file_array=read_dir(path)


def on_ok() -> None:
    path = entry_var.get()
    if not path:
        messagebox.showwarning("Выбор", "Сначала выберите файл или папку.")
        return
    # Здесь делаем что-то с выбранным путем
    replacer()

    # print("Выбрано:", path)
    root.destroy()

def read_dir(path) -> list:
    global allowed_ext
    result = []

    for f in os.listdir(path):
        full = os.path.join(os.path.normpath(path), f)
        if os.path.isfile(full):
            ext = os.path.splitext(f)[1].lower()
            if ext in allowed_ext:
                result.append(full)

    return result

def line_processor(line) -> str:
    global replcment_list
    for pattern, replacement in replcment_list.items():
        line = re.sub(pattern, replacement, line)
    return(line)

def replacer() -> None:
    global file_array
    for filename in file_array:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                with open(f"{filename}.new", "a", encoding="utf-8") as nf:
                    nf.write(line_processor(line))


replcment_list=get_replcment_list_fron_json("expressions.json")

root = tk.Tk()
root.title("Выбор файла или папки")
root.geometry("400x320")

entry_var = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

info_frame = tk.LabelFrame(frame, text="Описание программы")
info_frame.grid(row=0, column=0, columnspan=3, sticky="we", pady=10)

info_label = tk.Label(info_frame, text=f"Эта программа выбирает файл или папку и обрабатывает файлы. \nСогласно списку регулярных выражений:\n{"\n".join(f"{pattern}  →  {replacement}" for pattern, replacement in replcment_list.items())}")
info_label.pack(fill="both", expand=True, padx=5, pady=5)

entry = tk.Entry(frame, textvariable=entry_var, width=40)
entry.grid(row=1, column=0, columnspan=3, pady=5, sticky="we")

btn_file = tk.Button(frame, text="📄File", command=choose_file)
btn_file.grid(row=2, column=0, padx=5, pady=5)

btn_folder = tk.Button(frame, text="📂 Folder", command=choose_folder)
btn_folder.grid(row=2, column=1, padx=5, pady=5)

btn_ok = tk.Button(frame, text="✅ OK", command=on_ok)
btn_ok.grid(row=2, column=2, padx=5, pady=5)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=0)

root.mainloop()
# print(f"flag_folder = {flag_folder}")
# print(f"file_array = {file_array}")