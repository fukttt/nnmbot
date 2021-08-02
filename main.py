import asyncio
from mechanic.pars import Parser
from aiogram.types import ParseMode, Message
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types, executor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mechanic.db import User, Base

bot = Bot(token="1791568656:AAF7oE2R7L8Aw3pSGxV2YaYLzxDQROqDqaI")
dp = Dispatcher(bot)


def mainKeyboard():
    button1 = KeyboardButton('🎬 Новинки Кино')
    button3 = KeyboardButton('👾 Автор')
    button4 = KeyboardButton('❓ О боте')
    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    greet_kb.add(button1, button3)
    greet_kb.add(button4)
    return greet_kb


def paginationKeyboard(page):
    button1 = KeyboardButton('⬅️')
    button2 = KeyboardButton("📍 " + str(page))
    button3 = KeyboardButton('➡️')
    button4 = KeyboardButton('🏠 В главное меню')
    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    greet_kb.add(button1, button2, button3)
    greet_kb.add(button4)
    return greet_kb


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if not session.query(User).filter_by(tgid=message.from_user.id).first():
        newuser = User(tgid=message.from_user.id)
        session.add(newuser)
        session.commit()
    await message.reply(
        "Привет! Здесь ты можешь найти новинки кино и скачать их через торрент!",
        reply_markup=mainKeyboard())


@dp.message_handler(commands=['search'])
async def process_start_command(message: types.Message):
    a = Parser()
    links = await a.get_search(message.text.split(' ', 1)[1])
    await message.reply(
        "Привет! Здесь ты можешь найти новинки кино и скачать их через торрент!",
        reply_markup=mainKeyboard())


@dp.message_handler(commands=['sendall'])
async def sendall_command(message: types.Message):
    counter = 0
    for user in session.query(User).all():
        try:
            await bot.send_message(user.tgid, message.text.split(' ', 1)[1])
            counter += 1
        except:
            pass

    await message.reply("✅ Сообщение успешно отправлено %d раз." % counter)


@dp.message_handler(commands=['info'])
async def info_command(message: types.Message):
    count = session.query(User).count()
    await message.reply("Всего юзеров в БД %d" % count)


