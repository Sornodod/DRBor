import telebot
import pandas as pd
from datetime import datetime, timedelta
import time
import threading

API_TOKEN = 'ТЕЛЕГРАММ_ТОКЕН'
bot = telebot.TeleBot(API_TOKEN)

# Функция пидюривания в Excel.
def load_birthdays(file_path):
    df = pd.read_excel(file_path)
    df['Дата рождения'] = pd.to_datetime(df['Дата рождения'], dayfirst=True)
    return df

# Функция для проверки др и даты.
def check_birthdays(df):
    today = datetime.now().date()
    one_week_later = today + timedelta(days=7)
    today_birthdays = df[df['Дата рождения'].dt.date == today]
    week_birthdays = df[df['Дата рождения'].dt.date == one_week_later]
    return today_birthdays, week_birthdays

# Функция которая собственно и отправляет сообщения.
def send_messages(df):
    today_birthdays, week_birthdays = check_birthdays(df)

    # ID-шники чатов
    chat_id_today = ID_ЧАТА_ГДЕ_БОТ_БУДЕТ_ПОЗДРАВЛЯТЬ
    chat_id_week = ID_ЛС_ЧАТА_ГДЕ_БОТ_БУДЕТ_НАПОМИНАТЬ_ЧТО_У_ЧЕЛА_ЧЕРЕЗ_НЕДЕЛЮ_ДР

    # Пишет в общий чат поздравление с др.
    for index, row in today_birthdays.iterrows():
        message = f"Поздравляем {row['ФИО']} с днём рождения!"
        bot.send_message(chat_id_today, message)

    # Пишет тебе в лс у кого др через неделю.
    for index, row in week_birthdays.iterrows():
        message = f"Через неделю у {row['ФИО']} день рождения!"
        bot.send_message(chat_id_week, message)

birthdays_df = load_birthdays('birthdays.xlsx')

# Необязательная функция проверки даты 24х7. Это если бот будет работать круглосуточно, то он раз в сутки проверяет даты др.
def schedule_daily_check():
    while True:
        send_messages(birthdays_df)
        time.sleep(86400)

#Запуск ебатории в отдельной потоке.
daily_check_thread = threading.Thread(target=schedule_daily_check)
daily_check_thread.start()

bot.polling(none_stop=True)
