from datetime import datetime, timedelta


def get_week_range():
    date_format = '%Y%m%d'
    current_date = datetime.now()

    current_week_start = current_date - timedelta(days=current_date.weekday())
    current_week_end = current_week_start + timedelta(days=6)

    last_week_end = current_week_start - timedelta(days=1)
    last_week_start = last_week_end - timedelta(days=6)

    return [
        last_week_start.strftime(date_format) + '-' + last_week_end.strftime(date_format),
        current_week_start.strftime(date_format) + '-' + current_week_end.strftime(date_format)
    ]


week_range = get_week_range()
print(week_range)
