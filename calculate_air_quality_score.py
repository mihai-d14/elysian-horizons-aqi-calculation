def calculate_air_quality_score(aqi: float) -> int:
    """
    Converting AQI to 0-100 score (0 is worst, 100 is best).
    Returns integer score.
    """
    if aqi <= 1:
        return 100
    if aqi > 100:
        return 0
    score = max(0, min(100, 101 - aqi))
    return round(score)
