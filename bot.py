import config
import telebot, datetime
from telebot import types
from parse import get_schedule
bot = telebot.TeleBot(config.token)
now = datetime.datetime.now()
@bot.message_handler(commands=['start'])
def start(message):
    if message.text == '/start':
        print(message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
        now)
        bot.send_message(message.from_user.id, "Напиши мне номер своей группы");
        bot.register_next_step_handler(message, get_group);
    else:
        bot.send_message(message.from_user.id, 'Для начала выбери или напиши команду "/start"')


def get_group(message):
    group = int(message.text)
    schedule, date = get_schedule(group)
    print(date)
    date_index = 0
    for d in date:
        today = d.find('сегодня')
        if today != -1:
            bot.send_message(message.from_user.id, date[date_index])
            for i in range(len(schedule[date_index])):
                bot.send_message(message.from_user.id, schedule[date_index][i], parse_mode='Markdown')
        date_index += 1


bot.polling()
