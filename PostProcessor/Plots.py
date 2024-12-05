import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Processor import Calculations
import numpy as np


def show_epuras_with_tabs(parent, input_data, need=True):
    def draw_graph(tab, coordinates, type_, is_u_epur=False, image_path=None):
        figure = Figure(figsize=(6, 4), dpi=100)
        ax = figure.add_subplot(111)

        if is_u_epur:
            temp_len = 0
            for rod in input_data['rods']:
                rod_num = int(rod['point1'])
                rod_len = float(input_data['points'][rod_num])
                rod_e = float(rod['e'])
                rod_a = float(rod['a'])
                rod_q = [float(load['val']) for load in input_data['dist_loads'] if rod_num == int(load['rod'])]
                rod_q = rod_q[0] if rod_q else 0

                delta_0 = Calculations.find_deltas(input_data)[rod_num - 1]
                delta_l = Calculations.find_deltas(input_data)[rod_num]

                x = np.linspace(0, rod_len, 300)
                y = [Calculations.find_u(section_x, delta_0, delta_l, rod_len, rod_q, rod_e, rod_a) for section_x in x]

                ax.plot(x + temp_len, y, color='grey')
                ax.fill_between(x + temp_len, [0] * len(x), y, color='grey', alpha=0.5, hatch='||')

                ax.annotate(f'{round(abs(y[0]), 4)}', (temp_len, y[0]), textcoords="offset points", xytext=(-8, 2),
                             color='black')
                ax.annotate(f'{round(abs(y[-1]), 4)}', (temp_len + rod_len, y[-1]), textcoords="offset points",
                             xytext=(-8, 2), color='black')

                temp_len += rod_len

            ax.set_title("Эпюра для U(x)")
        else:
            x_line = [0] * len(coordinates[0])
            line_1 = coordinates[0]
            line_2 = coordinates[1]

            ax.plot(line_1, x_line, color='grey')
            ax.plot(line_1, line_2, color='grey')
            ax.fill_between(line_1, x_line, line_2, color='grey', hatch='||', alpha=0.5)

            for x, y in zip(line_1, line_2):
                ax.annotate(f'{abs(y)}', (x, y), textcoords="offset points", xytext=(-7, 0), color='black')

            ax.set_title(f"Эпюра для {type_}")

        ax.grid(True)
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

        if image_path:
            figure.savefig(image_path, format='png')

        canvas = FigureCanvasTkAgg(figure, master=tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    window = tk.Toplevel(parent)
    window.title("Графики")
    window.geometry("800x600")

    tab_control = ttk.Notebook(window)

    tab_n = ttk.Frame(tab_control)
    tab_sigma = ttk.Frame(tab_control)
    tab_u = ttk.Frame(tab_control)

    tab_control.add(tab_n, text="Эпюра для N(x)")
    tab_control.add(tab_sigma, text="Эпюра для σ(x)")
    tab_control.add(tab_u, text="Эпюра для U(x)")
    tab_control.pack(expand=1, fill="both")

    line_1, line_2, line_3 = Calculations.find_coordinates(input_data)

    epura_images = [
        "epura_nx.png",
        "epura_sigma.png",
        "epura_ux.png"
    ]

    draw_graph(tab_n, (line_1, line_2), "N(x)", image_path=epura_images[0])
    draw_graph(tab_sigma, (line_1, line_3), "σ(x)", image_path=epura_images[1])
    draw_graph(tab_u, None, None, is_u_epur=True, image_path=epura_images[2])

    if not need:
        window.destroy()

    return epura_images

