# trig_calc.py
import math


def calculate_trig(value, unit, func, precision):
    """
    Вычисляет тригонометрическую функцию с заданной точностью.
    Возвращает строку с результатом или сообщение об ошибке.
    """
    if unit == 'degrees':
        value_rad = math.radians(value)
    else:
        value_rad = value

    try:
        if func == 'sin':
            result = math.sin(value_rad)
        elif func == 'cos':
            result = math.cos(value_rad)
        elif func == 'tan':
            result = math.tan(value_rad)
        elif func == 'cot':
            result = 1 / math.tan(value_rad)
        else:
            return "❌ Неизвестная функция"

        return f"{result:.{precision}f}"

    except ZeroDivisionError:
        return "∞ (не определено)"
    except Exception as e:
        return f"❌ Ошибка: {e}"