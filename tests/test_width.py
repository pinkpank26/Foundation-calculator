"""Exercise actual calculation methods without starting Tk or importing Tkinter."""
import ast
from pathlib import Path
from types import SimpleNamespace
import math
import unittest


class Field:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def cget(self, key):
        return self.value

    def config(self, *, text):
        self.value = text


class WidthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'min.py').read_text())
        form = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'SecondForm')
        method = next(n for n in form.body if isinstance(n, ast.FunctionDef) and n.name == 'calculate_foundation_width')
        namespace = {'math': math}
        exec(compile(ast.Module(body=[method], type_ignores=[]), 'min.py', 'exec'), namespace)
        cls.calculate = staticmethod(namespace[method.name])

    def form(self, divisors):
        return SimpleNamespace(
            result_label1=Field('По оси Д: 12 т/п.м'),
            result_label2=Field('По оси В: 20 т/п.м'),
            result_label3=Field('По оси З: 30 т/п.м'),
            result_label5=Field(), result_label6=Field(), result_label7=Field(),
            **{f'entry_divisor_{axis}': Field(str(value)) for axis, value in zip('DBZ', divisors)},
        )

    def test_separate_soil_capacity_for_each_axis(self):
        form = self.form([2, 4, 10])
        self.calculate(form)
        self.assertTrue(form.result_label5.value.endswith('6.0 м'))
        self.assertTrue(form.result_label6.value.endswith('5.0 м'))
        self.assertTrue(form.result_label7.value.endswith('3.0 м'))

    def test_invalid_soil_capacity(self):
        for value in [0, -1, 'nan', 'inf', '']:
            with self.subTest(value=value):
                form = self.form([2, value, 10])
                self.calculate(form)
                self.assertIn('Ошибка', form.result_label5.value)


if __name__ == '__main__':
    unittest.main()
