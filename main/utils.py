import relizene_weather

def find_temprature(city):
    temp = relizene_weather.run_city(city=city)
    if temp['cod'] == 200:
        results = {}
        results['city'] = temp['name']
        results['temp'] = temp['main']['temp']
        results['condition'] = temp['weather'][0]['description']
        results['wind_speed'] = temp['wind']['speed']
        results['humidity'] = temp['main']['humidity']
        results['pressure'] = temp['main']['pressure']
        results['cod'] = temp['cod']
        return results
    else:
        return temp
    

def find_temprature_coord(lat, lon):
    temp = relizene_weather.run_geo(lat=lon, lon=lat)
    if temp['cod'] == 200:
        results = {}
        results['city'] = temp['name']
        results['temp'] = temp['main']['temp']
        results['condition'] = temp['weather'][0]['description']
        results['wind_speed'] = temp['wind']['speed']
        results['humidity'] = temp['main']['humidity']
        results['pressure'] = temp['main']['pressure']
        results['cod'] = temp['cod']
        return results
    else:
        return temp




if __name__ == '__main__':
    print(find_temprature_coord(lat='56.6388', lon='47.8908'))
    
    
    
    
