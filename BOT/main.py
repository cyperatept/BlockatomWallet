#!/usr/bin/python

# |---------------------------------------------CODED BY @SENSORDS---------------------------------------------|

import re
import json
import telebot
import sqlite3
import requests
from bit import *
import qrcode as qrcode
from config import TOKEN
from telebot import types
from bs4 import BeautifulSoup
from core import generic_address

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    db = sqlite3.connect('wallet_users.db')
    curs = db.cursor()
    curs.execute(f"SELECT * FROM users WHERE ID = {message.from_user.id}")
    data = curs.fetchone()
    if data is None:
        bot.send_message(message.chat.id, text='*Welcome to Blockatom wallet in Telegram,\nIt\'s decentralised bitcoin wallet.\n\nWant to create a wallet?\n\n*Blockatom-wallet.com', reply_markup=keyboardreg(), parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, text='*Welcome back*', reply_markup=keyboard(),parse_mode="Markdown")

def keyboard():
    keyboard_1 = telebot.types.ReplyKeyboardMarkup(True)
    Walletk = types.KeyboardButton('Wallet')
    sendk = types.KeyboardButton('Send')
    receivek = types.KeyboardButton('Receive')
    aboutk = types.KeyboardButton('About Us')
    infok = types.KeyboardButton('Information')
    keyboard_1.add(Walletk)
    keyboard_1.add(sendk, receivek)
    keyboard_1.add(aboutk)
    keyboard_1.add(infok)
    return keyboard_1

def keyboardreg():
    keyboard_reg = telebot.types.ReplyKeyboardMarkup(True)
    Createk = types.KeyboardButton('Create')
    Nocreatek = types.KeyboardButton('No create')
    keyboard_reg.add(Createk, Nocreatek)
    return keyboard_reg

@bot.message_handler(content_types=['text'])
def logic_bot(message):
    db = sqlite3.connect('wallet_users.db')
    curs = db.cursor()
    if message.text == 'Create':
        curs.execute(f"SELECT * FROM users WHERE ID = {message.from_user.id}")
        data = curs.fetchone()
        if data is None:
            sql = "SELECT COUNT(*) FROM users "
            curs.execute(sql)
            user = curs.fetchone()
            address, wif = generic_address(user[0]+1)
            curs.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",(message.from_user.id, message.from_user.first_name, address, wif, 0, 0))
            bot.send_message(message.chat.id, text='*You have created a wallet*', reply_markup=keyboard(),parse_mode="Markdown")
            db.commit()
    if message.text == 'Receive':
        db = sqlite3.connect('wallet_users.db')
        curs = db.cursor()
        curs.execute(f"SELECT BTC_ADDRESS FROM users WHERE ID = {message.from_user.id}")
        adres = curs.fetchone()
        bot.send_message(message.chat.id, text='*Your Bitcoin address*', parse_mode='Markdown')
        bot.send_message(message.chat.id, adres[0], parse_mode='Markdown')
        img = qrcode.make(adres[0])
        img.save('qrcode.jpg')
        bot.send_photo(message.chat.id, photo=open('qrcode.jpg', 'rb'))
    if message.text == 'Wallet':
        db = sqlite3.connect("wallet_users.db")
        curs = db.cursor()
        sss = f"SELECT BTC_ADDRESS FROM users WHERE ID = {message.from_user.id}"
        curs.execute(sss)
        adres = curs.fetchone()
        url = f'https://www.blockchain.com/btc/address/{adres[0]}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
        Response = requests.get(url, headers=headers)
        wallet = BeautifulSoup(Response.content, 'html.parser')
        convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0", "class": "eQTRKC"})
        rx = convert[6].text
        TS = convert[5].text
        TR = convert[4].text
        response = requests.get(url="https://yobit.net/api/3/ticker/btc_usd")
        curs = response.text
        curs = json.loads(curs)
        x = (curs['btc_usd']['sell'])
        r = rx.rstrip('BTC')
        us = (x * float(r))
        bot.send_message(message.chat.id, text='🌐️Your Wallet🌐️\n\n'+ '*ID: *' + str(message.from_user.id) +'\n\n*TOTAL RECEIVE: *'+ str(TR) + '\n*TOTAL SEND: *' + str(TS) +'\n\n*BALANCE:* ' + str(rx) + ' ~ ' + str(us) + '$', parse_mode='Markdown')
    if message.text == 'Send':
        keyboard_2 = telebot.types.ReplyKeyboardMarkup(True)
        Backk = types.KeyboardButton('Back')
        keyboard_2.add(Backk)
        send = bot.send_message(message.chat.id, text='*Send BTC address where you want to send*',parse_mode='Markdown', reply_markup=keyboard_2)
        bot.register_next_step_handler(send, sends)
    if message.text == 'Back':
        keyboard_1 = telebot.types.ReplyKeyboardMarkup(True)
        Walletk = types.KeyboardButton('Wallet')
        sendk = types.KeyboardButton('Send')
        receivek = types.KeyboardButton('Receive')
        aboutk = types.KeyboardButton('About Us')
        infok = types.KeyboardButton('Information')
        keyboard_1.add(Walletk)
        keyboard_1.add(sendk, receivek)
        keyboard_1.add(aboutk)
        keyboard_1.add(infok)
        bot.send_message(message.chat.id, text='*You have returned to the main menu*', reply_markup=keyboard_1, parse_mode='Markdown')
    if message.text == 'Information':
        bot.send_photo(message.chat.id, photo=open('desk.png', 'rb'))
        bot.send_message(message.chat.id, text='You can also use our PC shell\nfor a more convenient, secure and complete use and management of your funds.\nDownload for Windows, MacOs or Linux - https://blockatom-wallet.com/download\n\nIn order to leave your wishes or ask for help, go to our technical support - @Blockatom_support')
        bot.send_message(message.chat.id, text='HOW TO USE DESKTOP BLOCKATOM WALLET? - https://youtu.be/tt_ddba_H5M')
    if message.text == 'About Us':
        bot.send_photo(message.chat.id, photo=open('site.png', 'rb'))
        bot.send_message(message.chat.id, text='We provide a completely independent environment\nwhere you can store bitcoin, transfer and receive.\n\nVisit our website to learn more about our product.\nhttps://blockatom-wallet.com')
    if message.text == 'No create':
        bot.send_message(message.chat.id, text='*You have not created a wallet, to create a wallet click /start*', parse_mode='Markdown')

