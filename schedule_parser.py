import requests
from bs4 import BeautifulSoup as bs
import re
from datetime import datetime, timedelta


def get_week_range():
    date_format = '%Y%m%d'
    current_date = datetime.now()

    current_week_start = current_date - timedelta(days=current_date.weekday())
    current_week_end = current_week_start + timedelta(days=6)

    last_week_end = current_week_start - timedelta(days=1)
    last_week_start = last_week_end - timedelta(days=6)

    return {
        "0": "",
        "-1": last_week_start.strftime(date_format) + '-' + last_week_end.strftime(date_format),
        "1": current_week_start.strftime(date_format) + '-' + current_week_end.strftime(date_format)
    }


def is_group(message):
    pattern = r"\d{1,3}(?:\.\d{3}(?:-\d)?|\.\d{3}М|)"
    if re.match(pattern, message):
        return True
    else:
        return False


class SchedulePage:
    def __init__(self, inc: str = "19", group: str = "508", date="0"):
        self.inc = inc
        self.group = group
        self.group_list_url = "https://www.asu.ru/timetable/students/{}/".format(self.inc)
        self.groups = self.parse_groups()
        self.group_id = self.groups[group]
        self.date = get_week_range()
        self.url = "https://www.asu.ru/timetable/students/{0}/{1}?date={2}".format(self.inc, self.group_id, self.date[date])

    def prepare_url(self, inc: str, group: str):
        if inc is None:
            inc = self.inc

        if group is None:
            group = self.group

        return "https://www.asu.ru/timetable/students/{}/{}/".format(inc, self.groups[group])

    def get_group_list_page(self):
        return requests.get(self.group_list_url).text

    def get_schedule_page(self):
        print(self.url)
        return requests.get(self.url).text

    def parse_groups(self):
        page = self.get_group_list_page()
        soup = bs(page, 'html.parser')
        list_items = soup.findAll("a", class_="list-item-link")
        groups_array = {}
        for item in list_items:
            groups_array.update({item.text: item["href"]})

        return groups_array

    def parse_by_child(self, date: str = None, custom_url: str = None):
        page = self.get_schedule_page()

        soup = bs(page, 'html.parser')
        table = soup.findAll("div", class_="schedule_table-body-rows_group")
        result = []
        for day in table:
            date = day.findChild(class_="schedule_table-cell schedule_table-body-rows_group-cell")
            date_text = " ".join(date.text.split()[0:2])

            lesson_group = day.findChild('div', class_="schedule_table-body-rows_group-rows")
            lessons = lesson_group.findAll('div', class_="schedule_table-body-row")
            less = []
            for tags in lessons:

                if "schedule_table-body-row__dropdown" not in tags['class']:
                    lesson = {}
                    cell = tags.findAll('div', class_="schedule_table-cell schedule_table-body-cell")
                    for i in cell:
                        lesson.update({i["data-type"]: i.text.split()})
                    try:
                        room = tags.find('div', class_="schedule_table-cell schedule_table-body-cell "
                                                       "schedule_table-body-cell__with_ptr")
                        lesson.update({"room": room.text.split()})
                    except:
                        lesson.update({"room": "Дистант"})

                    less.append(self.prepare_dict(lesson))

            result.append({date_text: less})
        return result

    @staticmethod
    def prepare_dict(d: dict):
        """
        :param d: is dict with lesson data
        :return: prepared dict
        """
        day_dict = {"сб": "суббота", "пн": "понедельник"}
        d['num'] = ' '.join(d['num'])
        d['time'] = ' '.join(d['time'])
        d['subject'] = ' '.join(d['subject'])
        d['lecturer'] = ' '.join(d['lecturer'])
        d['room'] = ' '.join(d['room'])

        return d

    def rebuild_day(self, day: str):
        day_dict = {"пн": "понедельник ",
                    "вт": "вторник ",
                    "ср": "среда ",
                    "чт": "четверг ",
                    "пт": "пятница ",
                    "сб": "суббота ",
                    "вс": "воскресенье "}

        return day_dict[day[0:2]] + day.split(' ')[1]

    def get_messange(self):
        head_messange = """<b>{}</b>"""
        day_messange = """\n<b>{}) {}</b> {} {} {}\n"""
        day_messange_ab = """\n<b>{}) {}</b> \n {} {} {} \n{}{} {} {} {}\n"""
        schedule = self.parse_by_child()
        for days in schedule:
            for day_name in days.keys():
                msg = head_messange.format(self.rebuild_day(day_name).upper())
                for index, lesson in enumerate(days[day_name]):
                    if index < len(days[day_name]) - 1:
                        if days[day_name][index + 1]["num"] == "" and lesson["num"].isnumeric():
                            lesson_a = lesson
                            lesson_b = days[day_name][index + 1]
                            msg += day_messange_ab.format(*lesson_a.values(), *lesson_b.values())
                        elif lesson["num"].isnumeric():
                            msg += day_messange.format(*lesson.values())
                    elif lesson["num"].isnumeric():
                        msg += day_messange.format(*lesson.values())
                yield msg


if __name__ == '__main__':
    final_messange = """"""
    day_messange = """{} {} {} {} {}"""
    sp = SchedulePage('508')
    # for msg in sp.get_messange():
    #     print(msg)
    print(len(sp.parse_groups().keys()))

    for key in sp.parse_groups().keys():
        print(key, is_group(str(key)))
        print("507", is_group("507"))

#'5.101', '5.101М', '5.103', '5.103М', '5.105-1', '5.105-2(у)', '5.105М', '5.107-1', '5.107-2', '5.107-3', '5.107М', '5.109М', '5.201', '5.201М', '5.203', '5.203М', '5.205-1', '5.205-2', '5.205М', '5.206М', '5.207-1', '5.207-2', '5.207-3', '5.207М', '5.209М', '501', '501М', '503', '505', '506', '507', '508', '581', '583М', '591', '593', '595', '597', '598'