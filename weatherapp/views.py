import requests
from django.shortcuts import render
from .forms import CityForm
from .models import SearchHistory

def get_weather(request):
    api_key = '97e8797114ff0a48566fb2666085fff0'
    weather_data = {}
    forecast_data = []
    past_searches = SearchHistory.objects.all().order_by('-timestamp')[:5]  # Last 5 searches
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            # Current weather API
            weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            # 5-day forecast API
            forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
            
            weather_response = requests.get(weather_url)
            forecast_response = requests.get(forecast_url)

            if weather_response.status_code == 200 and forecast_response.status_code == 200:
                # Current Weather Data
                data = weather_response.json()
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }
                
                # Forecast Data (Next 5 days at 3-hour intervals)
                forecast_data = forecast_response.json()['list'][:5]
                
                # Save to search history
                SearchHistory.objects.create(city=city)

            else:
                weather_data['error'] = "City not found or API issue."

    else:
        form = CityForm()

    return render(request, 'weather.html', {
        'form': form,
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'past_searches': past_searches
    })
