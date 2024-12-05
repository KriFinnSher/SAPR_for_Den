import re
from tkinter import messagebox


def npn_checker(val):
    pattern = r'^([1-9]\d*|)$'
    return re.match(pattern, val) is not None


def rpn_checker(val):
    pattern = r'^(0(\.\d*)?|[1-9]\d*(\.\d*)?)?$'
    return re.match(pattern, val) is not None


def rn_checker(val):
    pattern = r'^-?(0(\.\d*)?|[1-9]\d*(\.\d*)?)?$'
    return re.match(pattern, val) is not None


def check_user_input(input_data):
    points = input_data['points']
    rods = input_data['rods']
    dist_loads = input_data['dist_loads']
    point_loads = input_data['point_loads']
    z_type = input_data['z_type']


    # <<< Points checks >>>

    if len(points) < 2:
        messagebox.showinfo('Ошибка ввода', 'Задайте как минимум 2 узла.')
        return False

    if points[0] != '0':
        messagebox.showerror('Ошибка ввода', 'Не лезьте в файл!')
        return False

    if len(points) - 1 != len(rods):
        messagebox.showerror('Ошибка ввода', 'Заданы неиспользуемые узлы.')
        return False

    for point in points:
        if point == '':
            messagebox.showerror('Ошибка ввода', 'Пустые поля в секции узлов.')
            return False


    for point in points:
        if not rpn_checker(point):
            messagebox.showerror('Ошибка ввода', 'Не лезьте в файл!')
            return False

    for point in points[1:]:
        if float(point) == 0:
            messagebox.showerror('Ошибка ввода', 'Уберите нули из узлов.')
            return False


    # <<< Rods checks >>>

    if len(rods) == 0:
        messagebox.showinfo('Ошибка ввода', 'Зачем вы это сделали...')
        return False

    if len(rods) > len(points) - 1:
        messagebox.showerror('Ошибка ввода', 'В стержнях используются неуказанные узлы.')
        return False

    for rod in rods:
        for value in rod.values():
            if value == '':
                messagebox.showerror('Ошибка ввода', 'Пустые поля в секции стержней.')
                return False


    for i, rod in enumerate(rods, start=1):
        if int(rod['point1']) != i or int(rod['point2']) != i + 1:
            messagebox.showerror('Ошибка ввода', 'Не лезьте в файл!')
            return False

        if not npn_checker(rod['point1']) or not npn_checker(rod['point2']):
            messagebox.showerror('Ошибка ввода', 'Не лезьте в файл!')
            return False

        if not rpn_checker(rod['a']) or not rpn_checker(rod['e']):
            messagebox.showerror('Ошибка ввода', 'Не лезьте в файл!')
            return False

        if not rpn_checker(rod['sigma']):
            messagebox.showerror('Ошибка ввода', 'Не лезьте в файл!')
            return False

    for rod in rods:
        if float(rod['a']) == 0 or float(rod['e']) == 0 or float(rod['sigma']) == 0:
            messagebox.showerror('Ошибка ввода', 'Уберите нули из стержней.')
            return False


    # <<< Point loads checks >>>

    if len(point_loads) == 0:
        messagebox.showinfo('Ошибка ввода', 'Зачем вы это сделали...')
        return False

    for point_load in point_loads:
        for value in point_load.values():
            if value == '':
                messagebox.showerror('Ошибка ввода', 'Пустые поля в секции нагрузок.')
                return False

    for point_load in point_loads:
        if not npn_checker(point_load['point']) or not rn_checker(point_load['val']):
            messagebox.showerror('Ошибка ввода', 'Не лезьте в файл!')
            return False

    for point_load in point_loads:
        if int(point_load['point']) > len(points):
            messagebox.showerror('Ошибка ввода', 'В нагрузках используются неуказанные узлы.')
            return False


        # <<< Dist loads checks >>>

        if len(dist_loads) == 0:
            messagebox.showinfo('Ошибка ввода', 'Зачем вы это сделали...')
            return False

        for dist_load in dist_loads:
            for value in dist_load.values():
                if value == '':
                    messagebox.showerror('Ошибка ввода', 'Пустые поля в секции нагрузок.')
                    return False

        for dist_load in dist_loads:
            if not npn_checker(dist_load['rod']) or not rn_checker(dist_load['val']):
                messagebox.showerror('Ошибка ввода', 'Не лезьте в файл!')
                return False

        for dist_load in dist_loads:
            if int(dist_load['rod']) > len(rods):
                messagebox.showerror('Ошибка ввода', 'В нагрузках используются неуказанные стержни.')
                return False


        # <<< Supports checks >>>

        if len(z_type) == 0:
            messagebox.showinfo('Ошибка ввода', 'Зачем вы это сделали...')
            return False

        if int(z_type[0]) not in [1, 2, 3]:
            messagebox.showerror('Ошибка ввода', 'Не лезьте в файл!')
            return False


        # <<< Loads checks >>>


        point_loads_points = []
        dist_loads_rods = []

        for point_load in point_loads:
            point_loads_points.append(point_load['point'])

        for dist_load in dist_loads:
            dist_loads_rods.append(dist_load['rod'])

        if len(set(point_loads_points)) != len(point_loads_points):
            messagebox.showinfo('Ошибка ввода', 'Укажите не более одной нагрузки на каждый узел.')
            return False

        if len(set(dist_loads_rods)) != len(dist_loads_rods):
            messagebox.showinfo('Ошибка ввода', 'Укажите не более одной нагрузки на каждый стержень.')
            return False


    return True








