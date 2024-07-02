from fastapi import FastAPI, Request

import requests


app = FastAPI()

#OpenWeatherMap API key
API_KEY = ''



@app.get('/api/hello')
def visitor_info(visitor_name: str, request: Request):
    
    client_ip = request.client.host    #Get the visitor ip address
    ipinfo_token = ''     #ipinfo.io api_key
    url = f'https://ipinfo.io/{client_ip}/json'
    headers = {'Authorization': f'Bearer {ipinfo_token}'}
    ipinfo_response = requests.get(url, headers=headers)
    
    
    if ipinfo_response.status_code == 200:
        location_data = ipinfo_response.json()
        city = location_data.get('city', 'Unknown')
        
        new_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        new_response = requests.get(new_url)
        data = new_response.json()
        temperature = data['main']['temp']
        
        greeting = f'Hello, {visitor_name}! the tempreture is {temperature} degrees celcius in {city}'
        response = {
            'client_ip' : client_ip,
            'location' : city,
            'greeting' : greeting,
        }
        return response
    
    return {"error": "Unable to retrieve location information"}

    
  

