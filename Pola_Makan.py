import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('Data_Random_Food.csv')

# Convert date and time columns to datetime format
df['Timestamp'] = pd.to_datetime(df['Tanggal'] + ' ' + df['Waktu'], format='%d/%m/%Y %H:%M')

# Calculate the time difference between rows
df['Selisih'] = df['Timestamp'].diff()

# Convert time difference to hours
df['Selisih'] = df['Selisih'].dt.total_seconds() / 3600

# Initialize 'Pesan' column
df['Pesan'] = None

# Inspect whether between two rows are more than 5 minutes
# Inspect whether the two rows each has 210 calories
# Remind the user if the time gap is less than 3 hours or more than 5 hours
for i in range(1, len(df)):
    if df['Calories'][i] >= 210 and df['Calories'][i-1] >= 210 and df['Selisih'][i] > 5/60:
        if df['Selisih'][i] < 3:
            df.at[i, 'Pesan'] = 'Rentang waktu makan kurang dari 3 jam'
        elif df['Selisih'][i] > 5:
            df.at[i, 'Pesan'] = 'Rentang waktu makan lebih dari 5 jam'
    else:
        df.at[i, 'Pesan'] = "Rentang waktu makan yang baik"

print(df)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Create a line plot
plt.figure(figsize=(10, 6))
for column in ['Calories', 'Carbs', 'Prots', 'Fats']:
    plt.plot(df['Timestamp'], df[column], label=column)

# Format the x-axis to show dates
ax = plt.gca()
date_format = mdates.DateFormatter('%d/%m/%Y')
ax.xaxis.set_major_formatter(date_format)

plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Daily Eating Time')
plt.legend()
plt.gcf().autofmt_xdate()  # Improve date labels' readability
plt.show()

# Calculate the total for 'Carbs', 'Prots', and 'Fats'
total = df[['Calories', 'Carbs', 'Prots', 'Fats']].sum()
total_macro = total[['Carbs', 'Prots', 'Fats']]

# Import recommended_calories from bmi_bmr_rtr.py
from bmi_bmr_rtr import recommended_calories

recommended_calories = recommended_calories()
# Pie chart for calories
remaining_calories = max(0, recommended_calories - total['Calories'])
calories_sizes = [total['Calories'], remaining_calories]

plt.figure(figsize=(8, 6))
plt.pie(calories_sizes, labels=['Consumed', 'Remaining'], autopct='%1.1f%%', startangle=140)
plt.title('Calories Consumption')
plt.axis('equal')
plt.show()

# Create a pie chart for macronutrients proportion
plt.figure(figsize=(6, 6))
plt.pie(total_macro, labels=total_macro.index, autopct='%1.1f%%')
plt.title('Proportion of Carbs, Prots, and Fats')
plt.show()

# Calculate the total amount of carbs, proteins, and fats over all days
total_carbs = df['Carbs'].sum()
total_prots = df['Prots'].sum()
total_fats = df['Fats'].sum()

# Calculate the total amount of these three macronutrients
total_all = total_carbs + total_prots + total_fats

# Calculate the proportion of each macronutrient
carbs_prop = total_carbs / total_all
prots_prop = total_prots / total_all
fats_prop = total_fats / total_all

# Check if the proportion of each macronutrient is within the AMDR
if not 0.45 <= carbs_prop <= 0.65:
    print('Warning: The proportion of carbs is out of the acceptable range (45–65%).')
elif not 0.20 <= fats_prop <= 0.35:
    print('Warning: The proportion of fats is out of the acceptable range (20–35%).')
elif not 0.10 <= prots_prop <= 0.35:
    print('Warning: The proportion of protein is out of the acceptable range (10–35%).')
else:
    print('You have a good proportion of carbohydrate, protein and fat.')
