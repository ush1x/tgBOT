import telebot
from telebot import types
import json
import requests

bot = telebot.TeleBot('6941731661:AAFfIW7YXDTDNSjsvmlpIiGLEloYxomLrbU')
# jsonresp = '{"now":1706434843,"now_dt":"2024-01-28T09:40:43.382080Z","info":{"url":"https://yandex.ru/pogoda/213?lat=55.75396\u0026lon=37.620393","lat":55.75396,"lon":37.620393},"fact":{"obs_time":1706432400,"temp":-4,"feels_like":-8,"icon":"ovc","condition":"overcast","wind_speed":1,"wind_dir":"w","pressure_mm":758,"pressure_pa":1010,"humidity":78,"daytime":"d","polar":false,"season":"winter","wind_gust":4.2},"forecast":{"date":"2024-01-28","date_ts":1706389200,"week":4,"sunrise":"08:32","sunset":"16:52","moon_code":1,"moon_text":"decreasing-moon","parts":[{"part_name":"evening","temp_min":-5,"temp_avg":-4,"temp_max":-3,"wind_speed":1.4,"wind_gust":3.8,"wind_dir":"w","pressure_mm":760,"pressure_pa":1013,"humidity":82,"prec_mm":0,"prec_prob":10,"prec_period":240,"icon":"ovc","condition":"overcast","feels_like":-8,"daytime":"n","polar":false},{"part_name":"night","temp_min":-6,"temp_avg":-6,"temp_max":-5,"wind_speed":2.1,"wind_gust":5,"wind_dir":"w","pressure_mm":761,"pressure_pa":1014,"humidity":83,"prec_mm":0,"prec_prob":10,"prec_period":480,"icon":"ovc","condition":"overcast","feels_like":-10,"daytime":"n","polar":false}]}}'

data = [
    {"country":"Россия","city":"Краснодар",     "lat":"45.02","lon":"38.59"},
    {"country":"Россия","city":"Сочи",          "lat":"43.35","lon":"39.43"},
    {"country":"Россия","city":"Екатеринбург",  "lat":"56.50","lon":"60.35"},
    {"country":"Турция","city":"Стамбул",       "lat":"41.01","lon":"28.94"},
    {"country":"Турция","city":"Аланья",        "lat":"36.32","lon":"31.59"},
    {"country":"Турция","city":"Кемер",         "lat":"36.36","lon":"30.33"},
    {"country":"Египет","city":"Шарм-Эль-Шейх", "lat":"27.58","lon":"34.23"},
    {"country":"Египет","city":"Каир",          "lat":"30.03","lon":"31.14"},
    {"country":"Египет","city":"Хургада",       "lat":"27.15","lon":"33.48"},
]

def countries():
    countries = []
    for el in data:
        country = el['country']
        if not country in countries:
            countries.append(country)
    return countries

def cities_by_country(country):
    cities = []
    for el in data:
        if el['country'] == country:
            cities.append(el['city'])
    return cities

def cities():
    cities = []
    for el in data:
        cities.append(el['city'])
    return cities


def print_weather(message):
    city = message.text
    lat = 0        
    lon = 0
    for el in data:
        if el['city'] == city:
            lat = el['lat']
            lon = el['lon']
    
    if lat == 0 or lon == 0:
        bot.send_message(message.chat.id, 'Город не найден!')
    else:
        headers={"Content-Type":"application/json", "X-Yandex-API-Key":"39f8ad18-41d5-4dd6-a3ce-646982ac197f"}
        params={"lat":lat, "lon":lon}
        response = requests.get("https://api.weather.yandex.ru/v1/informers", headers=headers, params=params)
        if response.status_code == 200:
            jsonresp = response.text
            dataresp = json.loads(jsonresp)
            info = dataresp['fact']
            bot.send_message(message.chat.id, "Погода в городе " + city + ": \n" + 
                             "Температура: " + str(info['temp']) + ", " + 
                             "Ощущается как: " + str(info['feels_like']) + " \n" + 
                             "Давление: " + str(info['pressure_mm']) + "мм/рт. ст.")
        else:
            bot.send_message(message.chat.id, 'Не удалось выполнить запрос:' + response.text)            

    message_select_country(message)


def message_select_country(message):

    markup=types.ReplyKeyboardMarkup(one_time_keyboard = True)
    for country in countries():
        markup.add(types.KeyboardButton(country))
    bot.send_message(message.chat.id,'Выберите страну',
                                                reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text in countries():
        markup=types.ReplyKeyboardMarkup(one_time_keyboard = True)
        for city in cities_by_country(message.text):
            markup.add(types.KeyboardButton(city))
        markup.add(types.KeyboardButton("Назад, к выбору страны"))
        bot.send_message(message.chat.id,'Выберите город',
                                                reply_markup=markup)

    if message.text=="Назад, к выбору страны":
        message_select_country(message)

    if message.text in cities():
        print_weather(message)
        
bot.polling(none_stop=True)