from django.http import HttpResponse
from django.shortcuts import render

import requests
from selenium import webdriver

import folium
import datetime
import time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

import math
import requests

# this method will return us our actual coordinates
# using our ip address
def locationdetector(city = None):
	try:
		response = requests.get('https://ipinfo.io')
		data = response.json()
		loc = data['loc'].split(',')
		lat, long = float(loc[0]), float(loc[1])
		city = data.get('city', 'Unknown')
		state = data.get('region', 'Unknown')
		return lat, long, city, state
	
	except:
		# return HttpResponse ("Internet Not avialable")
		return False

# this will return our lat & long based on input
def get_location(location_name):
	try:
		geolocator = Nominatim(user_agent="my_app")
		location = geolocator.geocode(location_name)
		latitude = location.latitude
		longitude = location.longitude
		
		# Get the time zone
		tf = TimezoneFinder()
		timezone_str = tf.certain_timezone_at(lat=latitude, lng=longitude)
		
		# Get the current time and date
		timezone = pytz.timezone(timezone_str)
		current_time = datetime.now(timezone)
		dt_str = str(current_time)
		dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f%z")

		# Split the date and time components
		date_components = [dt_obj.year, dt_obj.month, dt_obj.day]
		time_components = [dt_obj.hour, dt_obj.minute, dt_obj.second, dt_obj.microsecond]

		date = f'{date_components[2]}/{date_components[1]}/{date_components[0]}'
		t = f'{time_components[0]}.{time_components[1]}'

		print("Date components:", date_components)
		print("Time components:", time_components)
		
		
		return latitude, longitude, timezone_str, date, t
	except:
		return False

# Geocode the location
# geolocator = Nominatim(user_agent="my_app")
# location = geolocator.geocode("Dhaka")

# Define the function to fetch weather data
def fetch_weather(city):
	api_key = "62c308be0c3fb564b1d2bea688429b1d"
	url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
	try:
		response = requests.get(url)
		data = response.json()
		temperature = data["main"]["temp"]
		weather = data["weather"][0]["description"]
		return temperature, weather
	except:
		# print("Error", "Unable to fetch weather data")
		return False

