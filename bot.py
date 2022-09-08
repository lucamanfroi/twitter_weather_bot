import tweepy
from pyowm import OWM
import time
import os

CONSUMER_KEY = 'SECRET KEY'
CONSUMER_SECRET = 'SECRET KEY'
ACCESS_KEY = 'SECRET KEY'
ACCESS_SECRET = 'SECRET KEY'
BEARER_TOKEN = 'SECRET KEY'
GEO = '-27.59667,-48.54917,26km'
owm = OWM('SECRET KEY')


def get_last_id():
	with open('last_id.txt', 'r') as data:
		return(int(data.read()))


def set_last_id(id):
	with open('last_id.txt', 'w') as data:
		data.write(id)


mgr = owm.weather_manager()
obs = mgr.weather_at_place('Florianopolis, Brazil')
w = obs.weather
# Weather status dict, en --> pt-br
weather_translation = {
	'clear sky': 'Céu limpo ☀️',
	'few clouds': 'Poucas nuvens 🌤️',
	'scattered clouds': 'Nuvens dispersas 🌤️',
	'broken clouds': 'Nublado ☁️',
	'overcast clouds': 'Nublado ☁️',
	'light rain': 'Pouca chuva 🌧️',
	'moderate rain': 'Chuva moderada 🌧️',
	'heavy intensity rain': 'Chuva intensa 🌧️',
	'very heavy rain': 'Tempestade 🌧️',
	'extreme rain': 'Tempestade 🌧️',
	'light intensity shower rain': 'Pouca chuva dispersa 🌧️',
	'shower rain': 'Chuva dispersa 🌧️',
	'heavy intensity shower rain': 'Chuva dispersa intensa 🌧️',
	'ragged shower rain': 'Chuva dispersa intensa 🌧️',
	'light intensity drizzle': 'Garoa 🌧️',
	'drizzle': 'Garoa 🌧️',
	'heavy intensity drizzle': 'Garoa forte 🌧️',
	'light intensity drizzle rain': 'Garoa 🌧️',
	'drizzle rain': 'Garoa 🌧️',
	'heavy intensity drizzle rain': 'Garoa forte 🌧️',
	'shower rain and drizzle': 'Garoa com chuvas dispersas 🌧️',
	'heavy shower rain and drizzle': 'Garoa com fortes chuvas dispersas 🌧️',
	'shower drizzle': 'Garoa 🌧️',
	'thunderstorm with light rain': 'Trovoada com poucos raios 🌩️',
	'thunderstorm with rain': 'Trovoada com chuva ⛈️',
	'thunderstorm with heavy rain': 'Trovoada com chuva forte ⛈️',
	'light thunderstorm': 'Trovoada fraca 🌩️',
	'thunderstorm': 'Trovoada 🌩️',
	'heavy thunderstorm': 'Trovoada forte 🌩️',
	'ragged thunderstorm': 'Trovoada 🌩️',
	'thunderstorm with light drizzel': 'Trovoada com garoa fraca ⛈️',
	'thunderstorm with drizzle': 'Trovoada com garoa ⛈️',
	'thunderstorm with heavy drizzle': 'Trovoada com garoa forte ⛈️' 
}
weather_status = w.detailed_status
weather_status_br = weather_translation[weather_status] # Weather status translated tor portuguese
temperature = round(w.temperature('celsius')['temp'])
wind_speed = round(w.wind()['speed']* 3.6)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
last_id = get_last_id()

on = True
while on:
	mentions = api.mentions_timeline()
	print(f'searching for mentions...')
	for tweet in reversed(mentions):
		if tweet.user.screen_name != 'FloripaTempoBot' and tweet.id > get_last_id():
			try:
				print('found one')
				print(f'@{tweet.user.screen_name}: {tweet.text}')
				api.update_status(f'Olá @{tweet.user.screen_name}!\nPrevisão do tempo em Floripa com @FloripaTempoBot 🤗\n{weather_status_br}\nTemperatura: {temperature}°C\nVento: {wind_speed} km/h\nUmidade: {w.humidity}%\nNebulosidade: {w.clouds}%', in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
				set_last_id(tweet.id_str)
				print('tweeted mention')
			except Exception as e:
				print(e)
	time.sleep(30)
	os.system('cls||clear')
