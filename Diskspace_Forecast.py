# Requires matplotlib and pandas
# so
# pip install matplotlib and pandas


import matplotlib.pyplot as plt
import pandas as pd

# Function to prompt user for input data
def get_user_input():
    dates = []
    usage = []

    # Get maximum volume size
    max_volume = float(input("Enter the maximum volume size (GB): "))

    # Get the end date for the forecast
    end_date = pd.to_datetime(input("Enter the date to forecast to (YYYY-MM-DD): "))

    # Get at least two dates and usage sizes
    for i in range(2):
        date_input = input(f"Enter the {i+1} date (YYYY-MM-DD): ")
        usage_input = float(input(f"Enter the {i+1} usage size (GB): "))

        dates.append(pd.to_datetime(date_input))
        usage.append(usage_input)

    # Ask if user wants to add more dates and usage sizes
    while True:
        another = input("Would you like to add another date and usage size? (yes/no or y/n): ").strip().lower()
        if another in ['yes', 'y']:
            date_input = input("Enter a date (YYYY-MM-DD): ")
            usage_input = float(input(f"Enter the usage size (GB) for {date_input}: "))

            dates.append(pd.to_datetime(date_input))
            usage.append(usage_input)
        elif another in ['no', 'n']:
            break
        else:
            print("Please enter 'yes', 'no', 'y', or 'n'.")

    return dates, usage, max_volume, end_date

# Get data from user
dates, usage, max_volume, end_date = get_user_input()

# Create DataFrame and sort by date
data = pd.DataFrame({'Date': dates, 'Usage': usage})
data = data.sort_values('Date').reset_index(drop=True)

# Forecast future usage
start_date = data['Date'].max() + pd.Timedelta(days=7)
future_dates = pd.date_range(start=start_date, end=end_date, freq='W')
future_usage = [data['Usage'].iloc[-1] + (i+1)*5 for i in range(len(future_dates))]

# Add future data to DataFrame
future_data = pd.DataFrame({'Date': future_dates, 'Usage': future_usage})
data = pd.concat([data, future_data]).reset_index(drop=True)

# Plotting with a horizontal line at max_volume
plt.figure(figsize=(10, 6))
plt.plot(data['Date'], data['Usage'], marker='o', label='Forecasted Usage')
plt.axhline(y=max_volume, color='red', linestyle='--', label='Max Drive Volume ({}GB)'.format(max_volume))
plt.xlabel('Date')
plt.ylabel('Disk Space Usage (GB)')
plt.title('Forecasted Disk Space Usage')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot
plt.show()
