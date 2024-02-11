import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

TOKEN = '6880893642:AAFlKtV8Sf--5ysf2eteLQzd9lvi5ybgRVA'
bot = telebot.TeleBot(TOKEN)
CHANNEL_ID = '-1002025591043' 



def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    div_container = soup.find('div', {'id': 'listings'})
    if div_container is not None:
        img_tags = div_container.find_all('img')
        img_data = [{'src': tag['src'], 'alt': tag.find_next('div', {'class': 'desc'}).text.strip() if tag.find_next('div', {'class': 'desc'}) else 'No description available'} for tag in img_tags]
        return img_data
    else:
        return []


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Best Restaurants in Ethiopia')
    itembtn2 = types.KeyboardButton('Best Vehicle Services in Ethiopia')
    itembtn3 = types.KeyboardButton('Best Doctors and Clinics in Ethiopia')
    itembtn4 = types.KeyboardButton('Best Shopping Centres in Ethiopia')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "Choose from this category :", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Best Restaurants in Ethiopia')
def handle_button1(message):
    img_data = scrape_website('https://www.ethyp.com/category/Restaurants')
    for data in img_data:
        bot.send_message(CHANNEL_ID, data['alt'])

@bot.message_handler(func=lambda message: message.text == 'Best Vehicle Services in Ethiopia')
def handle_button2(message):
    img_data = scrape_website('https://www.ethyp.com/category/Vehicle_services')
    for data in img_data:
        bot.send_message(CHANNEL_ID, data['alt'])


@bot.message_handler(func=lambda message: message.text == 'Best Doctors and Clinics in Ethiopia')
def handle_button3(message):
    img_data = scrape_website('https://www.ethyp.com/category/Doctors_and_Clinics')
    for data in img_data:
        bot.send_message(CHANNEL_ID, data['alt'])

@bot.message_handler(func=lambda message: message.text == 'Best Shopping Centres in Ethiopia')
def handle_button4(message):
    img_data = scrape_website('https://www.ethyp.com/category/Shopping_centres')
    for data in img_data:
        bot.send_message(CHANNEL_ID, data['alt'])



bot.polling()