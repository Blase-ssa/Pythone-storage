#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import json
import sys
import subprocess


flag_folder = False
file_array = []
allowed_ext = [".xml", ".txt", ".svg", ".json"]
replcment_list = {}
DEFAULT_EXPRESSIONS = "expressions.json"


def app_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_replcment_list_fron_json(filename) -> dict:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла {filename}: {e}")
    if not isinstance(data, dict):
        raise RuntimeError(f"Файл {filename} должен содержать JSON-объект (словарь).")
    return data


def load_expressions(filename) -> None:
    global replcment_list
    replcment_list = get_replcment_list_fron_json(filename)
    expressions_status_var.set(f"Загружено правил: {len(replcment_list)}")


def choose_expressions() -> None:
    path = filedialog.askopenfilename(
        title="Файл со списком регулярных выражений",
        filetypes=[("JSON", "*.json"), ("Все файлы", "*.*")],
        initialdir=app_dir(),
    )
    if path:
        expressions_var.set(path)
        try:
            load_expressions(path)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


def open_expressions_editor() -> None:
    path = expressions_var.get()
    if not path:
        messagebox.showwarning("Выражения", "Сначала выберите файл со списком регулярных выражений.")
        return
    if not os.path.isfile(path):
        messagebox.showwarning("Выражения", f"Файл не найден:\n{path}")
        return
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть файл в редакторе:\n{e}")


def choose_file() -> None:
    global flag_folder, file_array
    path = filedialog.askopenfilename()
    if path:
        entry_var.set(path)
        flag_folder = False
        file_array = [path]


def choose_folder() -> None:
    global flag_folder, file_array
    path = filedialog.askdirectory()
    if path:
        entry_var.set(path)
        flag_folder = True
        file_array = read_dir(path)


def on_ok() -> None:
    path = entry_var.get()
    if not path:
        messagebox.showwarning("Выбор", "Сначала выберите файл или папку.")
        return
    expr_path = expressions_var.get()
    if not expr_path:
        messagebox.showwarning("Выражения", "Сначала выберите файл со списком регулярных выражений.")
        return
    try:
        load_expressions(expr_path)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
        return
    try:
        processed = replacer()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
        return
    messagebox.showinfo("Готово", f"Обработка завершена.\nФайлов: {processed}")


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
    return line


def replacer() -> int:
    global file_array
    for filename in file_array:
        with open(filename, "r", encoding="utf-8") as file:
            with open(f"{filename}.new", "w", encoding="utf-8") as nf:
                for line in file:
                    nf.write(line_processor(line))
    return len(file_array)


root = tk.Tk()
root.title("Выбор файла или папки")
root.geometry("520x280")

entry_var = tk.StringVar()
expressions_var = tk.StringVar(value=os.path.join(app_dir(), DEFAULT_EXPRESSIONS))
expressions_status_var = tk.StringVar(value="")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

info_frame = tk.LabelFrame(frame, text="Описание программы")
info_frame.grid(row=0, column=0, columnspan=3, sticky="we", pady=(0, 10))

info_label = tk.Label(
    info_frame,
    text="Программа обрабатывает выбранный файл или файлы в папке\n"
    "по списку регулярных выражений из JSON-файла.",
    justify="left",
)
info_label.pack(fill="both", expand=True, padx=5, pady=5)

tk.Label(frame, text="Список выражений:").grid(row=1, column=0, sticky="w")
expr_entry = tk.Entry(frame, textvariable=expressions_var)
expr_entry.grid(row=2, column=0, columnspan=3, pady=5, sticky="we")

btn_expr = tk.Button(frame, text="📋 JSON", command=choose_expressions)
btn_expr.grid(row=3, column=0, padx=5, pady=5, sticky="w")

btn_edit = tk.Button(frame, text="✎ Открыть", command=open_expressions_editor)
btn_edit.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame, textvariable=expressions_status_var, fg="#444").grid(
    row=3, column=2, padx=5, pady=5, sticky="e"
)

tk.Label(frame, text="Файл или папка:").grid(row=4, column=0, sticky="w", pady=(10, 0))
entry = tk.Entry(frame, textvariable=entry_var)
entry.grid(row=5, column=0, columnspan=3, pady=5, sticky="we")

btn_file = tk.Button(frame, text="📄 File", command=choose_file)
btn_file.grid(row=6, column=0, padx=5, pady=5)

btn_folder = tk.Button(frame, text="📂 Folder", command=choose_folder)
btn_folder.grid(row=6, column=1, padx=5, pady=5)

btn_ok = tk.Button(frame, text="✅ OK", command=on_ok)
btn_ok.grid(row=6, column=2, padx=5, pady=5)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=0)

default_expr = expressions_var.get()
if os.path.isfile(default_expr):
    try:
        load_expressions(default_expr)
    except Exception:
        expressions_status_var.set("Не удалось загрузить expressions.json")
else:
    expressions_status_var.set("Файл выражений не выбран")

root.mainloop()
