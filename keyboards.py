from telebot import types
from message import *

class Keyboards:

    @staticmethod
    def get_role_keyboard():
        keyboard = types.ReplyKeyboardMarkup(row_width=len(BotMessange.ROLE))
        keyboard.add(*[types.KeyboardButton(role.capitalize()) for role in BotMessange.ROLE])
        keyboard.add(types.KeyboardButton("Назад"))
        return keyboard

    @staticmethod
    def get_keyboard_menu():
        keyboard = types.ReplyKeyboardMarkup(row_width=len(BotMessange.START_TEXT))
        for btn in BotMessange.START_TEXT:
            keyboard.add(types.KeyboardButton(btn))
        keyboard.add(types.KeyboardButton("Назад"))
        return keyboard

    @staticmethod
    def get_keyboard_faq():
        keyboard = types.ReplyKeyboardMarkup(row_width=len(BotMessange.FAQ_TEXT))
        for btn in BotMessange.FAQ_TEXT:
            keyboard.add(types.KeyboardButton(btn))
        keyboard.add(types.KeyboardButton('Назад'))
        return keyboard

    @staticmethod
    def get_keyboard_domintory():
        markdowns = types.ReplyKeyboardMarkup()
        for btn in BotMessange.DOM_TEXT:
            markdowns.add(types.KeyboardButton(btn))
        markdowns.add(types.KeyboardButton('Назад'))
        return markdowns

    @staticmethod
    def get_schedule_keyboard():
        keyboard = types.ReplyKeyboardMarkup(row_width=3)
        keyboard.add(*[types.KeyboardButton(btn) for btn in BotMessange.SCHEDULE])
        keyboard.add(types.KeyboardButton("Назад"))
        return keyboard