import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from sys import platform
from multiprocessing import Pool, cpu_count
from numpy import reshape, array

from config_spinboxes import *
import config_gui_win as windows
import config_gui_mac_lin as mac
from TalbotMath import *


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.spinboxes = dict()
        self.system = None
        if platform == "win32":
            self.system = windows
        elif platform == "darwin" or platform == "linux":
            self.system = mac
        else:
            self.destroy()
        self.talbot = TalbotMath(1, 0, 1)
        self.array_of_spinboxes = spinboxes_to_create_wave
        # basic config of app
        self.title("Эффект Талбота")
        self.resizable(False, False)
        self.geometry("{}x{}".format(self.system.WINDOW_WIDTH, self.system.WINDOW_HEIGHT))

        self.spinboxes_labels = None

        self.protocol("WM_DELETE_WINDOW", self.closing_window)

        self._create_working_area()
        #self._create_graph()
        self._create_field_with_parameters()

    def closing_window(self):
        if mb.askokcancel("Выход", "{:}\n{:}".format("Вы уверены, что хотите выйти?",
                                                     "Все изменений несохраненные изменения пропадут")):
            self.destroy()

    def _create_working_area(self):
        # base frame and canvas
        self.working_area = tk.Frame(self, width=self.system.WORKING_AREA_SIZE, height=self.system.WORKING_AREA_SIZE)
        self.working_area.grid(row=0, column=0, columnspan=2, rowspan=2)
        self.working_area.propagate(False)

        self.canvas = tk.Canvas(self.working_area,
                                width=self.system.CANVAS_SIZE, height=self.system.CANVAS_SIZE, bg="gray")
        self.canvas.place(anchor='ne', relx=0.98, rely=0.02)

    def create_spinboxes(self):
        self.spinboxes_labels = dict()
        for index, item in enumerate(self.array_of_spinboxes):
            default_value = tk.DoubleVar()
            default_value.set(item['default_value'])

            label = tk.Label(self.field_with_parameters, text=item['label'], anchor='w',
                             width=self.system.FIELD_WITH_PARAMETERS_LABEL_WIDTH)
            label.grid(row=index + 1, column=0, pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

            spinbox = tk.Spinbox(self.field_with_parameters, from_=item['min_value'], to=item['max_value'],
                                 increment=item['step'], textvariable=default_value,
                                 width=self.system.FIELD_WITH_PARAMETERS_SPINBOX_WIDTH)
            spinbox.grid(row=index + 1, column=1, pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)
            self.spinboxes.update({item['name']: spinbox})
            self.spinboxes_labels.update({item['name']: label})

    def create_btns(self):
        self.start_button = tk.Button(self.field_with_parameters, text='Старт', command=self.start_button_pressed)
        # spinboxes_to_create
        self.start_button.grid(row=len(self.array_of_spinboxes) + 2, column=0, columnspan=2,
                               pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

        self.create_graph_button = tk.Button(self.field_with_parameters, text='График I(x, m * Zt)',
                                      command=self.create_graph_button_pressed)
        self.create_graph_button.grid(row=len(self.array_of_spinboxes) + 3, column=0, columnspan=2,
                              pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

    def _create_field_with_parameters(self):
        # base frame
        self.field_with_parameters = tk.LabelFrame(self, text="Параметры",
                                                   width=self.system.FIELD_WITH_PARAMETERS_WIDTH,
                                                   height=self.system.FIELD_WITH_PARAMETERS_HEIGHT)
        self.field_with_parameters.grid(row=0, column=4)
        self.field_with_parameters.grid_propagate(False)

        # buttons
        self.create_btns()

        # create ComboboxList
        self.list_delta_label = tk.Label(self.field_with_parameters, text="Тип решетки:", anchor='w',
                                         width=self.system.FIELD_WITH_PARAMETERS_LABEL_WIDTH)
        self.list_delta_label.grid(row=0, column=0, pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

        self.list_delta_text_var = tk.StringVar()
        self.list_delta_text_var.trace('w', callback=self.list_delta_changed)

        # self.type_of_lattice = tk.StringVar()
        # self.type_of_lattice.set('Волновая')
        # self.wave_delta = tk.Radiobutton(self.field_with_parameters, text='Волновая', value='Волновая', anchor='w',
        #                                  width=15)
        # self.rect_delta = tk.Radiobutton(self.field_with_parameters, text='Прямоугольник', value='Прямоугольник',
        #                                  anchor='w', width=15)

        self.list_delta = ttk.Combobox(self.field_with_parameters, values=["Волновая", "Дискретная"], state='readonly',
                                       text="решетку", width=self.system.FIELD_WITH_PARAMETERS_SPINBOX_WIDTH,
                                       textvar=self.list_delta_text_var)

        self.list_delta.current(0)
        # lbl = tk.Label(self.field_with_parameters, text='Выберите тип решетки: ',  anchor='w')
        # lbl.grid(row=0, column=0)
        # self.wave_delta.grid(row=1, column=0, pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)
        # self.rect_delta.grid(row=2, column=0, pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

        self.list_delta.grid(row=0, column=1, pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)
        # create Spinboxes
        self.create_spinboxes()

    # ПИСАТЬ АНДРЕЮ ПРИ ПОПЫТКЕ ПОНЯТЬ ГРАФИКИ (ТАМ ЕСТЬ ОДНА ПРОБЛЕМА)
    def _create_graph(self):
        self.graph_frame = tk.LabelFrame(self.graph_window, text="График", width=self.system.GRAPH_FRAME_WIDTH,
                                         height=self.system.GRAPH_FRAME_HEIGHT + 100)
        self.graph_frame.grid(row=0, column=2, rowspan=2)
        self.graph_frame.grid_propagate(False)

        graph = tk.Canvas(self.graph_frame, width=self.system.GRAPH_FRAME_WIDTH - 10,
                          height=self.system.GRAPH_FRAME_HEIGHT + 50 - 7, bg='white')
        graph.grid(column=1, row=1)

        self.draw_axis(graph)
        self.draw_graph(graph)

        graph.configure(scrollregion=(-self.system.GRAPH_FRAME_WIDTH // 2, -self.system.GRAPH_FRAME_HEIGHT,
                        self.system.GRAPH_FRAME_WIDTH // 2, 0))

    def draw_axis(self, graph):
        # Ось x
        graph.create_line(-self.system.GRAPH_FRAME_WIDTH // 2 + 8, 0,
                          self.system.GRAPH_FRAME_WIDTH // 2 - 8, 0, width=1, arrow=tk.LAST, fill='grey')
        # Ось y
        graph.create_line(2, (self.system.GRAPH_FRAME_WIDTH // 2),
                          2, -((self.system.GRAPH_FRAME_WIDTH // 2)), width=1, arrow=tk.LAST, fill='grey')

        try:
            x_start = -float(self.get_params_from_spinboxes()['k']) * float(self.get_params_from_spinboxes()['p'])
        except KeyError:
            x_start = -2

        scale = -x_start / 7  # min_x = 7 поэтому 7
        for i in range(-(self.system.GRAPH_FRAME_WIDTH // 2 - 50), self.system.GRAPH_FRAME_WIDTH // 2 - 49, 50):
            # 0.0
            if i == 0:
                size = 2
                graph.create_oval(i - size + 1, i - size + 1, i + size + 1, i + size + 1, fill='grey', outline='grey')
                graph.create_text(i + 12, -10, text='{:.2f}'.format((i / 50)), fill="purple", font=("Helvetica", "7"))
                continue
            # Ось x
            graph.create_line(i, -3, i, 3, width=0.5, fill='grey')
            graph.create_text(i + 3, -10, text='{:.2f}'.format(i / 50 * scale), fill="purple", font=("Helvetica", "7"))

            # Ось y
            if i > self.system.GRAPH_FRAME_WIDTH // 2 - 51:
                graph.create_line(0, -self.system.GRAPH_FRAME_WIDTH // 2 + 35, 6, -self.system.GRAPH_FRAME_WIDTH // 2 + 35, width=0.5, fill='grey')
                graph.create_text(12, -self.system.GRAPH_FRAME_WIDTH // 2 + 35, text="1.0", fill="purple", font=("Helvetica", "7"))

        # Лейблы
        graph.create_text(35, -(self.system.GRAPH_FRAME_WIDTH // 2) + 18, text='I(x, m * Zt)', fill="purple",
                          font=("Helvetica", "10"))
        graph.create_text(self.system.GRAPH_FRAME_WIDTH // 2 - 18, 10, text='x', fill="purple", font=("Helvetica", "10"))

    def draw_graph(self, graph):
        try:
            params = self.get_params_from_spinboxes()
            scale = float(params['k']) * float(params['p']) / 7000
            z0 = float(params['z0']) * 2 * float(params['p']) * float(params['p']) / (self.talbot.l * 1000000)
        except KeyError:
            scale = 2 / 7000
            z0 = 0.2 * 2 / (self.talbot.l * 1000000)
        # граф по дефолту от -7 до 7
        # если ковер от -7 до 7, то x_start надо умножить на kp/7
        points = []
        x_start = -7

        arr_y = []
        while x_start <= 7.1:
            x = x_start
            y = self.talbot.I(x * scale, z0)
            arr_y.append(y)
            points.append([x * 50, -y])
            x_start += 0.001
        y_max = max(arr_y)
        for i in range(len(points)):
            points[i][1] /= y_max
            points[i][1] *= 100
        graph.create_line(points, fill='blue')

    def _from_rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb

    def fill_working_area(self, x_start, x_end, z_start, z_end):
        COLOR_MAX = 255

        x_scale = (x_end - x_start) / self.canvas.winfo_width()
        z_scale = (z_end - z_start) / self.canvas.winfo_width()
        pixels = []
        for i in range(0, self.canvas.winfo_width()):
            for j in range(0, self.canvas.winfo_height()):
                pixels.append([j * x_scale + x_start, i * z_scale + z_start])

        with Pool(cpu_count()) as p:
            intense = array(p.starmap(self.talbot.I, pixels)).reshape(self.canvas.winfo_width(), self.canvas.winfo_height())

        i_min = i_max = intense[0][0]

        for i in range(self.canvas.winfo_width()):
            for j in range(self.canvas.winfo_height()):
                if i_max < intense[i][j]:
                    i_max = intense[i][j]

                if i_min > intense[i][j]:
                    i_min = intense[i][j]

        if not (i_max - i_min):
            color_scale = 0
        else:
            color_scale = COLOR_MAX / (i_max - i_min)

        for x in range(self.canvas.winfo_width()):
            for y in range(self.canvas.winfo_height()):
                color = (int((intense[x][y] - i_min) * color_scale), int((intense[x][y] - i_min) * color_scale),
                         int((intense[x][y] - i_min) * color_scale))
                x1, y1 = (x - 1), (y - 1)
                x2, y2 = (x + 1), (y + 1)
                filling = self._from_rgb(color)
                self.canvas.create_oval(x1, y1, x2, y2, width=0, fill=filling)

    def _check_params_in_spinboxes(self):
        params_are_correct = None
        try:
            for spinbox_original in self.array_of_spinboxes:
                value = float(self.spinboxes[spinbox_original['name']].get())
                if value < spinbox_original['min_value'] or value > spinbox_original['max_value']:
                    raise ValueError

                params_are_correct = True

        except ValueError:
            self.show_error()
            params_are_correct = False

        finally:
            return params_are_correct

    def show_error(self):
        mb.showwarning("Warning", "Проверьте параметры ввода")

    def get_params_from_spinboxes(self):
        params = dict()

        for name, spinbox in self.spinboxes.items():
            params.update({name: spinbox.get()})

        return params

    def set_params_to_spinboxes(self, params):
        for name, value in params.items():
            self.spinboxes[name].delete(0, len(self.spinboxes[name].get()))
            self.spinboxes[name].insert(0, value)

    @staticmethod
    def params_to_digits(params):
        params['p'] = float(params['p']) / 1000
        params['k'] = float(params['k'])
        params['zt'] = float(params['zt'])

    def start_button_pressed(self):
        params_are_correct = self._check_params_in_spinboxes()
        if params_are_correct:
            params = self.get_params_from_spinboxes()
            self.params_to_digits(params)
            if self.list_delta.get() == "Волновая":
                params['n'] = int(params['n'])
                self.talbot = TalbotMath(params['p'], 0, params['n'])
            else:
                params['n'] = int(params['n'])
                params['b'] = float(params['b']) / 1000
                self.talbot = TalbotMath(params['p'], 1, params['n'], params['b'])

            z_start = 0
            z_end = params['zt'] * 2 * params['p'] * params['p'] / self.talbot.l
            x_start = params['k'] * params['p'] * -1
            x_end = params['k'] * params['p']

            self.fill_working_area(x_start, x_end, z_start, z_end)
        else:
            self.stop_button_pressed()

    def stop_button_pressed(self):
        pass

    def create_graph_button_pressed(self):
        params_are_correct = self._check_params_in_spinboxes()
        if params_are_correct:
            params = self.get_params_from_spinboxes()
            self.params_to_digits(params)
            if self.list_delta.get() == "Волновая":
                params['n'] = int(params['n'])
                self.talbot = TalbotMath(params['p'], 0, params['n'])
            else:
                params['n'] = int(params['n'])
                params['b'] = float(params['b']) / 1000
                self.talbot = TalbotMath(params['p'], 1, params['n'], params['b'])

        self.graph_window = tk.Toplevel()
        self.graph_window.resizable(False, False)
        self.graph_window.title("График")
        self._create_graph()

    def delete_parameters(self):
        for key in self.spinboxes_labels:
            self.spinboxes_labels[key].destroy()
            self.spinboxes[key].destroy()

    def list_delta_changed(self, index, value, op):
        if self.spinboxes_labels is None:
            return

        if self.list_delta.get() == "Волновая":
            self.array_of_spinboxes = spinboxes_to_create_wave
            try:
                self.spinboxes_labels['b'].destroy()
                self.spinboxes['b'].destroy()
                self.spinboxes.pop('b')
                self.spinboxes_labels.pop('b')
                self.delete_parameters()
                self.create_spinboxes()
                self.start_button.grid(row=len(self.array_of_spinboxes) + 1, column=0, columnspan=2,
                                       pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)
                self.create_graph_button.grid(row=len(self.array_of_spinboxes) + 2, column=0, columnspan=2,
                                      pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)
            except KeyError:
                pass

        else:
            if self.array_of_spinboxes != spinboxes_to_create_rect:
                self.array_of_spinboxes = spinboxes_to_create_rect
                self.delete_parameters()
                self.create_spinboxes()
                self.start_button.grid(row=len(self.array_of_spinboxes) + 1, column=0, columnspan=2,
                                       pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)
                self.create_graph_button.grid(row=len(self.array_of_spinboxes) + 2, column=0, columnspan=2,
                                      pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)


def main():
    window = Window()
    window.mainloop()


if __name__ == "__main__":
    main()
