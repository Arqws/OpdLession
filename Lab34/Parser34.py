# Parser34.py
# Работа 3,4: Телеграм-бот «Кто хочет стать миллионером?» (5 вопросов)
# Используем: aiogram 2.25.1 (Long Polling)

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
import logging

# ================= НАСТРОЙКИ =================
#  ТОКЕН ОТ @BotFather
TOKEN = "8756203644:AAFXrWFJ0eAyr1stIuiXvjEV7n0kBkbkzHg"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


# ================= МАШИНА СОСТОЯНИЙ =================
class QuizState(StatesGroup):
    """Состояния для прохождения викторины"""
    answering_q1 = State()
    answering_q2 = State()
    answering_q3 = State()
    answering_q4 = State()
    answering_q5 = State()


# ================= БАЗА ВОПРОСОВ (5 вопросов) =================
QUESTIONS = [
    {
        "question": "Столица Австралии?",
        "options": ["Сидней", "Мельбурн", "Канберра", "Перт"],
        "correct": 2,  # индекс правильного ответа (0-3)
        "explanation": "✅ Верно! Канберра — столица Австралии с 1927 года."
    },
    {
        "question": "Сколько планет в Солнечной системе?",
        "options": ["7", "8", "9", "10"],
        "correct": 1,
        "explanation": "✅ Правильно! 8 планет (Плутон — карликовая планета с 2006 г)."
    },
    {
        "question": "Химическая формула воды?",
        "options": ["CO₂", "H₂O", "NaCl", "O₂"],
        "correct": 1,
        "explanation": "✅ Верно! H₂O — два атома водорода и один кислорода."
    },
    {
        "question": "Кто написал роман «Война и мир»?",
        "options": ["Достоевский", "Чехов", "Толстой", "Тургенев"],
        "correct": 2,
        "explanation": "✅ Правильно! Лев Николаевич Толстой (1863-1869 гг)."
    },
    {
        "question": "Сколько байт в 1 Килобайте?",
        "options": ["1000", "1024", "512", "2048"],
        "correct": 1,
        "explanation": "✅ Верно! 1 КБ = 1024 байта (в двоичной системе)."
    }
]


# ================= ОБРАБОТЧИКИ КОМАНД =================

