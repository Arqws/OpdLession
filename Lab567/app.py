# app.py
# Работа 5,6,7, вариант 1: Тригонометрические функции
# Flask-приложение с выбором точности и единиц измерения

from flask import Flask, render_template, request
import math

app = Flask(__name__)


def calculate_trig(value, unit, func, precision):
    """
    Вычисляет тригонометрическую функцию

    :param value: числовое значение угла
    :param unit: 'degrees' или 'radians'
    :param func: название функции ('sin', 'cos', 'tan', 'cot')
    :param precision: количество знаков после запятой
    :return: отформатированный результат или сообщение об ошибке
    """
    # Конвертируем в радианы, если нужно
    if unit == 'degrees':
        value_rad = math.radians(value)
    else:
        value_rad = value

    # Вычисляем функцию
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

        # Форматируем с заданной точностью
        return f"{result:.{precision}f}"

    except ZeroDivisionError:
        return "∞ (не определено)"
    except Exception as e:
        return f"❌ Ошибка: {e}"


@app.route('/', methods=['GET', 'POST'])
def index():
    """Главная страница с формой и результатом"""
    result = None
    error = None

    if request.method == 'POST':
        try:
            # Получаем данные из формы
            value = float(request.form.get('value', 0))
            unit = request.form.get('unit', 'radians')
            func = request.form.get('function', 'sin')
            precision = int(request.form.get('precision', 4))

            # Ограничиваем точность разумными пределами
            precision = max(0, min(precision, 15))

            # Вычисляем
            result = calculate_trig(value, unit, func, precision)

            # Формируем строку для отображения
            unit_symbol = '°' if unit == 'degrees' else ' рад'
            calculation = f"{func}({value}{unit_symbol}) = {result}"

        except ValueError:
            error = "❌ Пожалуйста, введите корректные числовые значения"
        except Exception as e:
            error = f"❌ Ошибка вычисления: {e}"

    return render_template('index.html', result=result, error=error)


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API-эндпоинт для JSON-запросов"""
    data = request.get_json()

    try:
        value = float(data.get('value', 0))
        unit = data.get('unit', 'radians')
        func = data.get('function', 'sin')
        precision = int(data.get('precision', 4))
        precision = max(0, min(precision, 15))

        result = calculate_trig(value, unit, func, precision)

        return {'success': True, 'result': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}, 400


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)