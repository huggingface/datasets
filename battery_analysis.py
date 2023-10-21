import psutil
import time

while True:
    battery = psutil.sensors_battery()
    battery_percentage = battery.percent if battery else "N/A"
    power_plugged = "Plugged In" if battery.power_plugged else "Battery"

    print(f'Battery Percentage: {battery_percentage}%')
    print(f'Power Source: {power_plugged}')

    time.sleep(300)  # Log data every 5 minutes
