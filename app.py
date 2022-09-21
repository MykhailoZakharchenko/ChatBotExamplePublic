import telebot
from telebot import types
import requests
import json
import chatbot.trackUsers as log
import time
import chatbot.imageClass as imgcl
token = 'link to token TG chatbot' # TODO: set your bot token
bot = telebot.TeleBot(token)
ws = open('WasteTypes.json')
global waste
waste_U = json.load(ws)


@bot.message_handler(commands=['start'])
def start(message):
    'welcome message'
    us = log.User(message.from_user.id,message.from_user.first_name,message.from_user.last_name,message.from_user.username,message.from_user.language_code) #Class initiation / Start of User logging
    checkUser = us.check_first_user()
    if checkUser:
        bot.send_message(message.chat.id, "Hi " + message.from_user.first_name + " 👋")
        bot.send_message(message.chat.id,"Send me waste pic👇")
    else:
        bot.send_message(message.chat.id, "Hi " + message.from_user.first_name + " 👋")
        bot.send_message(message.chat.id, 'I\'m Dandex, chatbot that recognizes waste, that can be recycable')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton('Ok 👌'))
        bot.send_message(message.chat.id,"I\'m still learning to recognize garbage, so if I don\'t recognize something correctly, please note it to me", reply_markup=markup)

@bot.message_handler()
def get_user_text(message):
    'recognize users text'
    if message.text == 'Ok 👌':
        bot.send_message(message.chat.id, "Great, I received a picture of your garbage, and I'll tell you if this garbage is suitable for recycling👇")
    elif message.text == 'Ok 🤷‍♂️':
            bot.send_message(message.chat.id,'Send me waste pic👇')
    elif message.text == 'Show️':
        mess = f"Id: {productInfo[0][0]}\n" \
               f"Country: {productInfo[0][1]}\n" \
               f"Producer: {productInfo[0][3]}\n" \
               f"Product: {productInfo[0][5]}\n" \
               f"Product code: {productInfo[0][6]}\n" \
               f"Brand: {productInfo[0][7]}\n" \
               f"Waste type: {productInfo[0][8]}\n" \
               f"Volume: {productInfo[0][9]} {''} {productInfo[0][10]}\n" \
               f"Category: {productInfo[0][11]}\n" \
               f"SubCategory: {productInfo[0][12]}\n"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton('Ok 🤷‍♂️'))
        bot.send_message(message.chat.id,mess,reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton('Ok 🤷‍♂️'))
        bot.send_message(message.chat.id,"Sorry, I don\'t understand you, try again",reply_markup=markup)

@bot.message_handler(content_types="photo")
def photo(message):
    'take all messages with photos and run it for detection'
    bot.send_message(message.chat.id, '\U000023F3')
    bot.send_message(message.chat.id,"Wait a second...")
    'get image link'
    imgTG = requests.get('https://api.telegram.org/bot'+token+'/getFile?file_id='+message.photo[-1].file_id)
    imgTG =json.loads(imgTG.text)
    waste = imgcl.ImageCl('https://api.telegram.org/file/bot' + token + '/' + imgTG['result']['file_path'])
    'read results'
    global productInfo
    wasteResult,productInfo = waste.Runner() #waste result -- recognized waste, product -- if CB detects barcode product
    if len(wasteResult) > 1: #decrypt waste
        bot.send_photo(message.chat.id, wasteResult[0]['url'],'Recognized the following:')
        for i in range(1, len(wasteResult)):
            if wasteResult[i]['name'] == 'Barcode':
                bot.send_message(message.chat.id, "Barcode ║█║▌║█║▌│║▌║▌█║, sure for "+wasteResult[i]['score'])
            else:
                getWasteType = next(d for d in waste_U if d['Type'] == wasteResult[i]['name'])
                if getWasteType['WasteCategory'] == 'Other':
                    bot.send_message(message.chat.id, "type " +wasteResult[i]['name']+", sure for " + wasteResult[i]['score'] +", not sure it can be recycled🥺")
                else:
                    bot.send_message(message.chat.id, "type " + wasteResult[i]['name'] + ", sure for " + wasteResult[i]['score'] + ", recyclable, meaning category "+getWasteType['WasteCategory'])

        if productInfo != None: #decrypt product
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            markup.row(types.KeyboardButton('Show️'))
            bot.send_message(message.chat.id, "Also I have more data about your waste", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Thats all... Send me another waste pic👇")
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton('😔'))
        bot.send_message(message.chat.id,"Didn't recognize anything 😔... Send me another waste pic👇")

while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        time.sleep(15)
