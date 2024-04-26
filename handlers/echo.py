from aiogram import Router, types


echo_router = Router()


@echo_router.message()
async def reversed_input(message: types.Message):
    messages = message.text
    messages_list = messages.split()
    messages_list.reverse()
    space = " "
    message1 = space.join(messages_list)
    await message.answer(message1)