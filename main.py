import telebot
import re
import db
from telebot import types
from message import *
from schedule_parser import SchedulePage

# Родной
# 1913038657:AAGBUpXae9gnCOka4Kz0xKCQ2t_n1TiFhZA
bot = telebot.TeleBot('698328096:AAGj3J9OxEi0DeLCjYpaka3uHor67rd0oOg')

OBR = ['None', 'Бакалавр', 'Магистр', 'Аспирант', 'Админ']
groups = ['all', 'master', 'bachelor', 'infsec', 'ivt', 'rphys', 'phys']
start_text = ['Расписание', 'Приезд в РФ 2021', 'Общежитие', 'Контакты', 'FAQ']
faq_text = ['Вакцинация', 'Потерял студенческий/зачетку']
dom_text = ["Заселение"]

arrows = ["➡️", "⬅️"]
ADMINS = [i[0] for i in db.DB().get_admins()]
ADMINS.append(230915398)


# ADMINS.append()
def keyboard_mark():
    mstart = types.ReplyKeyboardMarkup(row_width=5)
    startbtn1 = types.KeyboardButton(start_text[0])
    startbtn2 = types.KeyboardButton(start_text[1])
    startbtn3 = types.KeyboardButton(start_text[2])
    startbtn4 = types.KeyboardButton(start_text[3])
    startbtn5 = types.KeyboardButton(start_text[4])
    mstart.row(startbtn1)
    mstart.row(startbtn2)
    mstart.row(startbtn3)
    mstart.row(startbtn4)
    mstart.row(startbtn5)

    return mstart


def keyboard_faq():
    markka = types.ReplyKeyboardMarkup(row_width=3)
    faqbtn1 = types.KeyboardButton(faq_text[0])
    faqbtn2 = types.KeyboardButton(faq_text[1])
    faqbtn3 = types.KeyboardButton('Назад')
    markka.row(faqbtn1)
    markka.row(faqbtn2)
    markka.row(faqbtn3)
    return markka


def keyboard_domintory():
    markdowns = types.ReplyKeyboardMarkup()
    dombtn1 = types.KeyboardButton(dom_text[0])
    dombtn2 = types.KeyboardButton('Назад')
    markdowns.row(dombtn1)
    markdowns.row(dombtn2)
    return markdowns


def keyboard_schedule():
    middle_value = 0
    markdowns = types.ReplyKeyboardMarkup()
    left_btn = types.KeyboardButton("⬅️")
    right_btn = types.KeyboardButton("➡️")
    middle_btn = types.KeyboardButton("{}".format(middle_value))
    markdowns.row(left_btn, middle_btn, right_btn)
    return markdowns


markschedule = keyboard_schedule()
markstart = keyboard_mark()
markfaq = keyboard_faq()
markdomintory = keyboard_domintory()


def get_data_from_msg(string):
    res = [None, None, None, None]
    a = re.split(r'\s', string)
    for i in range(3):
        try:
            res[i] = a[i + 1]
        except:
            res[i] = None

    return res


# Старт
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Этот бот поможет тебе найти ответы на все твои вопросы", reply_markup=markstart)


# Помощь
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Меню", reply_markup=markstart)


# Помощь Админа
@bot.message_handler(commands=['admin_help'])
def send_a_help(message):
    if message.chat.id in ADMINS:
        bot.send_message(message.chat.id, TEXT_ADMIN_HELP)


# Добавление Студента
@bot.message_handler(commands=['add'])
def add_admin(message):
    if message.chat.id in ADMINS:
        i, g, p, c = get_data_from_msg(message.text)
        if int(p) < 4:
            bot.send_message(message.chat.id, 'Добавить пользователя пользоваетель'
                                              ' \nid {} \nгруппа {} \nобразование {}\n курс {}'.format(i, g,
                                                                                                       OBR[int(p)], c))

        db.DB().add_student(int(i), g, int(p))


