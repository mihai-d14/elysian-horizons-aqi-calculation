def fetch_air_quality(latitude: float, longitude: float) -> List[Dict]:
    """Fetch last 365 days of air quality data from OpenWeatherMap"""
    end_date = int(datetime.now().timestamp())
    start_date = int((datetime.now() - timedelta(days=365)).timestamp())
    
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={latitude}&lon={longitude}&start={start_date}&end={end_date}&appid={os.getenv('KEY')}"
    
    response = requests.get(url)
    if not response.ok:
        raise Exception(f"OpenWeatherMap API error: {response.status_code} - {response.text}")
    
    return response.json().get('list', [])
