import tkinter as tk
import time
import math

class MainForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Foundation Calculator")
        self.geometry("400x100")

        self.label = tk.Label(self, text="Автоматизация сбора нагрузок и ширины подошвы фундамента")
        self.label.pack(pady=10)

        self.button = tk.Button(self, text="Перейти к расчёту!", command=self.open_second_form)
        self.button.pack(pady=10)

    def open_second_form(self):
        self.withdraw()  # Скрыть текущую форму
        second_form = SecondForm(self)
        second_form.geometry("1350x600")  # Установить размер второй формы


class SecondForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Расчёт нагрузок и фундамента")
        self.geometry("1350x600")  # Установить размер второй формы
        self.parent = parent
        self.create_widgets()

    # Определение собственного веса стены
    def calculate_wall_self_weight(self, Hom1, Hom2, Hlo, b_wall, v_brick, b_basement_wall, v_concrete):
        P_wall = (Hom1 * b_wall * v_brick) + (Hom2 * b_wall * v_brick) + (Hlo * b_basement_wall * v_concrete)
        return P_wall / 1000  # переводим в тонны

    # Определение нагрузки от перекрытия (для наружной несущёй стены по оси Д)
        # Функция для расчета нагрузки по оси Д
    def calculate_load_from_axis_D(self, P_per_sob, P_snow, P_useful, P_per_basement, P_useful_attic, L_D):
        return (P_per_sob + P_useful) * L_D + (P_per_sob + P_useful_attic) * L_D + (P_per_basement + P_useful) * L_D + (P_per_basement + P_snow) * L_D

        # Определение нагрузки от перекрытия (для наружной несущёй стены по оси В)
    def calculate_load_from(self, P_per_sob, P_snow, P_useful, P_per_basement, P_useful_attic, reliability_factor, L_B):
        P_ext = ((P_per_sob + P_useful) * L_B) + ((P_per_sob + (P_useful_attic * reliability_factor)) * L_B) + ((P_per_basement + P_useful) * L_B) + ((P_per_basement + P_snow) * L_B)
        return P_ext

    # Определение нагрузки от собственного веса фундамента
    def calculate_foundation_load(self, b_foundation, h_foundation, P_concrete):
        P_foundation = b_foundation * h_foundation * P_concrete
        return P_foundation / 1000  # переводим в тонны

    # Определение нагрузки на ось Д
    def oci_D(self, P_wall, P_ext_wall, P_foundation):
        total_D = P_wall + P_ext_wall + P_foundation
        return total_D

    # Определение нагрузки на ось В
    def oci_B(self, P_wall, P_ext, P_foundation):
        total_B = P_wall + P_ext + P_foundation
        return  total_B

    # Определение нагрузки на ось З
    def oci_Z(self, P_wall, P_foundation):
        total_Z = P_wall + P_foundation
        return total_Z

    def create_widgets(self):
        # Создание и размещение элементов интерфейса
        self.label_hom1 = tk.Label(self, text="Высота 1-го этажа (м):")
        self.label_hom1.grid(row=0, column=0, padx=10, pady=5)
        self.entry_hom1 = tk.Entry(self)
        self.entry_hom1.grid(row=0, column=1, padx=10, pady=5)

        self.label_hom2 = tk.Label(self, text="Высота 2-го этажа (м):")
        self.label_hom2.grid(row=0, column=15, padx=10, pady=5)
        self.entry_hom2 = tk.Entry(self)
        self.entry_hom2.grid(row=0, column=16, padx=10, pady=5)

        self.label_hlo = tk.Label(self, text="Высота подвального этажа (м):")
        self.label_hlo.grid(row=0, column=30, padx=10, pady=5)
        self.entry_hlo = tk.Entry(self)
        self.entry_hlo.grid(row=0, column=32, padx=10, pady=5)

        self.label_b_wall = tk.Label(self, text="Толщина наружной стены (м):")
        self.label_b_wall.grid(row=1, column=0, padx=10, pady=5)
        self.entry_b_wall = tk.Entry(self)
        self.entry_b_wall.grid(row=1, column=1, padx=10, pady=5)

        self.label_v_brick = tk.Label(self, text="Плотность кирпичной кладки (м^3):")
        self.label_v_brick.grid(row=1, column=15, padx=10, pady=5)
        self.entry_v_brick = tk.Entry(self)
        self.entry_v_brick.grid(row=1, column=16, padx=10, pady=5)

        self.label_b_basement_wall = tk.Label(self, text="Толщина  наружной стены подвала (м):")
        self.label_b_basement_wall.grid(row=1, column=30, padx=10, pady=5)
        self.entry_b_basement_wall = tk.Entry(self)
        self.entry_b_basement_wall.grid(row=1, column=32, padx=10, pady=5)

        self.label_v_concrete = tk.Label(self, text="Плотность монолитного железобетона (м^3):")
        self.label_v_concrete.grid(row=2, column=0, padx=10, pady=5)
        self.entry_v_concrete = tk.Entry(self)
        self.entry_v_concrete.grid(row=2, column=1, padx=10, pady=5)

        self.label_P_per_sob = tk.Label(self, text="Собственный вес перекрытия (кг/м^3):")
        self.label_P_per_sob.grid(row=2, column=15, padx=10, pady=5)
        self.entry_P_per_sob = tk.Entry(self)
        self.entry_P_per_sob.grid(row=2, column=16, padx=10, pady=5)

        self.label_P_snow = tk.Label(self, text="Значение снеговой нагрузки S (кг/м^2):")
        self.label_P_snow.grid(row=2, column=30, padx=10, pady=5)
        self.entry_P_snow = tk.Entry(self)
        self.entry_P_snow.grid(row=2, column=32, padx=10, pady=5)

        self.label_P_useful = tk.Label(self, text="Полезная нагрузка на междуэтажное перекрытия (кг/м^2):")
        self.label_P_useful.grid(row=3, column=0, padx=10, pady=5)
        self.entry_P_useful = tk.Entry(self)
        self.entry_P_useful.grid(row=3, column=1, padx=10, pady=5)

        self.label_P_per_basement = tk.Label(self, text="Нагрузка на подвал (кН):")
        self.label_P_per_basement.grid(row=3, column=15, padx=10, pady=5)
        self.entry_P_per_basement = tk.Entry(self)
        self.entry_P_per_basement.grid(row=3, column=16, padx=10, pady=5)

        self.label_P_useful_attic = tk.Label(self, text="Полезная нагрузка на чердак (кН):")
        self.label_P_useful_attic.grid(row=3, column=30, padx=10, pady=5)
        self.entry_P_useful_attic = tk.Entry(self)
        self.entry_P_useful_attic.grid(row=3, column=32, padx=10, pady=5)

        self.label_L_D = tk.Label(self, text="Отношение длины к ширине Д:")
        self.label_L_D.grid(row=4, column=0, padx=10, pady=5)
        self.entry_L_D = tk.Entry(self)
        self.entry_L_D.grid(row=4, column=1, padx=10, pady=5)

        self.label_L_B = tk.Label(self, text="Отношение длины к ширине B:")
        self.label_L_B.grid(row=4, column=15, padx=10, pady=5)
        self.entry_L_B = tk.Entry(self)
        self.entry_L_B.grid(row=4, column=16, padx=10, pady=5)

        self.label_b_foundation = tk.Label(self, text="Ширина фундамента (м):")
        self.label_b_foundation.grid(row=4, column=30, padx=10, pady=5)
        self.entry_b_foundation = tk.Entry(self)
        self.entry_b_foundation.grid(row=4, column=32, padx=10, pady=5)

        self.label_h_foundation = tk.Label(self, text="Высота фундамента (м):")
        self.label_h_foundation.grid(row=5, column=0, padx=10, pady=5)
        self.entry_h_foundation = tk.Entry(self)
        self.entry_h_foundation.grid(row=5, column=1, padx=10, pady=5)

        self.label_P_concrete = tk.Label(self, text="Собственный вес:")
        self.label_P_concrete.grid(row=5, column=15, padx=10, pady=5)
        self.entry_P_concrete = tk.Entry(self)
        self.entry_P_concrete.grid(row=5, column=16, padx=10, pady=5)

        self.label_reliability_factor = tk.Label(self, text="Надежность:")
        self.label_reliability_factor.grid(row=5, column=30, padx=10, pady=5)
        self.entry_reliability_factor = tk.Entry(self)
        self.entry_reliability_factor.grid(row=5, column=32, padx=10, pady=5)

        self.label_divisor = tk.Label(self, text="Несущая способность грунта основания при оси Д:")
        self.label_divisor.grid(row=12, column=0, padx=10, pady=5)
        self.entry_divisor_D = tk.Entry(self)
        self.entry_divisor_D.grid(row=12, column=1, padx=10, pady=5)

        self.label_divisor = tk.Label(self, text="Несущая способность грунта основания при оси В:")
        self.label_divisor.grid(row=13, column=0, padx=10, pady=5)
        self.entry_divisor_B = tk.Entry(self)
        self.entry_divisor_B.grid(row=13, column=1, padx=10, pady=5)

        self.label_divisor = tk.Label(self, text="Несущая способность грунта основания при оси З:")
        self.label_divisor.grid(row=14, column=0, padx=10, pady=5)
        self.entry_divisor_Z = tk.Entry(self)
        self.entry_divisor_Z.grid(row=14, column=1, padx=10, pady=5)

        self.calculate_button = tk.Button(self, text="Рассчитать", command=self.calculate_and_display)
        self.calculate_button.grid(row=6, column=0, columnspan=1, padx=10, pady=5)

        self.result_label1 = tk.Label(self, text="")
        self.result_label1.grid(row=7, column=0, columnspan=1, padx=10, pady=5)

        self.result_label2 = tk.Label(self, text="")
        self.result_label2.grid(row=8, column=0, columnspan=1, padx=10, pady=5)

        self.result_label3 = tk.Label(self, text="")
        self.result_label3.grid(row=9, column=0, columnspan=1, padx=10, pady=5)

        self.result_label5 = tk.Label(self, text="")
        self.result_label5.grid(row=16, column=0, columnspan=1, padx=10, pady=5)

        self.result_label6 = tk.Label(self, text="")
        self.result_label6.grid(row=17, column=0, columnspan=1, padx=10, pady=5)

        self.result_label7 = tk.Label(self, text="")
        self.result_label7.grid(row=18, column=0, columnspan=1, padx=10, pady=5)

        # Создание кнопки для перехода на главную форму
        self.next_button = tk.Button(self, text="На главную", command=self.open_main_form)
        self.next_button.grid(row=19, column=0, columnspan=1, padx=10, pady=5)

        self.calculate_foundation_width_button = tk.Button(self, text="Рассчитать ширину подошвы фундамента", command=self.calculate_foundation_width)
        self.calculate_foundation_width_button.grid(row=15, column=0, columnspan=1, padx=10, pady=5)

    def calculate_and_display(self):
        try:
            # Получение данных от пользователя и выполнение расчетов
            Hom1 = float(self.entry_hom1.get())
            Hom2 = float(self.entry_hom2.get())
            Hlo = float(self.entry_hlo.get())
            b_wall = float(self.entry_b_wall.get())
            v_brick = float(self.entry_v_brick.get())
            b_basement_wall = float(self.entry_b_basement_wall.get())
            v_concrete = float(self.entry_v_concrete.get())
            P_per_sob = float(self.entry_P_per_sob.get())
            P_snow = float(self.entry_P_snow.get())
            P_useful = float(self.entry_P_useful.get())
            P_per_basement = float(self.entry_P_per_basement.get())
            P_useful_attic = float(self.entry_P_useful_attic.get())
            reliability_factor = float(self.entry_reliability_factor.get())
            L_D = float(self.entry_L_D.get())
            L_B = float(self.entry_L_B.get())
            b_foundation = float(self.entry_b_foundation.get())
            h_foundation = float(self.entry_h_foundation.get())
            P_concrete = float(self.entry_P_concrete.get())

            # Выполнение расчетов
            P_wall = self.calculate_wall_self_weight(Hom1, Hom2, Hlo, b_wall, v_brick, b_basement_wall, v_concrete)
            P_ext_wall = self.calculate_load_from(P_per_sob, P_snow, P_useful, P_per_basement, P_useful_attic, reliability_factor, L_D)
            P_foundation = self.calculate_foundation_load(b_foundation, h_foundation, P_concrete)
            P_axis_D = self.calculate_load_from_axis_D(P_per_sob, P_snow, P_useful, P_per_basement, P_useful_attic, L_D)
            P_axis_B = self.calculate_load_from(P_per_sob, P_snow, P_useful, P_per_basement, P_useful_attic, reliability_factor, L_B)
            total_Z = self.oci_Z(P_wall, P_foundation)

            # Вывод результатов
            self.result_label1.config(text=f"По оси Д: {round(P_axis_D, 2)} т/п.м")
            self.result_label2.config(text=f"По оси В: {round(P_axis_B, 2)} т/п.м")
            self.result_label3.config(text=f"По оси З: {round(total_Z, 2)} т/п.м")
            self.calculate_foundation_width()
        except ValueError:
            self.result_label1.config(text="Ошибка: Проверьте введенные значения")

    def calculate_foundation_width(self):
        try:
            # Получение данных от пользователя
            P_wall = float(self.result_label1.cget("text").split(":")[-1].strip().split()[0])  # Получение суммарной нагрузки на фундамент из текста метки
            P_ext_wall = float(self.result_label2.cget("text").split(":")[-1].strip().split()[0])  # Получение суммарной нагрузки на фундамент из текста метки
            P_foundation = float(self.result_label3.cget("text").split(":")[-1].strip().split()[0])  # Получение суммарной нагрузки на фундамент из текста метки
            divisors = [float(entry.get()) for entry in (self.entry_divisor_D, self.entry_divisor_B, self.entry_divisor_Z)]
            if any(value <= 0 or not math.isfinite(value) for value in divisors):
                raise ValueError("Несущая способность должна быть положительной")
            # Выполнение расчетов ширины подошвы фундамента
            B_1 = P_wall / divisors[0]  # Для первого случая
            B_2 = P_ext_wall / divisors[1]  # Для первого случая
            B_3 = P_foundation / divisors[2]  # Для первого случая

            # Вывод результатов
            self.result_label5.config(text=f"Ширина подошвы фундамента по оси Д: {round(B_1, 3)} м")
            self.result_label6.config(text=f"Ширина подошвы фундамента по оси В: {round(B_2, 3)} м")
            self.result_label7.config(text=f"Ширина подошвы фундамента по оси З: {round(B_3, 3)} м")

        except ValueError:
            self.result_label5.config(text="Ошибка: Проверьте введенные значения")


    def open_main_form(self):
        self.destroy()
        self.parent.deiconify()

if __name__ == "__main__":
    start_time = time.time()  # Запоминаем время начала работы программы
    app = MainForm()
    app.mainloop()
    end_time = time.time()  # Запоминаем время окончания работы программы
    print("Программа выполнялась за", round(end_time - start_time, 2), "секунд")
