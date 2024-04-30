import datetime
import logging
import os
import time

import pandas as pd
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ContentType
from dotenv import load_dotenv

load_dotenv("env/.env")

logging.basicConfig(level=logging.INFO)

bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    raise ValueError("Missing BOT_TOKEN environment variable")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer(
        f"Salom [{message.from_user.first_name}](tg://user?id={message.from_user.id})\nXush kelibsiz! ",
        parse_mode="Markdown",
    )


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def process_csv(message: types.Message):
    document = message.document
    if document.mime_type == "text/csv":
        time.sleep(1)
        file_path = f"input_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        await document.download(destination_file=file_path)  # CSV faylini yuklab olish
        await message.reply("Fayl qabul qilindi. XLSX formatiga o'tkazilmoqda...")
        time.sleep(1)

        try:
            # CSV faylini o'qish
            df = pd.read_csv(file_path)
            # Qo'shimcha o'zgarishlar kiritish uchun kod kiritilishi mumkin
        except Exception as e:
            await message.reply(f"Faylni o'qishda xatolik yuz berdi: {str(e)}")
            os.remove(file_path)
            return
        time.sleep(1)
        output_file = f"output_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        df.to_excel(output_file, index=False)  # XLSX fayliga o'tkazish
        time.sleep(1)

        await bot.send_document(
            message.chat.id, types.InputFile(output_file)
        )  # XLSX faylini yuborish

        # Fayllarni o'chirish
        os.remove(file_path)
        os.remove(output_file)
    else:
        await message.reply("Faqat CSV fayllarni qabul qilamiz.")


# Botni ishga tushirish
if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp)
