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
	'clear sky': 'CÃŠu limpo âī¸',
	'few clouds': 'Poucas nuvens đ¤ī¸',
	'scattered clouds': 'Nuvens dispersas đ¤ī¸',
	'broken clouds': 'Nublado âī¸',
	'overcast clouds': 'Nublado âī¸',
	'light rain': 'Pouca chuva đ§ī¸',
	'moderate rain': 'Chuva moderada đ§ī¸',
	'heavy intensity rain': 'Chuva intensa đ§ī¸',
	'very heavy rain': 'Tempestade đ§ī¸',
	'extreme rain': 'Tempestade đ§ī¸',
	'light intensity shower rain': 'Pouca chuva dispersa đ§ī¸',
	'shower rain': 'Chuva dispersa đ§ī¸',
	'heavy intensity shower rain': 'Chuva dispersa intensa đ§ī¸',
	'ragged shower rain': 'Chuva dispersa intensa đ§ī¸',
	'light intensity drizzle': 'Garoa đ§ī¸',
	'drizzle': 'Garoa đ§ī¸',
	'heavy intensity drizzle': 'Garoa forte đ§ī¸',
	'light intensity drizzle rain': 'Garoa đ§ī¸',
	'drizzle rain': 'Garoa đ§ī¸',
	'heavy intensity drizzle rain': 'Garoa forte đ§ī¸',
	'shower rain and drizzle': 'Garoa com chuvas dispersas đ§ī¸',
	'heavy shower rain and drizzle': 'Garoa com fortes chuvas dispersas đ§ī¸',
	'shower drizzle': 'Garoa đ§ī¸',
	'thunderstorm with light rain': 'Trovoada com poucos raios đŠī¸',
	'thunderstorm with rain': 'Trovoada com chuva âī¸',
	'thunderstorm with heavy rain': 'Trovoada com chuva forte âī¸',
	'light thunderstorm': 'Trovoada fraca đŠī¸',
	'thunderstorm': 'Trovoada đŠī¸',
	'heavy thunderstorm': 'Trovoada forte đŠī¸',
	'ragged thunderstorm': 'Trovoada đŠī¸',
	'thunderstorm with light drizzel': 'Trovoada com garoa fraca âī¸',
	'thunderstorm with drizzle': 'Trovoada com garoa âī¸',
	'thunderstorm with heavy drizzle': 'Trovoada com garoa forte âī¸' 
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
				api.update_status(f'OlÃĄ @{tweet.user.screen_name}!\nPrevisÃŖo do tempo em Floripa com @FloripaTempoBot đ¤\n{weather_status_br}\nTemperatura: {temperature}Â°C\nVento: {wind_speed} km/h\nUmidade: {w.humidity}%\nNebulosidade: {w.clouds}%', in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
				set_last_id(tweet.id_str)
				print('tweeted mention')
			except Exception as e:
				print(e)
	time.sleep(30)
	os.system('cls||clear')
