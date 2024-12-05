from Processor import Calculations
import tkinter as tk
from tkinter import ttk


def prepare_tables(input_data, divider):
    size = len(input_data['rods']) + 1
    tables = [[] for _ in range(size)]
    rods = input_data['rods']
    deltas = Calculations.find_deltas(input_data)

    for rod in rods:
        rod_num = int(rod['point1'])

        l = float(input_data['points'][rod_num])
        delta_0, delta_l = deltas[rod_num - 1], deltas[rod_num]

        e_val = float(rod['e'])
        a_val = float(rod['a'])
        q_val = 0
        for load in input_data['dist_loads']:
            if int(load['rod']) == rod_num:
                q_val = float(load['val'])


        for i in range(divider + 1):
            x_ = round(l / divider * i, 4)
            n_val = Calculations.find_n(x_, delta_0, delta_l, l, q_val, e_val, a_val)
            u_val = Calculations.find_u(x_, delta_0, delta_l, l, q_val, e_val, a_val)
            sigma_val = Calculations.find_sigma(n_val, a_val)

            pred_sigma = float(rod['sigma'])
            tables[rod_num].append((x_, n_val, u_val, sigma_val, pred_sigma))

    del tables[0]

    return tables


def create_notebook_with_tables(data):
    notebook_window = tk.Toplevel()
    notebook_window.title("Расчетные таблицы")
    notebook_window.geometry("410x275")
    notebook_window.resizable(False, False)

    notebook = ttk.Notebook(notebook_window)
    notebook.pack(fill="both", expand=True)

    for index, table_data in enumerate(data):
        frame = ttk.Frame(notebook)
        treeview = ttk.Treeview(frame, columns=("x", "N(x)", "U(x)", "σ(x)", "[σ]"), show="headings", height=11)
        treeview.grid(row=0, column=0, sticky="nsew")

        treeview.column("x", width=80, anchor="center")
        treeview.column("N(x)", width=80, anchor="center")
        treeview.column("U(x)", width=80, anchor="center")
        treeview.column("σ(x)", width=80, anchor="center")
        treeview.column("[σ]", width=80, anchor="center")

        treeview.heading("x", text="x")
        treeview.heading("N(x)", text="N(x)")
        treeview.heading("U(x)", text="U(x)")
        treeview.heading("σ(x)", text="σ(x)")
        treeview.heading("[σ]", text="[σ]")

        treeview.tag_configure('orange', foreground='orange')

        for row in table_data:
            if abs(row[-2]) > row[-1]:
                treeview.insert("", "end", values=row, tags=("orange",))
            else:
                treeview.insert("", "end", values=row)

        notebook.add(frame, text=f"Таблица {index + 1}")
