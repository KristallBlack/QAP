import pytest

from app.calc import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator
    def test_adding_success(self):
        assert self.calc.adding(self, 1, 1) == 2

    def test_zero_divdsion(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.division(self, 1, 0)

    def test_multiply(self):
        assert self.calc.multiply(self, 2, 2) == 4

    def test_divide(self):
        assert self.calc.division(self, 6, 3) == 2

    def test_subtraction(self):
        assert self.calc.subtraction(self, 10, 7) == 3
    def teardown(self):
        print('Выполнение метода Teardown')