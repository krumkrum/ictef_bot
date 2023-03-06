from datetime import datetime, timedelta


start_date = datetime.strptime('20230101', '%Y%m%d')
end_date = datetime.strptime('20231231', '%Y%m%d')

delta = timedelta(days=7)
week_start_dates = []
week_end_dates = []

while start_date <= end_date:
    week_start_dates.append(start_date)
    week_end_dates.append(start_date + timedelta(days=6))
    start_date += delta

for i in range(len(week_start_dates)):
    print(f"Week {i+1}: {week_start_dates[i].strftime('%Y%m%d')}-{week_end_dates[i].strftime('%Y%m%d')}")
# date_range.append((self.week_start.strftime('%Y%m%d'), self.week_end.strftime('%Y%m%d')))