# Получение id
@bot.message_handler(commands=['me'])
def add(message):
    bot.send_message(message.chat.id, 'id {}'.format(message.chat.id))


# Переотправка в группу
@bot.message_handler(commands=['resend_g'])
def resender_to_group(message):
    if not (message.chat.id in ADMINS):
        return 1
    try:
        to = re.split(r'\s', message.text)[1]
    except:
        bot.send_message(message.chat.id, 'Пожалуйста укажите группу /resend_g группа')
        return 1

    try:
        g = db.DB().find_student_by_group(to)
    except:
        bot.send_message(message.chat.id, 'Пожалуйста введите сообщение в формате /resendg 1.506 или /resend 598')
        return 0

    if message.reply_to_message:
        for i in g:
            bot.forward_message(i, message.chat.id, message.reply_to_message.message_id)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста зареплайте сообщение, которое хотите переслать')


# Переотравка уровню образования
@bot.message_handler(commands=['resend_le'])
def resender_to_le(message):
    if not (message.chat.id in ADMINS):
        return 1
    try:
        to = re.search(r'\d+', message.text).group()
    except:
        bot.send_message(message.chat.id, 'Укажите уровень образования /resend_le 1')
        return 1

    try:
        g = db.DB().find_student_by_level_eduaction(to)
    except:
        bot.send_message(message.chat.id, "{}".format(Exception))
        return 1

    if message.reply_to_message:
        for i in g:
            bot.forward_message(i, message.chat.id, message.reply_to_message.message_id)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста зареплайте сообщение, которое хотите переслать')


# Переотправка по курсам
@bot.message_handler(commands=['resend_c'])
def resender_to_course(message):
    if not (message.chat.id in ADMINS):
        return 1

    try:
        to = re.search(r'\d+', message.text).group()
    except:
        bot.send_message(message.chat.id, 'Укажите группу курс /resend_c 1')
        return 1

    try:
        g = db.DB().find_student_by_level_course(to)
    except:
        bot.send_message(message.chat.id, "{}".format(Exception))
        return 1

    if message.reply_to_message:
        for i in g:
            bot.forward_message(i, message.chat.id, message.reply_to_message.message_id)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста зареплайте сообщение, которое хотите переслать')


@bot.message_handler(commands=['resend'])
def resender_to_all(message):
    if not (message.chat.id in ADMINS):
        return 1

    g = db.DB().get_all_student()

    if message.reply_to_message:
        for i in g:
            bot.forward_message(i, message.chat.id, message.reply_to_message.message_id)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста зареплайте сообщение, которое хотите переслать')


# Реакция на текст
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == "Назад".lower():
        bot.send_message(message.chat.id, "Меню", reply_markup=markstart)

    # Приезд в рф2021
    elif message.text == start_text[1]:
        bot.send_message(message.chat.id, TEXT_PRIEZD)

    # Общежитие
    elif message.text == start_text[2]:
        bot.send_message(message.chat.id, TEXT_DOMINTORY, reply_markup=markdomintory)

    # Контакты
    elif message.text == start_text[3]:
        bot.send_message(message.chat.id, TEXT_CONTACT)

    # FAQ
    elif message.text == start_text[4]:
        bot.send_message(message.chat.id, TEXT_FAQ, reply_markup=markfaq)

    # Расписание
    elif message.text == start_text[0]:
        sp = SchedulePage()
        for msg in sp.get_messange():
            bot.send_message(message.chat.id, msg, parse_mode="HTML")
        bot.send_message(message.chat.id, "Расписание", reply_markup=markschedule)

    # Вакцинация
    elif message.text == faq_text[0]:
        bot.send_message(message.chat.id, TEXT_VACIN)

    # Потерял студент/зачетку
    elif message.text == faq_text[1]:
        bot.send_message(message.chat.id, TEXT_LOST_CART)

    # Общежитие
    elif message.text == dom_text[0]:
        bot.send_message(message.chat.id, TEXT_IN_DOMINTORY)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
