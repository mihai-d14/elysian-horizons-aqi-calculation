# elysian-horizons-aqi-calculation
Calculation of air quality score used on elysianhorizons.com. We use the US EPA's air quality calculation as per https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf and that index is then converted to a 1-100 score. See README for more information.

The ```fetch_air_quality``` function is used to fetch air quality metrics for every hour of the past year using OpenWeather's One Call API 3.0, specifically:
- Ozone
- PM2.5
- PM10
- CO
- SO2
- NO2

The ```calculate_aqi_for_pollutant``` function is used to calculate AQI for a specific pollutant using EPA breakpoints, according to EPA Technical Document Table 6.

The ```calculate_air_quality_score``` function is used to convert AQI to our own 1-100 score: AQI ≤ 1 scores 100, each point increase reduces the score by 1 until AQI 99 (score 1), with AQI ≥ 100 scoring 0.

We use the ```fetch_air_quality``` function to fetch air quality metrics for each one of our properties, and the ```calculate_aqi_for_pollutant``` to calculate the AQI:

         ```# Fetching historical air quality data
            measurements = fetch_air_quality(ad['latitude'], ad['longitude'])
            
            # Calculating AQI for each measurement and each pollutant
            aqi_values = []
            for m in measurements:
                components = m['components']
                try:
                    # We calculate AQI for each pollutant
                    # OpenWeatherMap gives concentrations in μg/m³, therefore we convert using EPA conversion factors
                    pm25_aqi = calculate_aqi_for_pollutant(components['pm2_5'], "PM2.5")  # already in μg/m³
                    pm10_aqi = calculate_aqi_for_pollutant(components['pm10'], "PM10")    # already in μg/m³
                    no2_aqi = calculate_aqi_for_pollutant(components['no2'] * 0.531, "NO2")  # μg/m³ to ppb
                    so2_aqi = calculate_aqi_for_pollutant(components['so2'] * 0.376, "SO2")  # μg/m³ to ppb
                    co_aqi = calculate_aqi_for_pollutant(components['co'] / 1145, "CO")      # μg/m³ to ppm
                    o3_aqi = calculate_aqi_for_pollutant(components['o3'] / 1963, "O3")      # μg/m³ to ppm
                    
                    # We take the maximum AQI value among all pollutants
                    max_aqi = max([pm25_aqi, pm10_aqi, no2_aqi, so2_aqi, co_aqi, o3_aqi])
                    aqi_values.append(max_aqi)
                except (KeyError, TypeError) as e:
                    print(f"Warning: Skipping invalid measurement data: {str(e)}")
                    continue
            
            if not aqi_values:
                print(f"No valid AQI values calculated for ad {ad['id']}")
                continue

            # Calculating average AQI
            avg_aqi = statistics.mean(aqi_values)```
            
The AQI is converted to a 1-100 score: AQI ≤ 1 scores 100, each point increase reduces the score by 1 until AQI 99 (score 1), with AQI ≥ 100 scoring 0.
            
         ```# Converting to 0-100 score where 100 is best (as integer)
            air_quality_score = calculate_air_quality_score(avg_aqi)```


