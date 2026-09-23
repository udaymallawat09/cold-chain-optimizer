def calculate_degradation(transit_hours, temp_celsius):
    """
    Calculates biochemical degradation (shelf-life loss) using a Q10 temperature coefficient model.
    
    Parameters:
    - transit_hours (float): Time spent in transit.
    - temp_celsius (float): Average temperature during transit.
    
    Returns:
    - float: The kinetic cost (degradation units).
    """
    # Baseline optimal refrigeration temperature
    baseline_temp = 4.0 
    
    # Base degradation rate per hour at the optimal baseline temperature
    base_rate = 0.5 
    
    # Q10 factor: rate of change for every 10 degree increase. 
    # A Q10 of 3.0 is typical for many microbiological spoilage reactions.
    q10 = 3.0
    
    # Calculate the exponential multiplier based on temperature abuse
    temperature_factor = q10 ** ((temp_celsius - baseline_temp) / 10.0)
    
    # Total degradation = rate * exponential factor * time
    degradation = base_rate * temperature_factor * transit_hours
    
    return round(degradation, 3)

# Quick test block to verify the math if this file is run directly
if __name__ == "__main__":
    print("Testing Kinetic Model:")
    print(f"Degradation at 4.0°C for 10 hrs: {calculate_degradation(10, 4.0)}")
    print(f"Degradation at 14.0°C for 10 hrs: {calculate_degradation(10, 14.0)}")