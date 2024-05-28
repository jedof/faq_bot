from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from init_bot import bot
from config import settings


router = Router()

menu_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Пройти тест")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

back_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="В меню")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

questions = [
    "Как вы оцениваете эффективность деятельности государственных органов в вашем регионе?",
    "Считаете ли вы, что муниципальные службы обеспечивают достаточное качество жизни в вашем городе/районе?",
    "Какие проблемы вы видите в работе государственных и муниципальных органов в вашем регионе?",
    "Как вы оцениваете уровень коррупции в государственном и муниципальном управлении?",
    "Какие изменения в системе государственного и муниципального управления вы бы хотели видеть?",
    "Как вы считаете, какую роль должны играть граждане в процессе принятия решений на уровне государственного и муниципального управления?"
]

class Form(StatesGroup):
    fullname = State()
    answers = State()


@router.message(Command("start"))
async def show_menu(message: types.Message):
    await message.answer("Государственный Опросник: Исследование Управления.\nВы в меню", reply_markup=menu_keyboard)

@router.message(F.text == "Пройти тест", StateFilter(None))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(Form.fullname)
    await message.answer("Привет! Чтобы начать, напиши своё ФИО:")

@router.message(StateFilter(Form.fullname))
async def fullname(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(Form.answers)
    await message.answer(questions[0])

@router.message(StateFilter(Form.answers))
async def answers(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Form.fullname.state:
        fullname = message.text
        await state.update_data(fullname=fullname)
        await state.set_state(Form.answers)
        await message.answer(questions[0])
    elif current_state == Form.answers.state:
        answers = await state.get_data()
        answers_list = answers.get('answers', [])
        answers_list.append(message.text)
        await state.update_data(answers=answers_list)
        if len(answers_list) < len(questions):
            await message.answer(questions[len(answers_list)])
        else:
            await message.answer(format_answers(answers['fullname'], answers_list), parse_mode="html", reply_markup=back_keyboard)
            for user_id in settings.ADMIN_USERS.get_secret_value().split(","):
                await bot.send_message(text=format_answers(answers['fullname'], answers_list), parse_mode="html", chat_id=user_id)
            await state.clear()


@router.message(F.text == "В меню")
async def back_to_menu(message: types.Message):
    await show_menu(message)


def format_answers(fullname, answers):
    response = f"<b>ФИО:\n</b>{fullname}\n\n<b>Ваши ответы:</b>\n"
    for i, answer in enumerate(answers):
        response += f"{questions[i]}\n<b>Ответ: {answer}</b>\n"
    return response
