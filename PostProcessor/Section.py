import tkinter as tk
from tkinter import ttk, messagebox
from Processor import Calculations
from Preprocessor import Checkers


def create_section_window(input_data):

    def find_section(rod_num_entry, rod_x_entry, section_table):

        temp_rod_num = rod_num_entry.get()
        if temp_rod_num == "":
            messagebox.showerror("Ошибка ввода", f"Введите корректный номер стержня [1-{len(input_data['rods'])}]")
            return

        temp_rod_x = rod_x_entry.get()
        if temp_rod_x == "":
            messagebox.showerror("Ошибка ввода",
                                 f"Введите корректную координату стержня [0; {input_data['points'][int(temp_rod_num)]}]")
            return

        rod_num = int(rod_num_entry.get())
        rod_x = float(rod_x_entry.get())

        if len(input_data['rods']) < rod_num:
            messagebox.showerror("Ошибка ввода", f"Введите корректный номер стержня [1-{len(input_data['rods'])}]")
            return

        if rod_x > float(input_data['points'][rod_num]):
            messagebox.showerror("Ошибка ввода", f"Введите корректную координату стержня [0-{input_data['points'][rod_num]}]")
            return



        section_u, section_n, section_sigma = Calculations.find_section(input_data, rod_num, rod_x)

        section_table.tag_configure('orange', foreground='orange')

        for item in section_table.get_children():
            section_table.delete(item)

        rod_sigma = float([rod['sigma'] for rod in input_data['rods'] if rod_num == int(rod['point1'])][0])

        if section_sigma > rod_sigma:
            section_table.insert("", "end", values=(section_u, section_n, section_sigma), tags="orange")
        else:
            section_table.insert("", "end", values=(section_u, section_n, section_sigma))

    section_window = tk.Toplevel()

    section_window.title('Сечение')
    section_window.geometry('300x130')
    section_window.resizable(False, False)

    section_frame = tk.Frame(section_window)
    section_frame.pack()

    rod_num_label = tk.Label(section_frame, text="№ стержня: ")
    rod_num_label.grid(row=0, column=0, sticky='w')

    validate_rod_num_cmd = section_frame.register(Checkers.npn_checker)
    rod_num_entry = tk.Entry(section_frame, width=10, validate="all", validatecommand=(validate_rod_num_cmd, '%P'))
    rod_num_entry.grid(row=0, column=1, sticky='w')

    rod_x_label = tk.Label(section_frame, text="Координата: ")
    rod_x_label.grid(row=0, column=2, sticky='e', padx=(10, 0))

    validate_rod_x_cmd = section_frame.register(Checkers.rpn_checker)
    rod_x_entry = tk.Entry(section_frame, width=10, validate="all", validatecommand=(validate_rod_x_cmd, '%P'))
    rod_x_entry.grid(row=0, column=3, sticky='w')

    calc_button = ttk.Button(section_frame, text="Расчет", width=20, command=lambda: find_section(rod_num_entry, rod_x_entry, section_table))
    calc_button.grid(row=1, column=0, columnspan=4, pady=(20, 5))

    section_table = ttk.Treeview(section_frame, columns=("N(x)", "U(x)", "σ(x)"), show="headings", height=1)
    section_table.grid(row=2, column=0, columnspan=4)

    section_table.heading("N(x)", text="N(x)")
    section_table.heading("U(x)", text="U(x)")
    section_table.heading("σ(x)", text="σ(x)")

    section_table.column("N(x)", width=90, anchor="center")
    section_table.column("U(x)", width=90, anchor="center")
    section_table.column("σ(x)", width=90, anchor="center")
