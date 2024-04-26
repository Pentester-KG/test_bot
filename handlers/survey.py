from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import database

survey_router = Router()


class BookSurvey(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    salary_or_grade = State()


@survey_router.message(Command("stop"))
@survey_router.message(F.text.lower() == "стоп")
async def stop(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Спасибо за прохождение опроса!")


@survey_router.message(Command('start'))
async def start_survey(message: types.Message, state: FSMContext):
    await state.set_state(BookSurvey.name)
    await message.answer("Как вас зовут?")


@survey_router.message(BookSurvey.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookSurvey.age)
    await message.answer("Напишите ваш возраст")


@survey_router.message(BookSurvey.age)
async def age_of_user(message: types.Message, state: FSMContext):
    age_user = int(message.text)
    if age_user < 7 or age_user > 60:
        await state.clear()
        await message.answer("Спасибо за прохождение опроса!")
    else:
        await state.update_data(age=age_user)
        await state.set_state(BookSurvey.occupation)
        await message.answer("Каким видом деятельности вы занимаетесь?")


@survey_router.message(BookSurvey.occupation)
async def occupation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    age1 = data['age']
    await state.set_state(BookSurvey.salary_or_grade)
    await state.update_data(occupation=message.text)
    if age1 <= 18:
        await message.answer('На какие оценки учишься?')
    else:
        await message.answer('Какую зарплату вы получаете?')


@survey_router.message(BookSurvey.salary_or_grade)
async def salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    data = await state.get_data()
    await database.execute(
        "INSERT INTO results_oprosa (name, age, occupation, salary_or_grade) VALUES (?, ?, ?, ?)",
        (data["name"], data["age"], data["occupation"], data["salary"])
    )
    await message.answer("Спасибо за пройденный опрос!")
    await state.clear()
    await message.answer('Спасибо за отзыв!')