@dp.message_handler()
async def echo_message(msg: types.Message):

    user = session.query(User).filter_by(tgid=msg.from_user.id).first()

    if "Страница" in msg.text:
        page = msg.text.split(':')[1]
        a = Parser()
        allFilms = await a.get_films(int(page))
        for a in allFilms:
            caption = "`" + a.split(' : ')[0] + "`\nРазмер : *" + a.split(
                ' : ')[3] + "*"
            imag = "https:" + a.split(' : ')[1].split('=')[1].replace(
                "%2F", "/")
            inline_kb_full = InlineKeyboardMarkup(row_width=2)
            inline_kb_full.add(
                InlineKeyboardButton(
                    'MAGNET 🧲',
                    url="https://www.sky-net.co/magnet.php?magnet=" +
                    a.split(' : ')[2]))
            #inline_kb_full.add(InlineKeyboardButton('СМОТРЕТЬ 👁', url="https://4-u.shop/?magnet="+a.split(' : ')[2]))
            await bot.send_photo(msg.from_user.id,
                                 imag,
                                 caption=caption,
                                 parse_mode=ParseMode.MARKDOWN,
                                 reply_markup=inline_kb_full)
    if "Страницу" in msg.text:
        await bot.send_message(
            msg.from_user.id,
            "Скажи боту 'Страница:2' и он выдаст тебе торренты на второй странице"
        )

    if "Автор" in msg.text:
        await bot.send_message(msg.from_user.id, "Автор @Pirate2110")

    if "О боте" in msg.text:
        await bot.send_message(
            msg.from_user.id,
            "Бот на данный момент имеет урезанный функционал : \nПоиск по новинкам кино и переход по страницам.\nВозможно если бот вам понравится, то я сделаю поиск и еще много чего."
        )

    if "В главное меню" in msg.text:
        await msg.reply("Вернулись в главное меню.",
                        reply_markup=mainKeyboard())

    if "Новинки Кино" in msg.text:

        user.page = 1
        session.add(user)
        session.commit()

        a = Parser()
        allFilms = await a.get_films(1)
        for a in allFilms:

            caption = "`" + a.split(' : ')[0] + "`\nРазмер : *" + a.split(
                ' : ')[3] + "*"
            imag = "https:" + a.split(' : ')[1].split('=')[1].replace(
                "%2F", "/")
            inline_kb_full = InlineKeyboardMarkup(row_width=2)
            inline_kb_full.add(
                InlineKeyboardButton(
                    'MAGNET 🧲',
                    url="https://www.sky-net.co/magnet.php?magnet=" +
                    a.split(' : ')[2]))
            #inline_kb_full.add(InlineKeyboardButton('СМОТРЕТЬ 👁', url="https://4-u.shop/?magnet="+a.split(' : ')[2]))
            try:
                await bot.send_photo(msg.from_user.id,
                                     imag,
                                     caption=caption,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=inline_kb_full)
            except Exception as e:
                pass
        await msg.reply("Для навигации используй клавиатуру.",
                        reply_markup=paginationKeyboard(user.page))
    if "⬅️" in msg.text:
        if user.page >= 1:
            if user.page >= 2:
                user.page -= 1
            session.add(user)
            session.commit()
            a = Parser()
            allFilms = await a.get_films(user.page)
            for a in allFilms:

                caption = "`" + a.split(' : ')[0] + "`\nРазмер : *" + a.split(
                    ' : ')[3] + "*"
                imag = "https:" + a.split(' : ')[1].split('=')[1].replace(
                    "%2F", "/")
                inline_kb_full = InlineKeyboardMarkup(row_width=2)
                inline_kb_full.add(
                    InlineKeyboardButton(
                        'MAGNET 🧲',
                        url="https://www.sky-net.co/magnet.php?magnet=" +
                        a.split(' : ')[2]))
                inline_kb_full.add(
                    InlineKeyboardButton('СМОТРЕТЬ 👁',
                                         url="https://4-u.shop/?magnet=" +
                                         a.split(' : ')[2]))
                try:
                    await bot.send_photo(msg.from_user.id,
                                         imag,
                                         caption=caption,
                                         parse_mode=ParseMode.MARKDOWN,
                                         reply_markup=inline_kb_full)
                except Exception as e:
                    pass

        else:
            await bot.send_message(msg.from_user.id,
                                   "Нулевой страницы не существует !.",
                                   reply_markup=paginationKeyboard(user.page))

        await msg.reply("Предыдущая страница.",
                        reply_markup=paginationKeyboard(user.page))

    if "➡️" in msg.text:

        user.page += 1
        session.add(user)
        session.commit()

        await msg.reply("Следующая страница.",
                        reply_markup=paginationKeyboard(user.page))
        a = Parser()
        allFilms = await a.get_films(user.page)
        for a in allFilms:

            caption = "`" + a.split(' : ')[0] + "`\nРазмер : *" + a.split(
                ' : ')[3] + "*"
            imag = "https:" + a.split(' : ')[1].split('=')[1].replace(
                "%2F", "/")
            inline_kb_full = InlineKeyboardMarkup(row_width=2)
            inline_kb_full.add(
                InlineKeyboardButton(
                    'MAGNET 🧲',
                    url="https://www.sky-net.co/magnet.php?magnet=" +
                    a.split(' : ')[2]))
            #inline_kb_full.add(InlineKeyboardButton('СМОТРЕТЬ 👁', url="https://4-u.shop/?magnet="+a.split(' : ')[2]))
            try:
                await bot.send_photo(msg.from_user.id,
                                     imag,
                                     caption=caption,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=inline_kb_full)
            except Exception as e:
                pass


if __name__ == '__main__':
    db = create_engine("sqlite:///users.db")
    connection = db.connect()
    Session = sessionmaker(bind=db)
    session = Session()
    Base.metadata.create_all(db)
    executor.start_polling(dp)
