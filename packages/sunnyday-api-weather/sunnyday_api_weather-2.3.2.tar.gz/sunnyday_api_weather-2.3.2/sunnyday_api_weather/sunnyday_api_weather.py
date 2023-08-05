import requests, pprint

url = "https://api.openweathermap.org/data/2.5/forecast?q=Madrid&appid=39afed6191ae609ad21f1ddb2c9418e0&units=imperial"
url = "https://api.openweathermap.org/data/2.5/forecast?lat=40.1&lon=30.1&appid=39afed6191ae609ad21f1ddb2c9418e0&units=imperial"



class Weather:
    
    def __init__(self, apikey, city=None, lat=None, lon=None):
        if city:
            r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=imperial")
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=39afed6191ae609ad21f1ddb2c9418e0&units=imperial")
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("Provide either a city or lon and lat arguments")
        
    def next_12h(self):
        simply_data = []
        #return self.data['list'][:4]
        for dicty in self.data['list'][:4]:
            simply_data.append((dicty['dt_txt'], dicty['main']['temp'], dicty['weather'][0]['description']))
        return simply_data

#weather = Weather(apikey="39afed6191ae609ad21f1ddb2c9418e0", city="Madrid")
weather = Weather(apikey="39afed6191ae609ad21f1ddb2c9418e0", lat="40.1", lon="30.1")
pprint.pprint(weather.next_12h())