# app.py
# Работа 5,6,7: Тригонометрический калькулятор (Flask)
# Логика вычислений вынесена в trig_calc.py для unit-тестирования (Работа 8,9)

from flask import Flask, render_template, request
from trig_calc import calculate_trig

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Главная страница: обработка формы и вывод результата"""
    result = None
    error = None

    if request.method == 'POST':
        try:
            # 1. Получаем данные из HTML-формы
            value = float(request.form.get('value'))
            unit = request.form.get('unit')
            func = request.form.get('function')
            precision = int(request.form.get('precision'))

            # 2. Ограничиваем точность безопасным диапазоном (0–15 знаков)
            precision = max(0, min(precision, 15))

            # 3. Вызываем функцию из отдельного модуля
            result = calculate_trig(value, unit, func, precision)

        except ValueError:
            error = "Ошибка: введите корректные числовые значения."
        except Exception as e:
            error = f"Ошибка вычисления: {e}"

    # 4. Передаём результат или ошибку в шаблон
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    # Запуск локального сервера разработки
    app.run(debug=True, host='127.0.0.1', port=5000)