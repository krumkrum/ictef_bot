import telebot
import re
import db
from telebot import types

text_help = """Этот создан для помощи студентам"""
text_contact = """
Сайт ИЦТЭФ: phys.asu.ru  
Vk: https://vk.com/ictef74 
Адрес: г. Барнаул, пр. Красноармейский, 90, ауд. 306.\n  
Почтовый адрес: 656049 г. Барнаул, пр. Ленина, 61.\n
Телефоны:  
Дирекция:\n+7(3852)29-12-24\n
Кафедра Общей и экспериментальной физики: +7(3852)296-659\n  
Кафедра Радиофизики и теоретической физики: +7(3852)296-668\n  
Кафедра Информационной безопасности: +7(3852)296-656\n
Кафедра ВТиЭ: +7(3852)296-644  

E-mail:  
• Директор - Макаров Сергей Викторович  makarov@phys.asu.ru  
• Заместитель по учебной работе - Белозерских Василий Вениаминович  bww@phys.asu.ru  
• Заместитель по внеучебной работе - Ладыгин Павел Сергеевич    pavel-ladygin@yandex.ru  
• Cпециалист по учебно-методической работе — Чичварина Наталья Юрьевна  chichvarina@phys.asu.ru
"""
text_priezd = """Уважаемый студент! 
 
В этом году продолжается особенный способ въезда в РФ, поэтому будь внимателен.  
 
Перед приездом в Россию необходимо не менее чем за 7 дней до прибытия в РФ написать Ладыгину Павлу Сергеевичу (заместитель директора по внеучебной работе) письмо на почту pavel-ladygin@yandex.ru с информацией: 
 
1. ФИО на русском и латиннице  
2. Дата рождения  
3. Номер серия документа, по которому будет осуществлен въезд  
4. Гражданство  
5. Предполагаемая дата прибытия  
6. Нуждаетесь или нет в общаге для изоляции и последующего проживания в ней. 
 
После отправки письма на электронную почту необходимо дождаться ответа от Ладыгина П.С. с согласованием даты въезда в РФ и возможности проживания в общежитиях студенческого городка АлтГУ.
 
Для пересечения границы вам может понадобиться справка об обучении в АлтГУ. Закажите её в дирекции у Чичвариной Натальи Юрьевны. Её контакт chichvarina@phys.asu.ru .
 
Не ранее чем за 3 календарных дня до прибытия в Россию студенту необходимо сдать тест на COVID-19 методом ПЦР и, если результат отрицательный, получить в своей стране соответствующий документ на русском или английском языке.  
  
В течение 72 часов после въезда на территорию России иностранные обучающиеся должны сдать повторный ПЦР-тест. До получения результатов теста им необходимо соблюдать режим самоизоляции по месту проживания.   
  
Справочно сообщаем контактные данные центров, осуществляющих лабораторные исследования на COVID-19 методом ПЦР в г. Барнауле:  
  
1. ДНК-Диагностика +7 (3852) 289-060  
2. Хелми +7 (3852) 56-01-03  
3. Инвитро 8 800 200 3630  
  
После получения отрицательного результата повторного теста на COVID-19 немедленно (в течении одного рабочего дня) студенту необходимо явиться в Управление международной деятельности АлтГУ (пр-т Ленина, д. 61, каб. 400, тел. +7 (3852) 291-253) для получения справки о допуске к очному обучению и оформления документов для постановки на миграционный учет.  
  
Вакцинация иностранных студентов от Covid-19 носит рекомендательный характер, при этом все иностранные студенты, получившие справку о допуске к учебным занятиям, смогут начать учебный год в очном режиме.  
  
Также дополнительно сообщаем, что в случае невозможности очного прибытия учебный год возможно начать в удаленном формате с использованием дистанционных образовательных технологий. 
 
По поводу изоляции. 
 
На сегодняшний день мы не знаем официальных дат заселения в общежитие для нашего института.  
 
Какие варианты проведения изоляции до получения результатов теста есть? 
- У кого-то на квартире. 
- В хостеле (можем дать контакты, около 500 р/сутки) 
- В общежитии №5 университета (бесплатно, но всего - 6 мест, что делает невозможным приезд всех в одно время) 
 
Просьба учитывать это при планировании приезда в РФ. 
 
ВНИМАНИЕ! Для заселения в общежитие потребуются дополнительные документы! Об этом будет сообщено дополнительно в пункте меню "Заселение в общежитие" телеграм-бота ИЦТЭФ.
"""
text_domintory = """Студенты ИЦТЭФ живут в Общежитии №4 по адрессу ул. Крупской д.103. 
Общежитие секционного типа, студенты проживают по 2-3 человека в комнатах. В каждой секции: 4 жилых комнаты, душ, туалет, кухня. 
В течении года работают: учебная комната, актовый зал, теннисный зал, а так же бытовые комнаты: постирочная, гладильная и комната для сушки белья.

Стоимость проживания 1132р/мес. для бюджетного набора 1532р/мес. для дополнительного набора.

Если у Вас возникли вопросы касаемые общежития можете обратиться к председателю студенческого совета (ПСС) ИЦТЭФ Попыкину Вадиму Андреевичу vk.com/fakstor 
Fakstor001@ya.ru (в теме письма указать "ИЦТЭФ")
"""
text_in_domintory = """Уважаемые студенты!  
 
В этом году обновлен список документов к заселению. Просьба отнестись внимательно к их наличию.  
  
С 18 августа ожидайте звонка, с Вами свяжутся председатель студенческого совета Попыкин Вадим Андреевич или помощник Прокопенко Анастасия Сергеевна, которые назначат дату и время вашего прибытия в корпус университета по адресу Красноармейский, 90 (корпус «К» АлтГУ). 
  
Чтобы заселение прошло как можно быстрее, вам потребуется для медкомиссии:  
  
1. Ксерокопия паспорта (2-3, 4-5 страница) и оригинал;  
2. Ксерокопия прививочного сертификата и оригинал;  
3. Ксерокопия полиса ОМС и оригинал;  
4. Ксерокопия пенсионного страхового свидетельства (СНИЛС) и оригинал;  
5. Результат флюорографического обследования со штампом медицинского учреждения (действителен в течение года);  
6. Девушкам справку от гинеколога (действительна в течение 10 дней) со следующим оформлением: штамп медицинского учреждения, подпись и личная печать врача, печать для справок.  
7. Фото 3х4 для оформления пропуска в общежитие.  
  
План заселения следующий:  
  
1. Вы приходите в корпус университета в назначенный день и час (не нужно приходить заранее!!!).  
2. В назначенной аудитории будет организовано заполнение документов, которые мы вам предоставим.  
3. Далее вы пройдёт инструктаж у заместителя директора по внеучебной и воспитательной работе Ладыгина Павла Сергеевича и направитесь за подписями: 
  
1) Здравпункт (ул. Крупской, 103)  
2) Бухгалтерия (606М, Ленина, 61 — Главный корпус АлтГУ);  
3) Касса (первый этаж, Ленина, 61 — Главный корпус АлтГУ);  
4) Студенческий городок (второй этаж, 215М, Ленина, 61 — Главный корпус АлтГУ);  
5) Для иностранных граждан — Международный отдел (400М, Ленина, 61 — Главный корпус АлтГУ);  
6) Студенческое общежитие (заведующая общежитием, ул. Крупской, 103).  
  
Стоимость проживания в общежитии для бюджетного набора — 1132 р. / мес., для дополнительного набора — 1532 р./мес. Даты найма помещения (по умолчанию) — 01.09.2020-30.06.2021 (10 месяцев).  
  
Возможна оплата через банк. Скоро прикрепим инструкцию.  
  
Оплачивается весь указанный период проживания. 
 
ВНИМАНИЕ! Возможны изменения. Следите.
"""
text_faq = """Какой вопрос у тебя возник?"""
text_vacin = """На сегодняшний день вакцинация студентов от Covid-19 носит рекомендательный характер. Каждый из вас должен принять решение самостоятельно. Однако, ситуация может меняться.

Старосты групп скоро начнут собирать информацию о том, кто уже  привился или собирается это сделать. Это необходимо просто для справки.

Практически все преподаватели и сотрудники нашего института и университета уже привились.
"""
text_lost_cart = """
ЧТО ДЕЛАТЬ, ЕСЛИ ПОТЕРЯЛ ЗАЧЁТКУ ИЛИ СТУДЕНЧЕСКИЙ БИЛЕТ

1. Выяснить номер документа. Помните, что у студенческого билета и зачетной книжки он один и тот же. В самом крайнем-крайнем случае его можно узнать в деканате/дирекции.  
2. Прийти (написать, позвонить) в редакцию газеты «За науку», чтобы подать объявление о том, что данный документ недействителен.  
Адрес: natapisma7@gmail.com (в теме обязательно укажите: «Тоска объявлений»),  
Телефон редакции: 29-12-60. 
3. Дождаться публикации. Взять свежий номер «ЗН» и перечитать его от корки до корки. 
4. Показать объявление о недействительности документа в деканате/дирекции своего института.  
5. Дождаться восстановления документа.
"""
text_admin_help = """/add idtelegram НомерГруппы УровеньОбразования Курс - добавление пользователя\n id - идентификатор пользователя получить из /me \n номер группы \n уровень образования \n курс обучения

# 0 - None
# 1 - Бакалавр
# 2 - Магистр
# 3 - Аспирант
# 4 - Админ

Например:
/add 13124125 598 1 3
Добавление бакалавра 3 курса из 598 группы

Рассылка сообщений 
/resend_g по группам
/resend_le по уровню образования
/resend_c по курсам
/resend всем
"""

