def calculate_aqi_for_pollutant(concentration: float, pollutant: str) -> int:
    """
    Calculate AQI for a specific pollutant using EPA breakpoints.
    Returns AQI value (0-500 scale).
    """
    def linear(Cp: float, Ih: float, Il: float, BPh: float, BPl: float) -> float:
        """EPA's linear interpolation formula"""
        return ((Ih - Il) / (BPh - BPl)) * (Cp - BPl) + Il

    # Breakpoints for each pollutant according to EPA Technical Document Table 6
    breakpoints = {
        "PM2.5": [
            (0.0, 12.0, 0, 50),
            (12.1, 35.4, 51, 100),
            (35.5, 55.4, 101, 150),
            (55.5, 150.4, 151, 200),
            (150.5, 250.4, 201, 300),
            (250.5, 350.4, 301, 400),
            (350.5, 500.4, 401, 500)
        ],
        "PM10": [
            (0, 54, 0, 50),
            (55, 154, 51, 100),
            (155, 254, 101, 150),
            (255, 354, 151, 200),
            (355, 424, 201, 300),
            (425, 504, 301, 400),
            (505, 604, 401, 500)
        ],
        "O3": [  # 8-hour
            (0.000, 0.054, 0, 50),
            (0.055, 0.070, 51, 100),
            (0.071, 0.085, 101, 150),
            (0.086, 0.105, 151, 200),
            (0.106, 0.200, 201, 300),
        ],
        "CO": [
            (0.0, 4.4, 0, 50),
            (4.5, 9.4, 51, 100),
            (9.5, 12.4, 101, 150),
            (12.5, 15.4, 151, 200),
            (15.5, 30.4, 201, 300),
            (30.5, 40.4, 301, 400),
            (40.5, 50.4, 401, 500)
        ],
        "SO2": [  # 1-hour
            (0, 35, 0, 50),
            (36, 75, 51, 100),
            (76, 185, 101, 150),
            (186, 304, 151, 200),
            (305, 604, 201, 300),
            (605, 804, 301, 400),
            (805, 1004, 401, 500)
        ],
        "NO2": [  # 1-hour
            (0, 53, 0, 50),
            (54, 100, 51, 100),
            (101, 360, 101, 150),
            (361, 649, 151, 200),
            (650, 1249, 201, 300),
            (1250, 1649, 301, 400),
            (1650, 2049, 401, 500)
        ]
    }

    # Get the breakpoints for this pollutant
    breaks = breakpoints.get(pollutant)
    if not breaks:
        return 0

    # Find the appropriate breakpoint category
    for BPl, BPh, Il, Ih in breaks:
        if BPl <= concentration <= BPh:
            return round(linear(concentration, Ih, Il, BPh, BPl))

    # If concentration is higher than the highest breakpoint
    if concentration > breaks[-1][1]:
        return 500
    
    return 0
