import telebot
import requests
import traceback

bot = telebot.TeleBot('private_for_you')
admin_id = private_for_you

start_txt = 'Привет! Это бот прогноза погоды.\nНапиши любой символ чтобы\nузнать погоду в Новосибирске на данный момент.'



keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('Информация о проекте')
button_2 = telebot.types.KeyboardButton('Информация о создателях проекта')
keyboard.add(button_1, button_2)

keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('Вернуться к определению погоды')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown', reply_markup = keyboard)



@bot.message_handler(content_types=['text'])
def weather(message):
    try:
        city = "Новосибирск"
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        responce = requests.get(url)
        if responce.status_code == 200:
            if message.text == 'Информация о проекте':
                bot.send_message(message.from_user.id, 'Мы сделали проект про бота, который может\nприсылать погоду в реальном времени.', reply_markup=keyboard2)
            elif message.text == 'Информация о создателях проекта':
                bot.send_message(message.from_user.id, 'Создатели проекта: Кирилл Кошелев, Виктор Пономарев\n'
                                                       'Ученики 7 "Г" класса ', reply_markup=keyboard2)
            else:
                url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
                weather_data = requests.get(url).json()
                temperature = round(weather_data['main']['temp'])
                temperature_feels = round(weather_data['main']['feels_like'])
                humidity = round(weather_data['main']['humidity'])
                clouds = round(weather_data['clouds']['all'])
                w_now = 'Сейчас в городе ' + city + ' ' + str(temperature) + ' °C'
                w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
                w_hum = 'Влажность: '+ str(humidity) +'%'
                w_clouds = 'Облачность: ' + str(clouds) + '%'
                bot.send_message(message.from_user.id, w_now, reply_markup = keyboard)
                bot.send_message(message.from_user.id, w_feels, reply_markup = keyboard)
                bot.send_message(message.from_user.id, w_hum, reply_markup = keyboard)
                bot.send_message(message.from_user.id, w_clouds, reply_markup = keyboard)
        else:
            bot.send_message(message.from_user.id, 'Бот не обработал запрос, попробуйте позже.' ,reply_markup=keyboard)
            bot.send_message(admin_id, f'status_code: {responce.status_code}')
    except:
        bot.send_message(admin_id, f'Error in weather: {traceback.format_exc()}')

bot.polling(none_stop=True, interval=0)

