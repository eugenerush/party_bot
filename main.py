import telebot
from telebot import types
from settings import token

bot = telebot.TeleBot(token)

date = ''
place = ''
do = ''


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    new_party = types.InlineKeyboardButton(text='Новая тусовка', callback_data='new_party')
    see_party = types.InlineKeyboardButton(text='Посмотреть предстоящие тусовки', callback_data='show_party')
    markup.add(new_party, see_party)

    bot.send_message(message.chat.id, 'Привет, что ты хочешь ?', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'new_party':
        markup = types.InlineKeyboardMarkup()
        create_party = types.InlineKeyboardButton(text='Создать тусовку', callback_data='create_party')
        comeback = types.InlineKeyboardButton(text='Вернуться', callback_data='comeback')
        markup.add(create_party, comeback)

        bot.send_message(callback.message.chat.id, 'Выбери', reply_markup=markup)

    elif callback.data == 'create_party':
        bot.send_message(callback.message.chat.id, 'Напиши дату:')
        bot.register_next_step_handler(callback.message, get_date)

    elif callback.data == 'show_party':
        f = open('party.txt', 'r+')
        parties = f.read()

        bot.send_message(callback.message.chat.id, text=parties)

        f.close()

    elif callback.data == 'comeback':
        markup = types.InlineKeyboardMarkup()
        new_party = types.InlineKeyboardButton(text='Новая тусовка', callback_data='new_party')
        see_party = types.InlineKeyboardButton(text='Посмотреть предстоящие тусовки', callback_data='see_party')
        markup.add(new_party, see_party)

        bot.send_message(callback.message.chat.id, 'Привет, что ты хочешь ?', reply_markup=markup)

    if callback.data == 'yes':
        bot.send_message(callback.message.chat.id, 'Отлично, тусовка создана')
        markup = types.InlineKeyboardMarkup()
        new_party = types.InlineKeyboardButton(text='Новая тусовка', callback_data='new_party')
        see_party = types.InlineKeyboardButton(text='Посмотреть предстоящие тусовки', callback_data='show_party')
        markup.add(new_party, see_party)

        bot.send_message(-1001172473473,
                         text='Предложили новую тусовку \nДата ' + date + ', место: ' + place + ', будем - ' + do)
        question = 'Кто "За" ?'
        answer = ['Я', 'Не я', 'Макс лох']

        bot.send_poll(-1001172473473, question, answer,
                      is_anonymous=False, allows_multiple_answers=False)

        f = open('party.txt', 'a+')
        f.write('Дата ' + date + ', место: ' + place + ', будем - ' + do + '\n')
        f.close()

        bot.send_message(callback.message.chat.id, 'Привет, что ты хочешь ?', reply_markup=markup)

    elif callback.data == 'no':
        bot.send_message(callback.message.chat.id, 'Давай попробуем еще раз')
        markup = types.InlineKeyboardMarkup()
        create_party = types.InlineKeyboardButton(text='Создать тусовку', callback_data='create_party')
        comeback = types.InlineKeyboardButton(text='Вернуться', callback_data='comeback')
        markup.add(create_party, comeback)

        bot.send_message(callback.message.chat.id, 'Выбери', reply_markup=markup)


def get_date(message):
    global date
    date = message.text
    bot.send_message(message.chat.id, 'Назови место:')
    bot.register_next_step_handler(message, get_place)


def get_place(message):
    global place
    place = message.text
    bot.send_message(message.chat.id, 'Что будем делать ?')
    bot.register_next_step_handler(message, get_do)


def get_do(message):
    global do
    do = message.text

    markup = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    markup.add(yes, no)
    question = 'Дата ' + date + ', место: ' + place + ', будем - ' + do + ' ?'
    bot.send_message(message.chat.id, text=question, reply_markup=markup)


bot.polling()
