import pytz


def get_msc_date(utc_time):
    # Задаем московский часовой пояс
    moscow_tz = pytz.timezone('Europe/Moscow')
    # Переводим время в московский часовой пояс
    moscow_time = utc_time.astimezone(moscow_tz)
    return moscow_time

