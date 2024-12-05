import json
import tkinter as tk
from tkinter import ttk
from collections import defaultdict
from tkinter import filedialog

from Preprocessor import Sheme, Checkers
from PostProcessor import Tables, Plots, Report, Section



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Конструкция")
        self.geometry("1510x600")
        self.resizable(False, False)
        self.node_rows = []
        self.bar_rows = []
        self.point_load_rows = []
        self.distributed_load_rows = []


        self.npn_checker = self.register(Checkers.npn_checker)
        self.rpn_checker = self.register(Checkers.rpn_checker)
        self.rn_checker = self.register(Checkers.rn_checker)

        self.user_data = defaultdict(list)

        self.create_widgets()

    def create_widgets(self):
        self.create_menu()
        self.create_frames()

    def create_menu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Загрузить", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Очистить", command=self.clear_input)
        file_menu.add_separator()
        file_menu.add_command(label="Выйти", command=self.close)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        postproc_menu = tk.Menu(menu_bar, tearoff=0)

        postproc_menu.add_command(label="Сечение", command=self.show_section)
        postproc_menu.add_command(label="Таблицы", command=self.show_tables)
        postproc_menu.add_command(label="Эпюры", command=self.show_epuras)
        postproc_menu.add_command(label="Отчет", command=self.show_report)
        menu_bar.add_cascade(label="Постпроцессор", menu=postproc_menu)

        self.config(menu=menu_bar)

    def show_tables(self):

        self.collect_user_data()
        if Checkers.check_user_input(self.user_data):
            tables = Tables.prepare_tables(self.user_data, 10)
            Tables.create_notebook_with_tables(tables)


    def show_epuras(self):

        self.collect_user_data()
        if Checkers.check_user_input(self.user_data):
            Plots.show_epuras_with_tabs(self, self.user_data)

    def show_section(self):

        self.collect_user_data()
        if Checkers.check_user_input(self.user_data):
            Section.create_section_window(self.user_data)


    def show_report(self):

        self.collect_user_data()
        if Checkers.check_user_input(self.user_data):
            points_table, rods_table, calc_tables = Report.prepare_data(self.user_data)


            output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if output_file:
                Report.generate_pdf(points_table, rods_table, calc_tables, self.scheme, self.user_data, self, output_file)


    def create_frames(self):
        top_frame = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        top_frame.place(x=10, y=10, width=1500, height=220)

        node_frame = self.create_node_frame(top_frame)
        bar_frame = self.create_bar_frame(top_frame)
        point_load_frame = self.create_point_load_frame(top_frame)
        distributed_load_frame = self.create_distributed_load_frame(top_frame)

        top_frame.add(node_frame)
        top_frame.add(bar_frame)
        top_frame.add(point_load_frame)
        top_frame.add(distributed_load_frame)

        bottom_frame = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        bottom_frame.place(x=10, y=240, width=1500, height=350)

        options_frame = self.create_options_frame(bottom_frame)
        canvas_frame = self.create_canvas_frame(bottom_frame)

        bottom_frame.add(options_frame)
        bottom_frame.add(canvas_frame)

    def save_file(self):
        self.collect_user_data()
        data = self.user_data
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            self.clear_input()

            if data.get("points"):
                self.node_rows[0][1].insert(0, data["points"][0])
                for point in data["points"][1:]:
                    self.add_row(self.node_sf, self.node_rows, {"name": "Узел", "fields": ["S, м"]})
                    self.node_rows[-1][1].insert(0, point)

            if data.get("rods"):
                self.bar_rows[0][1].insert(0, data["rods"][0]["point1"])
                self.bar_rows[0][2].insert(0, data["rods"][0]["point2"])
                self.bar_rows[0][3].insert(0, data["rods"][0]["a"])
                self.bar_rows[0][4].insert(0, data["rods"][0]["e"])
                self.bar_rows[0][5].insert(0, data["rods"][0]["sigma"])

                for rod in data["rods"][1:]:
                    self.add_row(self.bar_sf, self.bar_rows,
                                 {"name": "Стержень", "fields": ["Узел 1", "Узел 2", "A, м", "E, Па", "[σ], Па"]})
                    self.bar_rows[-1][1].insert(0, rod["point1"])
                    self.bar_rows[-1][2].insert(0, rod["point2"])
                    self.bar_rows[-1][3].insert(0, rod["a"])
                    self.bar_rows[-1][4].insert(0, rod["e"])
                    self.bar_rows[-1][5].insert(0, rod["sigma"])

            if data.get("point_loads"):
                self.point_load_rows[0][1].insert(0, data["point_loads"][0]["point"])
                self.point_load_rows[0][2].insert(0, data["point_loads"][0]["val"])

                for load in data["point_loads"][1:]:
                    self.add_row(self.pl_sf, self.point_load_rows,
                                 {"name": "Нагрузка", "fields": ["Узел", "F, Н"]})
                    self.point_load_rows[-1][1].insert(0, load["point"])
                    self.point_load_rows[-1][2].insert(0, load["val"])

            if data.get("dist_loads"):
                self.distributed_load_rows[0][1].insert(0, data["dist_loads"][0]["rod"])
                self.distributed_load_rows[0][2].insert(0, data["dist_loads"][0]["val"])

                for load in data["dist_loads"][1:]:
                    self.add_row(self.dl_sf, self.distributed_load_rows,
                                 {"name": "Нагрузка", "fields": ["Стержень", "F, Н"]})
                    self.distributed_load_rows[-1][1].insert(0, load["rod"])
                    self.distributed_load_rows[-1][2].insert(0, load["val"])

            z_type = data.get("z_type", [0])
            self.z_type_var.set(z_type[0])

            self.draw()

    def close(self):
        self.destroy()

    def clear_input(self):
        for rows_storage in [self.node_rows, self.bar_rows, self.point_load_rows, self.distributed_load_rows]:
            while len(rows_storage) > 1:
                self.delete_row(rows_storage, rows_storage[-1], rows_storage[-1][0].cget("text").split()[0])

            if rows_storage:
                last_row = rows_storage[0]
                for widget in last_row[1:]:
                    if isinstance(widget, tk.Entry):
                        widget.delete(0, tk.END)

        self.canvas.delete("all")


    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def add_row(self, frame, rows_storage, labels):
        row_index = len(rows_storage) + 2
        new_row = []

        labels_names = labels['fields']

        for i, text in enumerate(labels_names, start=1):
            tk.Label(frame, text=text).grid(row=1, column=i, padx=5)

        label = tk.Label(frame, text=f"{labels['name']} {row_index-1}")
        label.grid(row=row_index, column=0, padx=5)
        new_row.append(label)

        validation_map = {
            1: lambda col_n: self.rpn_checker if col_n == 'S, м' else self.npn_checker,
            2: lambda col_n: self.npn_checker if col_n == 'Узел 2' else self.rn_checker,
            3: lambda _: self.rpn_checker,
            4: lambda _: self.rpn_checker,
            5: lambda _: self.rpn_checker,
        }

        for col_index, col_name in enumerate(labels['fields'], start=1):
            validate_command = validation_map.get(col_index, lambda _: self.rpn_checker)(col_name)
            entry = tk.Entry(frame, width=10, validate='all', validatecommand=(validate_command, '%P'))
            entry.grid(row=row_index, column=col_index, padx=5)
            if col_name == "Узел 1":
                entry.insert(0, str(row_index-1))
                entry.config(state=tk.DISABLED)
            elif col_name == "Узел 2":
                entry.insert(0, str(row_index))
                entry.config(state=tk.DISABLED)
            elif col_name == "S, м" and row_index == 2:
                entry.insert(0, 0)
                entry.config(state=tk.DISABLED)

            new_row.append(entry)


        delete_button = ttk.Button(frame, text="Удалить", command=lambda: self.delete_row(rows_storage, new_row, labels['name']))
        delete_button.grid(row=row_index, column=len(labels['fields']) + 1, padx=5)

        if row_index == 2:
            delete_button.config(state=tk.DISABLED)

        new_row.append(delete_button)
        rows_storage.append(new_row)

    def delete_row(self, rows_storage, row_widgets, name):
        if len(rows_storage) == 1:
            return

        for widget in row_widgets:
            widget.destroy()
        rows_storage.remove(row_widgets)
        self.update_indices(rows_storage, name)
        self.collect_user_data()

    def update_indices(self, rows_storage, name):
        for index, row in enumerate(rows_storage, start=1):
            row[0].config(text=f"{name} {index}")

            if rows_storage == self.bar_rows:
                row[1].config(state=tk.NORMAL)
                row[1].delete(0, tk.END)
                row[1].insert(0, index)
                row[1].config(state=tk.DISABLED)

                row[2].config(state=tk.NORMAL)
                row[2].delete(0, tk.END)
                row[2].insert(0, index + 1)
                row[2].config(state=tk.DISABLED)

            for widget in row:
                widget.grid_configure(row=index + 1)

    def collect_user_data(self):
        self.user_data.clear()
        for row in self.node_rows:
            s = row[1].get()
            self.user_data["points"].append(s)

        for row in self.bar_rows:
            point1 = row[1].get()
            point2 = row[2].get()
            a = row[3].get()
            e = row[4].get()
            sigma = row[5].get()
            self.user_data["rods"].append({
                "point1": point1,
                "point2": point2,
                "a": a,
                "e": e,
                "sigma": sigma
            })

        for row in self.point_load_rows:
            point = row[1].get()
            val = row[2].get()
            self.user_data["point_loads"].append({
                "point": point,
                "val": val
            })

        for row in self.distributed_load_rows:
            rod = row[1].get()
            val = row[2].get()
            self.user_data["dist_loads"].append({
                "rod": rod,
                "val": val
            })

        z_type = self.z_type_var.get()
        self.user_data["z_type"] = [z_type]

    def draw(self):

        self.collect_user_data()
        if Checkers.check_user_input(self.user_data):
            self.user_data["points"] = [0] + Sheme.change_scale(self.user_data["points"][1:], 10)
            ls = [float(val) for val in self.user_data["points"][1:]]
            nodes = [0.] * len(self.node_rows)
            for i in range(1, len(self.node_rows)):
                nodes[i] = float(self.user_data["points"][i]) + nodes[i - 1]

            rods = sorted(self.user_data["rods"], key=lambda x: x["point1"])
            hs = [float(rod["a"]) for rod in rods]
            hs = Sheme.change_scale(hs, 10)

            temp = Sheme.change_scale(hs + ls, 10)

            hs, ls = temp[:len(hs)], temp[len(hs):]

            conc_loads = self.user_data["point_loads"]
            dist_loads = self.user_data["dist_loads"]

            left_z = [self.user_data["z_type"] == [1] or self.user_data["z_type"] == [3]]
            right_z = [self.user_data["z_type"] == [2] or self.user_data["z_type"] == [3]]

            self.scheme = Sheme.display_scheme(self.canvas, ls, hs, rods, nodes, conc_loads, dist_loads, left_z, right_z)

    def create_node_frame(self, parent):
        node_frame = ttk.LabelFrame(parent, text="Узлы", width=240, height=220)
        node_frame.pack_propagate(False)


        container = ttk.Frame(node_frame)
        canvas = tk.Canvas(container, width=210, height=180)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        self.node_sf = ttk.Frame(canvas)

        self.node_sf.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.node_sf, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)


        ttk.Button(self.node_sf, text="Добавить", command=lambda: self.add_row(
            self.node_sf, self.node_rows, {"name": "Узел", "fields": ["S, м"]}
        )).grid(row=0, column=0, columnspan=5, pady=5)

        container.pack(fill=tk.BOTH, expand=True)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_row(
            self.node_sf, self.node_rows, {"name": "Узел", "fields": ["S, м"]}
        )

        return node_frame

    def create_bar_frame(self, parent):
        bar_frame = ttk.LabelFrame(parent, text="Стержни", width=570, height=220)
        bar_frame.pack_propagate(False)

        container = ttk.Frame(bar_frame)
        canvas = tk.Canvas(container, width=540, height=180)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        self.bar_sf = ttk.Frame(canvas)

        self.bar_sf.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.bar_sf, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self.bar_sf, text="Добавить", command=lambda: self.add_row(
            self.bar_sf, self.bar_rows, {"name": "Стержень", "fields": ["Узел 1", "Узел 2", "A, м", "E, Па", "[О], Па"]}
        )).grid(row=0, column=0, columnspan=8, pady=5)

        container.pack(fill=tk.BOTH, expand=True)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_row(
            self.bar_sf, self.bar_rows,
            {"name": "Стержень", "fields": ["Узел 1", "Узел 2", "A, м", "E, Па", "[О], Па"]}
        )

        return bar_frame

    def create_point_load_frame(self, parent):
        pl_frame = ttk.LabelFrame(parent, text="Сосредоточенные нагрузки", width=335, height=220)
        pl_frame.pack_propagate(False)

        container = ttk.Frame(pl_frame)
        canvas = tk.Canvas(container, width=305, height=180)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        self.pl_sf = ttk.Frame(canvas)

        self.pl_sf.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.pl_sf, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self.pl_sf, text="Добавить", command=lambda: self.add_row(
            self.pl_sf, self.point_load_rows, {"name": "Нагрузка", "fields": ["Узел", "F, Н"]}
        )).grid(row=0, column=0, columnspan=4, pady=5)

        container.pack(fill=tk.BOTH, expand=True)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_row(
            self.pl_sf, self.point_load_rows, {"name": "Нагрузка", "fields": ["Узел", "F, Н"]}
        )

        return pl_frame

    def create_distributed_load_frame(self, parent):
        dl_frame = ttk.LabelFrame(parent, text="Распределенные нагрузки", width=210, height=220)
        dl_frame.pack_propagate(False)

        container = ttk.Frame(dl_frame)
        canvas = tk.Canvas(container, width=180, height=180)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        self.dl_sf = ttk.Frame(canvas)

        self.dl_sf.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.dl_sf, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self.dl_sf, text="Добавить", command=lambda: self.add_row(
            self.dl_sf, self.distributed_load_rows, {"name": "Нагрузка", "fields": ["Стержень", "F, Н"]}
        )).grid(row=0, column=0, columnspan=4, pady=5)

        container.pack(fill=tk.BOTH, expand=True)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_row(
            self.dl_sf, self.distributed_load_rows, {"name": "Нагрузка", "fields": ["Стержень", "F, Н"]}
        )

        return dl_frame

    def create_options_frame(self, parent):
        self.opt_frame = ttk.LabelFrame(parent, text="Заделки", width=160, height=350)
        self.opt_frame.pack_propagate(False)

        self.z_type_var = tk.IntVar()
        self.z_type_var.set(1)

        tk.Radiobutton(self.opt_frame, text="Левая", value=1, variable=self.z_type_var).pack(anchor=tk.W)
        tk.Radiobutton(self.opt_frame, text="Правая", value=2, variable=self.z_type_var).pack(anchor=tk.W)
        tk.Radiobutton(self.opt_frame, text="Обе", value=3, variable=self.z_type_var).pack(anchor=tk.W)

        ttk.Button(self.opt_frame, text="Построить конструкцию", command=self.draw).pack(pady=20)

        return self.opt_frame

    def create_canvas_frame(self, parent):
        self.canvas_frame = ttk.LabelFrame(parent, text="Схема конструкции", width=600, height=350)
        self.canvas_frame.pack_propagate(False)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        return self.canvas_frame


if __name__ == "__main__":
    app = App()
    app.mainloop()
