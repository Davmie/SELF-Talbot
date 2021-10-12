import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from sys import platform

from config_spinboxes import *
import config_gui_win as windows
import config_gui_mac_lin as mac

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


        # ДЛЯ ЖЕНИ! ВАЖНО! Теперь эта функция не устанавливает параметры маятников !!!

    def start_button_pressed(self):
        params_are_correct = self._check_params_in_spinboxes()
        if params_are_correct:

            params = self.get_params_from_spinboxes()
            params['p'] = float(params['p']) / 1000
            # здесь вызов ф-ции отрисовки, туда передаёшь params
            # в парамс все переменные
            # ничего не меняй при вводе, запускай с дефолтными
            print(params)

        else:
            self.stop_button_pressed()

    def stop_button_pressed(self):
        print(2)

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
                self.spinboxes_labels['p'].destroy()
                self.spinboxes['p'].destroy()
                self.spinboxes_labels['k'].destroy()
                self.spinboxes['k'].destroy()
                self.spinboxes_labels['zt'].destroy()
                self.spinboxes['zt'].destroy()
                print(self.spinboxes)
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