def sends(message):
    result = re.match(r'^(?=.*[0-9])(?=.*[a-zA-Z])[\da-zA-Z]{27,42}$', message.text)
    if message.text != 'Back':
        if result is None:
            send2 = bot.send_message(message.chat.id, text="*Check that BTC wallet is entered correctly*",parse_mode="Markdown")
            bot.register_next_step_handler(send2, sends)
        else:
            db = sqlite3.connect('wallet_users.db')
            curs = db.cursor()
            curs.execute(f"UPDATE users SET BTC_SEND = '{message.text}' WHERE ID = '{message.from_user.id}'")
            db.commit()
            summ = bot.send_message(message.chat.id,text='*Send the BTC value you want to send*\n_For example 0.00010000_',parse_mode='Markdown')
            bot.register_next_step_handler(summ, summd)
    if message.text == 'Back':
        keyboard()
        bot.send_message(message.chat.id, text='*You have returned to the main menu*', reply_markup=keyboard(),parse_mode='Markdown')

def summd(message):
    if message.text != 'Back':
        if len(message.text) > 10:
            amount = bot.send_message(message.chat.id, text='*Check the correctness of the indicated amount*', parse_mode='Markdown')
            bot.register_next_step_handler(amount, summd)
        if len(message.text) < 10:
            amount = bot.send_message(message.chat.id, text='*Check the correctness of the indicated amount*',parse_mode='Markdown')
            bot.register_next_step_handler(amount, summd)
        else:
            db = sqlite3.connect('wallet_users.db')
            curs = db.cursor()
            curs.execute(f"UPDATE users SET AMOUNT = '{message.text}' WHERE ID = '{message.from_user.id}'")
            db.commit()
            keyboard_1 = telebot.types.ReplyKeyboardMarkup(True)
            minimalk = types.KeyboardButton('Minimal ~ (0.00001 BTC)')
            preorityk = types.KeyboardButton('Preority ~ (0.0002 BTC)')
            keyboard_1.add(minimalk, preorityk)
            fee = bot.send_message(message.chat.id, text='*Select fees*', reply_markup=keyboard_1, parse_mode='Markdown')
            bot.register_next_step_handler(fee, feeandsend)
    if message.text == 'Back':
        keyboard()
        bot.send_message(message.chat.id, text='*You have returned to the main menu*', reply_markup=keyboard(),parse_mode='Markdown')