def index(reuest):
	weather_descriptions = {
    "Sunny": ["Clear sky", "Sunny", "Clear", "Fair"],
    "Cloudy ": ["Overcast clouds", "Broken clouds", "Scattered clouds", "Cloudy"],
    "Rainy": ["Light rain", "Moderate rain", "Heavy rain", "Freezing rain", "Light drizzle", "Heavy drizzle", "Drizzle", 'Heavy intensity rain'],
    "Snowy": ["Light snow", "Moderate snow", "Heavy snow", "Sleet", "Freezing rain", "Light snow showers", "Heavy snow showers"],
    "Stormy": ["Thunderstorm", "Heavy thunderstorm", "Ragged thunderstorm", "Thunderstorm with light rain", "Thunderstorm with heavy rain", "Thunderstorm with hail"],
    "Windy": ["Gentle breeze", "Moderate breeze", "Fresh breeze", "Strong breeze", "High wind", "Gale", "Storm"],
    "Foggy": ["Fog", "Light fog", "Dense fog", "Freezing fog"],
    "Extreme": ["Mist", "Smoke", "Haze", "Dust", "Sand", "Ash", "Squall", "Tornado", "Hurricane", "Typhoon", "Cyclone", "Blizzard", "Ice storm", "Dust storm", "Sandstorm"]
	}
	des = ''
	todo = ''
	d = ''
	loc = locationdetector()
	if loc != False:
		forcast = fetch_weather(loc[2])
		if forcast != False:
			for k, v in weather_descriptions.items():
				for i in v:
					if i == forcast[1].capitalize():
						des = f'The weather is going to be {k} today. There\'s going to be {i.capitalize()} out there!'
						d = k
			if k.capitalize() == "Sunny" or k.capitalize() == "Clear":
							todo = f"Wear sunscreen and protective clothing to prevent sunburn\nStay hydrated by drinking plenty of water\nPlan outdoor activities like hiking, biking, or picnics\nTake advantage of natural light to get some vitamin D\nConsider wearing sunglasses and a hat to protect your eyes and face\n"
			elif k.capitalize() == "Cloudy":
							todo += "Bring an umbrella or raincoat in case of unexpected rain\n"
							todo += "Wear layers to adjust to changing temperatures\n"
							todo += "Plan indoor activities like visiting a museum or watching a movie\n"
							todo += "Take advantage of the cooler temperatures to get some exercise or go for a walk\n"
							todo += "Consider wearing comfortable shoes with good grip in case of slippery surfaces\n"

			elif k.capitalize() == "Rainy":
							todo += "Carry an umbrella or raincoat to stay dry\n"
							todo += "Wear waterproof shoes and clothing to prevent getting soaked\n"
							todo += "Plan indoor activities like reading a book or playing board games\n"
							todo += "Avoid traveling or commuting during heavy rain\n"
							todo += "Consider staying indoors and taking a relaxing day off\n"

			elif k.capitalize() == "Snowy":
							todo += "Dress warmly in layers to stay cozy\n"
							todo += "Wear waterproof and insulated clothing to prevent cold and wetness\n"
							todo += "Plan winter activities like skiing, snowboarding, or building a snowman\n"
							todo += "Be cautious when driving or walking on icy roads and sidewalks\n"
							todo += "Consider staying indoors and enjoying hot chocolate or coffee\n"

			elif k.capitalize() == "Stormy":
							todo += "Avoid being outdoors during a thunderstorm\n"
							todo += "Stay away from tall objects like trees or buildings that could attract lightning\n"
							todo += "Unplug electronics and appliances to prevent power surges\n"
							todo += "Stay informed about weather updates and warnings\n"
							todo += "Consider staying indoors and waiting for the storm to pass\n"

			elif k.capitalize() == "Windy":
							todo += "Hold onto your hat and loose items to prevent them from being blown away\n"
							todo += "Wear warm and windproof clothing to stay cozy\n"
							todo += "Avoid traveling or commuting during strong winds\n"
							todo += "Secure outdoor furniture and decorations to prevent them from being blown away\n"
							todo += "Consider staying indoors and enjoying a warm beverage\n"

			elif k.capitalize() == "Foggy":
							todo += "Drive slowly and carefully to avoid accidents\n"
							todo += "Use low-beam headlights to reduce glare\n"
							todo += "Wear warm and breathable clothing to stay comfortable\n"
							todo += "Avoid traveling or commuting during heavy fog\n"
							todo += "Consider staying indoors and waiting for the fog to clear\n"

			elif k.capitalize() == 'Extreme':
							todo += "Avoid outdoor activities during extreme weather conditions like hurricanes or tornadoes\n"
							todo += "Stay informed about weather updates and warnings\n"
							todo += "Follow evacuation orders and instructions from authorities\n"
							todo += "Consider staying indoors and waiting for the weather to improve\n"
			data = {'lat':loc[0], 'lon': loc[1], 'city': loc[2], 'state': loc[3], 'temp': round((forcast[0]-273.15), 1), 'weather': forcast[1].capitalize(), 'desc' : des, 'todo': todo}
			return render(reuest, 'index.html', data)
		else:
			# return render(request, 'error.html')
			return HttpResponse('Unable to fetch weather data')
	else:
		# return render(request, 'error.html')
		return HttpResponse('Internet Not Available\nPlease check your Internet connection')