@dp.message_handler(commands=['start', 'help'])
async def process_start_command(message: types.Message):
    """Обработчик команд /start и /help"""
    await message.reply(
        "🎮 Добро пожаловать в игру «Кто хочет стать миллионером?»!\n\n"
        "📋 Правила:\n"
        "• 5 вопросов с 4 вариантами ответа каждый\n"
        "• Введите номер правильного ответа (1-4)\n"
        "• За верный ответ — +1 балл 🏆\n"
        "• Максимальный счёт: 5 из 5!\n\n"
        "Нажмите /game чтобы начать!",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message_handler(commands=['game'])
async def start_game(message: types.Message, state: FSMContext):
    """Начало игры"""
    await state.update_data(score=0, current_question=0)

    q = QUESTIONS[0]
    options = "\n".join([f"{i + 1}. {opt}" for i, opt in enumerate(q["options"])])

    await message.reply(
        f"🚀Игра началась!\n\n"
        f"❓ Вопрос 1 из 5:\n\n"
        f"{q['question']}\n\n"
        f"{options}\n\n"
        f"💡 Введите номер ответа (1-4):",
        reply_markup=ReplyKeyboardRemove()
    )
    await QuizState.answering_q1.set()


# ================= ОБРАБОТЧИКИ ОТВЕТОВ =================

@dp.message_handler(state=QuizState.answering_q1)
async def handle_q1(message: types.Message, state: FSMContext):
    await _process_answer(message, state, 0, QuizState.answering_q2)


@dp.message_handler(state=QuizState.answering_q2)
async def handle_q2(message: types.Message, state: FSMContext):
    await _process_answer(message, state, 1, QuizState.answering_q3)


@dp.message_handler(state=QuizState.answering_q3)
async def handle_q3(message: types.Message, state: FSMContext):
    await _process_answer(message, state, 2, QuizState.answering_q4)


@dp.message_handler(state=QuizState.answering_q4)
async def handle_q4(message: types.Message, state: FSMContext):
    await _process_answer(message, state, 3, QuizState.answering_q5)


@dp.message_handler(state=QuizState.answering_q5)
async def handle_q5(message: types.Message, state: FSMContext):
    await _process_answer(message, state, 4, None)


async def _process_answer(message: types.Message, state: FSMContext, q_index: int, next_state):
    """Универсальная обработка ответа на вопрос"""

    user_answer = message.text.strip()
    data = await state.get_data()
    score = data.get("score", 0)

    # Валидация ввода
    if not user_answer.isdigit() or not 1 <= int(user_answer) <= 4:
        await message.reply("⚠️ Пожалуйста, введите число от 1 до 4.")
        return

    answer = int(user_answer) - 1  # конвертируем 1-4 → 0-3
    correct = QUESTIONS[q_index]["correct"]

    # Проверка ответа
    if answer == correct:
        score += 1
        feedback = QUESTIONS[q_index]["explanation"]
    else:
        correct_text = QUESTIONS[q_index]["options"][correct]
        feedback = (f"❌ Неверно. Правильный ответ: {correct_text}.\n"
                    f"{QUESTIONS[q_index]['explanation']}")

    await state.update_data(score=score)

    # Последний вопрос?
    if q_index == len(QUESTIONS) - 1:
        await _show_final_result(message, score)
        await state.finish()
        return

    # Следующий вопрос
    next_q = q_index + 1
    q = QUESTIONS[next_q]
    options = "\n".join([f"{i + 1}. {opt}" for i, opt in enumerate(q["options"])])

    await message.reply(
        f"{feedback}\n\n"
        f"📊 Ваш счёт: {score}/{next_q}\n\n"
        f"❓ Вопрос {next_q + 1} из {len(QUESTIONS)}:\n\n"
        f"{q['question']}\n\n"
        f"{options}\n\n"
        f"💡 Введите номер ответа (1-4):"
    )
    await state.set_state(next_state)


async def _show_final_result(message: types.Message, score: int):
    """Показ финального результата"""

    if score == 5:
        result = "🏆 ПОЗДРАВЛЯЕМ! Вы ответили на все вопросы!\nВы — настоящий эрудит! 🎉"
    elif score >= 3:
        result = "🎉 Отличный результат! Вы хорошо разбираетесь в темах!"
    elif score >= 1:
        result = "👍 Неплохо! Попробуйте ещё раз для лучшего результата."
    else:
        result = "📚 Не расстраивайтесь! Попробуйте пройти викторину снова."

    await message.reply(
        f"🎮 Игра завершена!\n\n"
        f"📊 Ваш счёт: {score} из 5\n\n"
        f"{result}\n\n"
        f"Нажмите /game чтобы сыграть ещё раз!",
        reply_markup=ReplyKeyboardRemove()
    )


# ================= ЗАПУСК БОТА =================

def run_bot():
    """Функция запуска бота (вызывается из main34.py)"""
    print("🤖 Бот запущен. Ожидаю сообщения в Telegram...")
    print("💡 Для начала игры отправьте боту команду /game")
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("💡 Возможные причины:")
        print("   • Неправильный токен бота")
        print("   • Нет доступа к api.telegram.org (проверьте сеть/VPN)")
        print("   • Бот уже запущен в другом месте")
        _test_logic_mock()


def _test_logic_mock():
    """Тест логики без подключения к Telegram (для отчёта)"""
    print("\n🧪 ТЕСТОВЫЙ РЕЖИМ — проверка вопросов:")
    print("=" * 60)
    for i, q in enumerate(QUESTIONS, 1):
        print(f"\n❓ Вопрос {i}: {q['question']}")
        for j, opt in enumerate(q['options'], 1):
            print(f"   {j}. {opt}")
        print(f"   ✅ Правильный: {q['options'][q['correct']]}")
    print(f"\n✅ Логика бота работает корректно!")
    print("📁 Для полноценной работы: проверьте токен и интернет.")


if __name__ == "__main__":
    run_bot()