# Родной
# 1913038657:AAGBUpXae9gnCOka4Kz0xKCQ2t_n1TiFhZA
bot = telebot.TeleBot('698328096:AAGj3J9OxEi0DeLCjYpaka3uHor67rd0oOg')

OBR = ['None', 'Бакалавр', 'Магистр', 'Аспирант', 'Админ']
groups = ['all', 'master', 'bachelor', 'infsec', 'ivt', 'rphys', 'phys']
start_text = ['Расписание', 'Приезд в РФ 2021', 'Общежитие', 'Контакты', 'FAQ']
faq_text = ['Вакцинация', 'Потерял студенческий/зачетку']
dom_text = ["Заселение"]

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
        bot.send_message(message.chat.id, text_admin_help)


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
        bot.send_message(message.chat.id, 'Пожалуйста за реплайте сообщение, которое хотите переслать')


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
        bot.send_message(message.chat.id, 'Пожалуйста за реплайте сообщение, которое хотите переслать')


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
        bot.send_message(message.chat.id, 'Пожалуйста за реплайте сообщение, которое хотите переслать')

@bot.message_handler(commands=['resend'])
def resender_to_all(message):
    if not (message.chat.id in ADMINS):
        return 1

    g = db.DB().get_all_student()

    if message.reply_to_message:
        for i in g:
            bot.forward_message(i, message.chat.id, message.reply_to_message.message_id)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста за реплайте сообщение, которое хотите переслать')


# Реакция на текст
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == "Назад":
        bot.send_message(message.chat.id, "Меню", reply_markup=markstart)

    # Приезд в рф2021
    elif message.text == start_text[1]:
        bot.send_message(message.chat.id, text_priezd)

    # Общежитие
    elif message.text == start_text[2]:
        bot.send_message(message.chat.id, text_domintory, reply_markup=markdomintory)

    # Контакты
    elif message.text == start_text[3]:
        bot.send_message(message.chat.id, text_contact)

    # FAQ
    elif message.text == start_text[4]:
        bot.send_message(message.chat.id, text_faq, reply_markup=markfaq)

    # Расписание
    elif message.text == start_text[0]:
        bot.send_message(message.chat.id, "В работе")

    # Вакцинация
    elif message.text == faq_text[0]:
        bot.send_message(message.chat.id, text_vacin)

    # Потерял студент/зачетку
    elif message.text == faq_text[1]:
        bot.send_message(message.chat.id, text_lost_cart)

    # Общежитие
    elif message.text == dom_text[0]:
        bot.send_message(message.chat.id, text_in_domintory)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