def feeandsend(message):
    try:
        if message.text == 'Minimal ~ (0.00001 BTC)':
            db = sqlite3.connect('wallet_users.db')
            curs = db.cursor()
            sss = f"SELECT BTC_ADDRESS FROM users WHERE ID = {message.from_user.id}"
            curs.execute(sss)
            adres = curs.fetchone()
            url = f'https://www.blockchain.com/btc/address/{adres[0]}'
            db.commit()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
            Response = requests.get(url, headers=headers)
            wallet = BeautifulSoup(Response.content, 'html.parser')
            convert = wallet.findAll("span",{"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
            rx = convert[6].text
            xx = rx.rstrip('BTC')
            curs = db.cursor()
            curs.execute(f"SELECT AMOUNT FROM users WHERE ID = {message.from_user.id}")
            SET = curs.fetchone()[0]
            if float(SET) + 0.00002000 <= float(xx):
                try:
                    curs.execute(f"SELECT wif FROM users WHERE ID = {message.from_user.id}")
                    wif = curs.fetchone()[0]
                    wifSTR = str(wif, encoding='utf-8')
                    wif_key = PrivateKey(wif=wifSTR)
                    fee = 2000
                    curs.execute(f"SELECT BTC_SEND FROM users WHERE ID = {message.from_user.id}")
                    sending = curs.fetchone()[0]
                    tx_hash = wif_key.create_transaction([(sending, float(SET), 'btc')], fee=fee, absolute_fee=True)
                    url = 'https://blockchain.info/pushtx'
                    x = requests.post(url, data={'tx': tx_hash})
                    result = x.text
                    keyboard_1 = telebot.types.ReplyKeyboardMarkup(True)
                    Walletk = types.KeyboardButton('Wallet')
                    sendk = types.KeyboardButton('Send')
                    receivek = types.KeyboardButton('Receive')
                    aboutk = types.KeyboardButton('About Us')
                    infok = types.KeyboardButton('Information')
                    keyboard_1.add(Walletk)
                    keyboard_1.add(sendk, receivek)
                    keyboard_1.add(aboutk)
                    keyboard_1.add(infok)
                    bot.send_message(message.chat.id, result, reply_markup=keyboard_1)
                except Exception:
                    keyboard_2 = telebot.types.ReplyKeyboardMarkup(True)
                    Backk = types.KeyboardButton('Back')
                    keyboard_2.add(Backk)
                    bot.send_message(message.chat.id, text='An error occurred while executing a transaction', reply_markup=keyboard_2)
            else:
                keyboard_2 = telebot.types.ReplyKeyboardMarkup(True)
                Backk = types.KeyboardButton('Back')
                keyboard_2.add(Backk)
                bot.send_message(message.chat.id, text='*Not enought coins*', parse_mode='Markdown', reply_markup=keyboard_2)
    except ValueError:
        bot.send_message(message.chat.id, text='Amount entered incorrectly')

    if message.text == 'Preority ~ (0.0002 BTC)':
        try:
            db = sqlite3.connect('wallet_users.db')
            curs = db.cursor()
            sss = f"SELECT BTC_ADDRESS FROM users WHERE ID = {message.from_user.id}"
            curs.execute(sss)
            adres = curs.fetchone()
            url = f'https://www.blockchain.com/btc/address/{adres[0]}'
            db.commit()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
            Response = requests.get(url, headers=headers)
            wallet = BeautifulSoup(Response.content, 'html.parser')
            convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
            rx = convert[6].text
            xx = rx.rstrip('BTC')
            curs = db.cursor()
            curs.execute(f"SELECT AMOUNT FROM users WHERE ID = {message.from_user.id}")
            SET = curs.fetchone()[0]
            if float(SET) + 20000 <= float(xx) / 100000000:
                try:
                    curs.execute(f"SELECT wif FROM users WHERE ID = {message.from_user.id}")
                    wif = curs.fetchone()[0]
                    wifSTR = str(wif, encoding='utf-8')
                    wif_key = PrivateKey(wif=wifSTR)
                    fee = 20000
                    curs.execute(f"SELECT BTC_SEND FROM users WHERE ID = {message.from_user.id}")
                    sending = curs.fetchone()[0]
                    tx_hash = wif_key.create_transaction([(sending, SET, 'btc')], fee=fee, absolute_fee=True)
                    url = 'https://blockchain.info/pushtx'
                    x = requests.post(url, data={'tx': tx_hash})
                    result = x.text
                    keyboard_1 = telebot.types.ReplyKeyboardMarkup(True)
                    Walletk = types.KeyboardButton('Wallet')
                    sendk = types.KeyboardButton('Send')
                    receivek = types.KeyboardButton('Receive')
                    aboutk = types.KeyboardButton('About Us')
                    infok = types.KeyboardButton('Information')
                    keyboard_1.add(Walletk)
                    keyboard_1.add(sendk, receivek)
                    keyboard_1.add(aboutk)
                    keyboard_1.add(infok)
                    bot.send_message(message.chat.id, result, reply_markup=keyboard_1)
                except Exception:
                    keyboard_2 = telebot.types.ReplyKeyboardMarkup(True)
                    Backk = types.KeyboardButton('Back')
                    keyboard_2.add(Backk)
                    bot.send_message(message.chat.id, text='An error occurred while executing a transaction',reply_markup=keyboard_2)
            else:
                keyboard_2 = telebot.types.ReplyKeyboardMarkup(True)
                Backk = types.KeyboardButton('Back')
                keyboard_2.add(Backk)
                bot.send_message(message.chat.id, text='*Not enought coins*', parse_mode='Markdown',reply_markup=keyboard_2)
        except ValueError:
            bot.send_message(message.chat.id, text='Amount entered incorrectly')

bot.polling(none_stop=True)
