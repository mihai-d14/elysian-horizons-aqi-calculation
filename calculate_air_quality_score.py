def calculate_air_quality_score(aqi: float) -> int:
    """
    Converting EPA AQI (0-500+) to 0-100 score where:
    - EPA AQI 0-3 → score 100 (best)
    - Each +3 EPA AQI points → -1 score point
    - EPA AQI ≥ 300 → score 0 (hazardous)
    
    Score ranges mapping to EPA categories:
    - 0: EPA AQI ≥ 300 (Hazardous)
    - 1-33: EPA AQI 201-300 (Very Unhealthy)
    - 34-50: EPA AQI 151-200 (Unhealthy)
    - 51-67: EPA AQI 101-150 (Unhealthy for Sensitive Groups)
    - 68-83: EPA AQI 51-100 (Moderate)
    - 84-100: EPA AQI 0-50 (Good)
    """
    # Handle hazardous levels
    if aqi >= 300:
        return 0
        
    # Handle other levels
    # We want to map 0-300 EPA AQI to 100-0 score
    # Each 3 point increase in AQI = 1 point decrease in score
    score = 100 - (aqi / 3)
    
    # Ensure score is between 0 and 100
    score = max(0, min(100, score))
    
    return round(score)  # Return rounded integer
