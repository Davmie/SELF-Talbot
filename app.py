import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from sys import platform

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
        self.field_with_parameters = tk.LabelFrame(self, text="Параметры",
                                                   width=self.system.FIELD_WITH_PARAMETERS_WIDTH,
                                                   height=self.system.FIELD_WITH_PARAMETERS_HEIGHT)
        self.spinboxes_labels = None

        self.protocol("WM_DELETE_WINDOW", self.closing_window)

        self._create_field_with_parameters()
        self._create_working_area()

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
        self.start_button.grid(row=len(self.array_of_spinboxes) + 2, column=0,
                               pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

        self.stop_button = tk.Button(self.field_with_parameters, text='Стоп', command=self.stop_button_pressed)
        self.stop_button.grid(row=len(self.array_of_spinboxes) + 2, column=1,
                              pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

    def _create_field_with_parameters(self):
        # base frame

        self.field_with_parameters.grid(row=0, column=3)
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

        self.list_delta = ttk.Combobox(self.field_with_parameters, values=["Волновая", "Щели"], state='readonly',
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

    def fill_working_area(self, x_start, x_end, z_start, z_end):
        COLOR_MAX = 255


        x_scale = (x_end - x_start) / self.system.WORKING_AREA_SIZE
        z_scale = (z_end - z_start) / self.system.WORKING_AREA_SIZE
        print(x_end, x_start, z_end, z_start)

        intens = []

        for i in range(self.system.WORKING_AREA_SIZE):
            intens.append([0]*self.system.WORKING_AREA_SIZE)

        i_max = i_min = self.talbot.I(x_start, z_start)

        for x in range(self.system.WORKING_AREA_SIZE):
            for y in range(self.system.WORKING_AREA_SIZE):
                print((y) * x_scale + x_start, x * z_scale + z_start)
                intens[x][y]= self.talbot.I((y) * x_scale + x_start, x * z_scale + z_start)

                if i_max > intens[x][y]:
                    i_max = intens[x][y]

                if i_min < intens[x][y]:
                    i_min = intens[x][y]

        if not(i_max - i_min):
            color_scale = 0
        else:
            color_scale = COLOR_MAX / (i_max - i_min)


        for x in range(self.system.WORKING_AREA_SIZE):
            for y in range(self.system.WORKING_AREA_SIZE):
                color = (int((intens[x][y] - i_min) * color_scale), int((intens[x][y] - i_min) * color_scale), int((intens[x][y] - i_min) * color_scale))

                self.canvas.create_line(x, y, x, y, width=1, fill=color)

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
        params['k'] = int(params['k'])
        params['zt'] = float(params['zt'])

    def start_button_pressed(self):
        params_are_correct = self._check_params_in_spinboxes()
        if params_are_correct:
            params = self.get_params_from_spinboxes()
            self.params_to_digits(params)
            if self.list_delta.get() == "Волновая":
                params['n'] = 1
                self.talbot = TalbotMath(params['p'], 0, params['n'])
            else:
                params['n'] = 400
                self.talbot = TalbotMath(params['p'], 1, params['n'], params['b'])

            z_start = 0
            z_end = params['zt'] * 2 * params['p'] * params['p'] / (5 * 10 ** (-7))
            x_start = params['k'] * params['p'] * -1
            x_end = params['k'] * params['p']
            print(z_start, z_end, x_start, x_end)

            self.fill_working_area(x_start, x_end, z_start, z_end)

        else:
            self.stop_button_pressed()

    def stop_button_pressed(self):
        print(2)

    def delete_parameters(self):
        self.spinboxes_labels['p'].destroy()
        self.spinboxes['p'].destroy()
        self.spinboxes_labels['k'].destroy()
        self.spinboxes['k'].destroy()
        self.spinboxes_labels['zt'].destroy()
        self.spinboxes['zt'].destroy()

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
                self.start_button.grid(row=len(self.array_of_spinboxes) + 1, column=0,
                                       pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)
                self.stop_button.grid(row=len(self.array_of_spinboxes) + 1, column=1,
                                      pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)
            except KeyError:
                pass

        else:
            if self.array_of_spinboxes != spinboxes_to_create_rect:
                self.array_of_spinboxes = spinboxes_to_create_rect
                self.delete_parameters()
                self.create_spinboxes()
                self.start_button.grid(row=len(self.array_of_spinboxes) + 1, column=0,
                                       pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)
                self.stop_button.grid(row=len(self.array_of_spinboxes) + 1, column=1,
                                      pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)


def main():
    window = Window()
    window.mainloop()


if __name__ == "__main__":
    main()
