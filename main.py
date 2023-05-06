import telebot
import re

import schedule_parser
from message import BotMessange
from keyboards import Keyboards
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


class AsuBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

        @self.bot.message_handler(commands=["help"])
        def send_help(message):
            chat_id = message.chat.id
            if DB().is_admin(chat_id):
                self.bot.send_message(chat_id, BotMessange.ADMIN_HELP)
            else:
                self.bot.send_message(chat_id, BotMessange.HELP, reply_markup=Keyboards.get_keyboard_faq())

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)
            if user_data:
                self.bot.send_message(chat_id, BotMessange.WELCOME_MSG.format(parse_name_from_message(message)),
                                      reply_markup=Keyboards.get_keyboard_menu())
            else:
                self.bot.send_message(chat_id, BotMessange.WELCOME_ASK,
                                      reply_markup=Keyboards.get_role_keyboard())

        @self.bot.message_handler(commands=['me'])
        def send_me_message(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)
            if user_data:

                self.bot.send_message(chat_id, BotMessange.ABOUT_USER.format(user_data["id"],
                                                                             parse_name_from_message(message),
                                                                             user_data["group"],
                                                                             user_data["phone_number"],
                                                                             user_data["role"]), parse_mode="HTML")
            else:
                self.bot.send_message(chat_id, BotMessange.WELCOME_HELP_MSG,
                                      reply_markup=Keyboards.get_role_keyboard())

        @self.bot.message_handler(commands=["update_group"])
        def send_update_group(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)
            group = message.text.strip("/update_group ")
            print(group)
            if user_data and is_group(group):
                DB().update_user_group_by_id(chat_id, group)

                self.bot.send_message(chat_id, BotMessange.DATA_UPDATE)

                user_data = DB().get_user(chat_id)
                self.bot.send_message(chat_id, BotMessange.ABOUT_USER.format(user_data["id"],
                                                                             parse_name_from_message(message),
                                                                             user_data["group"],
                                                                             user_data["phone_number"],
                                                                             user_data["role"]), parse_mode="HTML")
            else:
                self.bot.send_message(chat_id, BotMessange.GROUP_HELP,
                                      reply_markup=Keyboards.get_role_keyboard(),
                                      parse_mode="HTML")

        @self.bot.message_handler(commands=["get_all"])
        def admin_send_all_users(message):
            chat_id = message.chat.id
            users = DB().get_all()
            if DB().is_admin(chat_id):
                for user_data in users:
                    self.bot.send_message(chat_id, BotMessange.ABOUT_USER.format(user_data["id"],
                                                                                 parse_name_from_message(message),
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
            self.bot.send_message(message.chat.id, "Меню", reply_markup=Keyboards.get_keyboard_menu())

        @self.bot.message_handler(func=lambda message: message.text in BotMessange.SCHEDULE)
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

        @self.bot.message_handler(func=lambda message: message.text in BotMessange.FAQ_TEXT)
        def handle_start_navigation(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)

            if user_data is None:
                return 0

            if message.text == BotMessange.FAQ_TEXT[0]:
                self.bot.send_message(chat_id, BotMessange.LOST_CART)

        @self.bot.message_handler(func=lambda message: message.text in BotMessange.START_TEXT)
        def handle_start_navigation(message):
            chat_id = message.chat.id
            user_data = DB().get_user(chat_id)

            if user_data is None:
                return 0

            if message.text == BotMessange.START_TEXT[0]:
                self.send_schedule(chat_id, user_data, schedule_date="0")

            elif message.text == BotMessange.START_TEXT[1]:
                self.bot.send_message(chat_id, BotMessange.SPAVKA)

            elif message.text == BotMessange.START_TEXT[2]:
                self.bot.send_message(chat_id, BotMessange.DOMINTORY)

            elif message.text == BotMessange.START_TEXT[3]:
                self.bot.send_message(chat_id, BotMessange.CONTACT, parse_mode="HTML")

            elif message.text == BotMessange.START_TEXT[4]:
                self.bot.send_message(chat_id, BotMessange.FAQ,
                                      reply_markup=Keyboards.get_keyboard_faq())

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

                    self.bot.send_message(chat_id, BotMessange.WELCOME_MSG.format(name))

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
                if message.text == BotMessange.START_TEXT[0]:
                    self.send_schedule(chat_id, user_data, schedule_date="0")
                else:
                    self.bot.send_message(chat_id, BotMessange.ERROR)

            # Обработка всех сообщений преподователей
            elif user_data["role"] == "teacher":
                if message.text == BotMessange.START_TEXT[0]:
                    self.send_schedule(chat_id, user_data, schedule_date="0")
                else:
                    self.bot.send_message(chat_id, BotMessange.ERROR)

            # Обработка всех сообщений абитуриентов
            elif user_data['role'] == "applicant":
                if message.text == BotMessange.START_TEXT[0]:
                    self.send_schedule(chat_id, user_data, schedule_date="0")
                else:
                    self.bot.send_message(chat_id, BotMessange.ERROR)

            # Обработка всех сообщений админов
            elif user_data['role'] == "admin":
                if message.text == BotMessange.START_TEXT[0]:
                    self.send_schedule(chat_id, user_data, schedule_date="0")
                else:
                    self.bot.send_message(chat_id, BotMessange.ERROR)

    def send_schedule(self, chat_id, user_data, group=None, schedule_date=None):
        self.bot.send_message(chat_id, "Расписание для группы {}".format(user_data["group"]))
        try:
            msg = SchedulePage(group=user_data["group"], date=schedule_date).get_messange()
            for line in msg:
                self.bot.send_message(chat_id, line, parse_mode="HTML",
                                      reply_markup=Keyboards.get_schedule_keyboard())
        except:
            self.bot.send_message(chat_id, BotMessange.SCHEDULE_ERROR)
            self.bot.send_message(chat_id, BotMessange.GROUP_HELP, parse_mode="HTML")


if __name__ == '__main__':
    bot_token = '1913038657:AAGBUpXae9gnCOka4Kz0xKCQ2t_n1TiFhZA'
    my_bot = AsuBot(bot_token)
    my_bot.bot.polling(none_stop=True, interval=0)
