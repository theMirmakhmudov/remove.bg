import asyncio
import logging
from aiogram import Dispatcher, F, types, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
import shutil
from config import TOKEN, API_KEY
import requests
import os

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"<b>Assalomu Aleykum, Xurmatli {message.from_user.mention_html()}\nRasmni yuboring:</b>")


@dp.message()
async def cmd_photo(message: types.Message):
    if message.photo:
        photo = message.photo[-1]
        photo_info = await bot.get_file(photo.file_id)

        file_path = f'https://api.telegram.org/file/bot{TOKEN}/{photo_info.file_path}'
        response = requests.get(file_path)

        if response.status_code == 200:
            save_directory = 'photos'
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            save_path = os.path.join(save_directory, photo_info.file_unique_id + '.jpg')

            with open(save_path, 'wb') as f:
                f.write(response.content)

            await message.answer(f"Rasm muvaffaqiyatli saqlandi: {save_path}")
        else:
            await message.answer("Rasmni yuklab olishda xatolik yuz berdi!")
    else:
        await message.answer("Habar rasm turi emas!")

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(save_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': API_KEY},
    )
    if response.status_code == requests.codes.ok:
        with open('no-bg.png', 'wb') as out:
            out.write(response.content)

        file_ids = []

        with open("no-bg.png", "rb") as image_from_buffer:
            result = await message.answer_photo(
                BufferedInputFile(
                    image_from_buffer.read(),
                    filename="example.jpg"
                ))
            shutil.rmtree("photos")

            file_ids.append(result.photo[-1].file_id)
    else:
        print("Error:", response.status_code, response.text)


async def main() -> None:
    await dp.start_polling(bot, polling_timeout=1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
