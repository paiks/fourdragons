import telebot
import sqlite3
import os
import random

conn = sqlite3.connect("bob.db",check_same_thread = False)
cursor = conn.cursor()

bot = telebot.TeleBot('1051197481:AAE_FQc5oF6ZSdAf37jtA4jCNE-0A7lGtH0')

@bot.message_handler(commands=['start'])
def start_message(message):
    sender = message.from_user
    cursor.execute(f"""SELECT EXISTS(SELECT ID from users where ID={sender.id})""")
    temp_id=cursor.fetchone()
    print(temp_id)
    if temp_id[0]==0:
        cursor.execute(f"""INSERT INTO users VALUES ({sender.id}, 1000, 0)""")
        conn.commit()
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start и если ты новый пользователь то тебе начислено 1000 монет')

@bot.message_handler(commands=['bet'])
def bet(message):
    variants=['red','black']
    sender = message.from_user
    bet=int(message.text.split()[1])
    cursor.execute(f"""select money from users where ID = {sender.id}""")
    balance=cursor.fetchone()[0]
    if balance>=bet:
        type_bet=message.text.split()[2]
        egor_rab=random.choice(variants)
        bot.send_message(sender.id, f'Выпало {egor_rab}')
        if type_bet==egor_rab:
            bot.send_message(sender.id, f'Вы выиграли {bet} монет')
            cursor.execute(f"""update users set money = money + {bet} where ID = {sender.id}""")
            conn.commit()
        else:
            bot.send_message(sender.id, f'Вы проебали нахуй {bet} монет, как теперь платить ипотеку?')
            cursor.execute(f"""update users set money = money - {bet} where ID = {sender.id}""")
            conn.commit()

@bot.message_handler(content_types=['text'])
def balance_all(message):
    sender=message.from_user
    if message.text.lower()=='бонус':
        cursor.execute(f"""update users set money = money + {1000} where ID = {sender.id}""")
        conn.commit()
        bot.send_message(sender.id, 'Баланас пополнен на 1000')
    if message.text.lower()=='баланс':
        cursor.execute(f"""select money from users where ID = {sender.id}""")
        balance=cursor.fetchone()[0]
        bot.send_message(sender.id, f'Ваш баланс = {balance} монет')

bot.polling()