def weather(request):
	weather_descriptions = {
    "Sunny/Clear": ["Clear sky", "Sunny", "Clear", "Fair"],
    "Cloudy ": ["Overcast clouds", "Broken clouds", "Scattered clouds", "Cloudy"],
    "Rain": ["Light rain", "Moderate rain", "Heavy rain", "Freezing rain", "Light drizzle", "Heavy drizzle", "Drizzle"],
    "Snow": ["Light snow", "Moderate snow", "Heavy snow", "Sleet", "Freezing rain", "Light snow showers", "Heavy snow showers"],
    "Thunderstorm": ["Thunderstorm", "Heavy thunderstorm", "Ragged thunderstorm", "Thunderstorm with light rain", "Thunderstorm with heavy rain", "Thunderstorm with hail"],
    "Wind": ["Gentle breeze", "Moderate breeze", "Fresh breeze", "Strong breeze", "High wind", "Gale", "Storm"],
    "Fog": ["Fog", "Light fog", "Dense fog", "Freezing fog"],
    "Other": ["Mist", "Smoke", "Haze", "Dust", "Sand", "Ash", "Squall", "Tornado"],
    "Extreme Weather": ["Hurricane", "Typhoon", "Cyclone", "Blizzard", "Ice storm", "Dust storm", "Sandstorm"]
	}
	des = ''
	todo = ''
	d = ''
	c = request.GET.get('city', 'default')
	print(c)
	if c != 'default':
		loc = get_location(c.capitalize())
		if loc != False:
			forcast = fetch_weather(c.capitalize())
			if forcast!= False:
				for k, v in weather_descriptions.items():
					for i in v:
						if i == forcast[1].capitalize():
							des = f'The weather is going to be {k} today. There\'s going to be {i.capitalize()} out there!'
							d = k

				if d == "Sunny" or d == "Clear":
								todo = f"Wear sunscreen and protective clothing to prevent sunburn\nStay hydrated by drinking plenty of water\nPlan outdoor activities like hiking, biking, or picnics\nTake advantage of natural light to get some vitamin D\nConsider wearing sunglasses and a hat to protect your eyes and face\n"
				elif d.capitalize() == "Cloudy":
								todo += "Bring an umbrella or raincoat in case of unexpected rain\n"
								todo += "Wear layers to adjust to changing temperatures\n"
								todo += "Plan indoor activities like visiting a museum or watching a movie\n"
								todo += "Take advantage of the cooler temperatures to get some exercise or go for a walk\n"
								todo += "Consider wearing comfortable shoes with good grip in case of slippery surfaces\n"

				elif d.capitalize() == "Rainy":
								todo += "Carry an umbrella or raincoat to stay dry\n"
								todo += "Wear waterproof shoes and clothing to prevent getting soaked\n"
								todo += "Plan indoor activities like reading a book or playing board games\n"
								todo += "Avoid traveling or commuting during heavy rain\n"
								todo += "Consider staying indoors and taking a relaxing day off\n"

				elif d.capitalize() == "Snowy":
								todo += "Dress warmly in layers to stay cozy\n"
								todo += "Wear waterproof and insulated clothing to prevent cold and wetness\n"
								todo += "Plan winter activities like skiing, snowboarding, or building a snowman\n"
								todo += "Be cautious when driving or walking on icy roads and sidewalks\n"
								todo += "Consider staying indoors and enjoying hot chocolate or coffee\n"

				elif d.capitalize() == "Stormy":
								todo += "Avoid being outdoors during a thunderstorm\n"
								todo += "Stay away from tall objects like trees or buildings that could attract lightning\n"
								todo += "Unplug electronics and appliances to prevent power surges\n"
								todo += "Stay informed about weather updates and warnings\n"
								todo += "Consider staying indoors and waiting for the storm to pass\n"

				elif d.capitalize() == "Windy":
								todo += "Hold onto your hat and loose items to prevent them from being blown away\n"
								todo += "Wear warm and windproof clothing to stay cozy\n"
								todo += "Avoid traveling or commuting during strong winds\n"
								todo += "Secure outdoor furniture and decorations to prevent them from being blown away\n"
								todo += "Consider staying indoors and enjoying a warm beverage\n"

				elif d.capitalize() == "Foggy":
								todo += "Drive slowly and carefully to avoid accidents\n"
								todo += "Use low-beam headlights to reduce glare\n"
								todo += "Wear warm and breathable clothing to stay comfortable\n"
								todo += "Avoid traveling or commuting during heavy fog\n"
								todo += "Consider staying indoors and waiting for the fog to clear\n"

				elif d.capitalize() == 'Extreme':
								todo += "Avoid outdoor activities during extreme weather conditions like hurricanes or tornadoes\n"
								todo += "Stay informed about weather updates and warnings\n"
								todo += "Follow evacuation orders and instructions from authorities\n"
								todo += "Consider staying indoors and waiting for the weather to improve\n"
				data = {'lat':loc[0], 'lon': loc[1], 'cont': loc[2], 'd': loc[3], 't': loc[4], 'temp': round((forcast[0]-273.15), 1), 'weather': forcast[1].capitalize(), 'desc' : des, 'todo': todo}
				return render(request, 'forcast.html', data)
			else:
				return render(request, 'error.html')
		else:
			return render(request, 'error.html')
	elif c == 'default' or c == '':
		return render(request, 'error.html')