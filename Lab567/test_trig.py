# test_trig.py
# Работа 8,9: Unit-тесты для тригонометрического калькулятора
import unittest
import math
from trig_calc import calculate_trig


class TestTrigCalculator(unittest.TestCase):
    """Тестирование вычисления тригонометрических функций"""

    # === Тесты для SIN ===
    def test_sin_30_degrees(self):
        self.assertEqual(calculate_trig(30, 'degrees', 'sin', 4), "0.5000")

    def test_sin_pi2_radians(self):
        self.assertEqual(calculate_trig(math.pi/2, 'radians', 'sin', 4), "1.0000")

    def test_sin_0(self):
        self.assertEqual(calculate_trig(0, 'degrees', 'sin', 2), "0.00")

    # === Тесты для COS ===
    def test_cos_60_degrees(self):
        self.assertEqual(calculate_trig(60, 'degrees', 'cos', 4), "0.5000")

    def test_cos_pi_radians(self):
        self.assertEqual(calculate_trig(math.pi, 'radians', 'cos', 4), "-1.0000")

    # === Тесты для TAN ===
    def test_tan_45_degrees(self):
        self.assertEqual(calculate_trig(45, 'degrees', 'tan', 4), "1.0000")

    def test_tan_0(self):
        self.assertEqual(calculate_trig(0, 'degrees', 'tan', 3), "0.000")

    # === Тесты для COT ===
    def test_cot_45_degrees(self):
        self.assertEqual(calculate_trig(45, 'degrees', 'cot', 4), "1.0000")

    def test_cot_0_undefined(self):
        # cot(0) = 1/tan(0) → Division by Zero
        result = calculate_trig(0, 'degrees', 'cot', 4)
        self.assertIn("∞", result)

    # === Тесты точности ===
    def test_precision_2_digits(self):
        self.assertEqual(calculate_trig(45, 'degrees', 'sin', 2), "0.71")

    def test_precision_6_digits(self):
        self.assertEqual(calculate_trig(45, 'degrees', 'sin', 6), "0.707107")

    def test_precision_0_digits(self):
        self.assertEqual(calculate_trig(90, 'degrees', 'sin', 0), "1")

    # === Граничные случаи и ошибки ===
    def test_negative_angle(self):
        self.assertEqual(calculate_trig(-90, 'degrees', 'sin', 4), "-1.0000")

    def test_large_angle_360(self):
    # sin(360°) может вернуть -0.0000 из-за точности float
        result = calculate_trig(360, 'degrees', 'sin', 4)
        self.assertTrue(result in ["0.0000", "-0.0000"])

    def test_unknown_function(self):
        self.assertEqual(calculate_trig(30, 'degrees', 'sec', 4), "❌ Неизвестная функция")

    def test_invalid_precision_type(self):
        result = calculate_trig(30, 'degrees', 'sin', -1)
        self.assertTrue(isinstance(result, str))


if __name__ == '__main__':
    unittest.main(verbosity=2)