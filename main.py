import telebot
import re
from telebot import types

import schedule_parser
from message import BotMessange
from schedule_parser import SchedulePage
from db import DB
from schedule_parser import is_group


def parse_name_from_message(message):
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    username = message.from_user.username or ""

    if not first_name and not last_name:
        return username

    return f"{first_name} {last_name}".strip()


def get_schedule_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3)
    keyboard.add(*[telebot.types.KeyboardButton(btn) for btn in SCHEDULE])
    keyboard.add(telebot.types.KeyboardButton("Назад"))
    return keyboard


def get_role_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=len(ROLE))
    keyboard.add(*[types.KeyboardButton(role.capitalize()) for role in ROLE])
    keyboard.add(telebot.types.KeyboardButton("Назад"))
    return keyboard


def get_keyboard_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=len(START_TEXT))
    for btn in START_TEXT:
        keyboard.add(types.KeyboardButton(btn))
    keyboard.add(telebot.types.KeyboardButton("Назад"))
    return keyboard


def get_keyboard_faq():
    keyboard = types.ReplyKeyboardMarkup(row_width=len(FAQ_TEXT))
    for btn in FAQ_TEXT:
        keyboard.add(types.KeyboardButton(btn))
    keyboard.add(types.KeyboardButton('Назад'))
    return keyboard


def get_keyboard_domintory():
    markdowns = types.ReplyKeyboardMarkup()
    for btn in DOM_TEXT:
        markdowns.add(types.KeyboardButton(btn))
    markdowns.add(types.KeyboardButton('Назад'))
    return markdowns


ROLE = ["Студент", "Преподователь", "Абитуриент"]
START_TEXT = ['Расписание', 'Заказать справку', 'Общежитие', 'Контакты', 'FAQ']
FAQ_TEXT = ['Потерял студенческий/зачетку']
DOM_TEXT = ["Заселение"]
SCHEDULE = ["Предыдущая", "Текущая", "Следующая"]


class AsuBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

        @self.bot.message_handler(commands=["help"])
        def send_help(message):
            chat_id = message.chat.id
            if DB().is_admin(chat_id):
                self.bot.send_message(chat_id, BotMessange.ADMIN_HELP)
            else:
                self.bot.send_message(chat_id, BotMessange.HELP, reply_markup=get_keyboard_faq())

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)
            if user_data:
                self.bot.send_message(chat_id, BotMessange.WELCOME_MSG.format(user_data["username"]),
                                      reply_markup=get_keyboard_menu())
            else:
                self.bot.send_message(chat_id, BotMessange.WELCOME_ASK,
                                      reply_markup=get_role_keyboard())

        @self.bot.message_handler(commands=['me'])
        def send_me_message(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)
            if user_data:

                self.bot.send_message(chat_id, BotMessange.ABOUT_USER.format(user_data["id"],
                                                                             user_data["username"],
                                                                             user_data["group"],
                                                                             user_data["phone_number"],
                                                                             user_data["role"]), parse_mode="HTML")
            else:
                self.bot.send_message(chat_id, BotMessange.WELCOME_HELP_MSG,
                                      reply_markup=get_role_keyboard())

        @self.bot.message_handler(commands=["update_group"])
        def send_update_group(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)
            group = message.text.strip("/update_group ")
            print(group)
            if user_data and is_group(group):
                DB().update_user_group_by_id(chat_id, group)

                self.bot.send_message(chat_id, "Ваши данные обновлены!")

                user_data = DB().get_user(chat_id)
                self.bot.send_message(chat_id, BotMessange.ABOUT_USER.format(user_data["id"],
                                                                             user_data["username"],
                                                                             user_data["group"],
                                                                             user_data["phone_number"],
                                                                             user_data["role"]), parse_mode="HTML")
            else:
                self.bot.send_message(chat_id, BotMessange.GROUP_HELP,
                                      reply_markup=get_role_keyboard(),
                                      parse_mode="HTML")

        @self.bot.message_handler(commands=["get_all"])
        def admin_send_all_users(message):
            chat_id = message.chat.id
            users = DB().get_all()
            if DB().is_admin(chat_id):
                for user_data in users:
                    self.bot.send_message(chat_id, BotMessange.ABOUT_USER.format(user_data["id"],
                                                                                 user_data["username"],
                                                                                 user_data["group"],
                                                                                 user_data["phone_number"],
                                                                                 user_data["role"]), parse_mode="HTML")

        @self.bot.message_handler(commands=["forward"])
        def admin_forward_all(message):
            chat_id = message.chat.id
            users = DB().get_all()
            if not DB().is_admin(chat_id):
                return 0

            try:
                reply_id = message.reply_to_message.message_id

            except:
                self.bot.send_message(chat_id, "Нужно зареплаить сообщение")
                return 0

            for user_data in users:
                self.bot.copy_message(chat_id=user_data["id"], from_chat_id=chat_id, message_id=reply_id)

        @self.bot.message_handler(func=lambda message: message.text.lower() == "Назад".lower())
        def handle_menu(message):
            self.bot.send_message(message.chat.id, "Меню", reply_markup=get_keyboard_menu())

        @self.bot.message_handler(func=lambda message: message.text in SCHEDULE)
        def handle_schedule_navigation(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)
            if user_data is None:
                return 0

            if message.text == "Предыдущая":
                self.send_schedule(chat_id, user_data, schedule_date="-1")

            elif message.text == "Текущая":
                self.send_schedule(chat_id, user_data, schedule_date="0")

            elif message.text == "Следующая":
                self.send_schedule(chat_id, user_data, schedule_date="1")


        @self.bot.message_handler(func=lambda message: message.text in START_TEXT)
        def handle_start_navigation(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)

            if user_data is None:
                return 0

            if message.text == "Расписание":
                self.send_schedule(chat_id, user_data, schedule_date="0")

            elif message.text == "Заказать справк":
                self.bot.send_message(chat_id, BotMessange.SPAVKA)

            elif message.text == "Общежитие":
                self.bot.send_message(chat_id, BotMessange.SPAVKA)

            elif message.text == "Контакты":
                self.bot.send_message(chat_id, BotMessange.SPAVKA)

            elif message.text == "FAQ":
                self.bot.send_message(chat_id, BotMessange.FAQ,
                                      reply_markup=get_keyboard_faq())

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)

            # Не авторизированные пользователи
            if not user_data:
                if message.text == "Студент":
                    self.bot.send_message(chat_id, BotMessange.GROUP_REMIND)

                elif message.text == "Преподователь":
                    user_id = message.chat.id
                    phone_number = message.contact.phone_number if message.contact else "0"
                    name = parse_name_from_message(message)
                    DB().add_student(user_id, name, "teacher", phone_number, "teacher")

                    self.bot.send_message(chat_id, BotMessange.WELCOME_MSG.format(user_data["username"]))

                elif message.text == "Абитуриент":
                    user_id = message.chat.id
                    name = parse_name_from_message(message)
                    phone_number = message.contact.phone_number if message.contact else "0"

                    DB().add_student(user_id, name, "applicant", phone_number, "applicant")

                    self.bot.send_message(chat_id, BotMessange.WELCOME_MSG.format(name))

                elif is_group(message.text):
                    user_id = message.chat.id
                    name = parse_name_from_message(message)
                    phone_number = message.contact.phone_number if message.contact else "0"

                    DB().add_student(user_id, name, message.text, phone_number, "student")

                    self.bot.send_message(chat_id, BotMessange.WELCOME_MSG.format(name))

                else:
                    self.bot.send_message(chat_id, BotMessange.UNREGISTER_USER)
            # обработка всех сообщений студентов
            elif user_data["role"] == "student":
                if message.text == "Расписание":
                    self.send_schedule(chat_id, user_data, schedule_date="0")
                else:
                    self.bot.send_message(chat_id, "Sorry, I didn't understand that.")

            # Обработка всех сообщений преподователей
            elif user_data["role"] == "teacher":
                if message.text == "Расписание":
                    self.send_schedule(chat_id, user_data, schedule_date="0")
                else:
                    self.bot.send_message(chat_id, "Sorry, I didn't understand that.")

            # Обработка всех сообщений абитуриентов
            elif user_data['role'] == "applicant":
                if message.text == "Расписание":
                    self.send_schedule(chat_id, user_data, schedule_date="0")
                else:
                    self.bot.send_message(chat_id, "Sorry, I didn't understand that.")

            # Обработка всех сообщений админов
            elif user_data['role'] == "admin":
                if message.text == "Расписание":
                    self.send_schedule(chat_id, user_data, schedule_date="0")
                else:
                    self.bot.send_message(chat_id, "Sorry, I didn't understand that.")

    def send_schedule(self, chat_id, user_data, group=None, schedule_date=None):
        self.bot.send_message(chat_id, "Расписание для группы {}".format(user_data["group"]))
        try:
            msg = SchedulePage(group=user_data["group"], date=schedule_date).get_messange()
            for line in msg:
                self.bot.send_message(chat_id, line, parse_mode="HTML",
                                      reply_markup=get_schedule_keyboard())
        except:
            self.bot.send_message(chat_id, BotMessange.SCHEDULE_ERROR)
            self.bot.send_message(chat_id, BotMessange.GROUP_HELP, parse_mode="HTML")


if __name__ == '__main__':
    bot_token = 'API_KEY'
    my_bot = AsuBot(bot_token)
    my_bot.bot.polling(none_stop=True, interval=0)
