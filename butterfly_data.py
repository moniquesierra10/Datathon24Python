# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 11:27:52 2024

@author: sierram2

Rowdy Datathon - 2024
"""
# getting the data imported

import pandas as pd
#import sqlalchemy
# import pyodbc
import matplotlib.pyplot as plt
import csv
import seaborn as sns
import numpy as np

USDA_Pesticides = pd.read_csv(r"C:\Users\sierram2\Downloads\USDA_PDP_AnalyticalResults.csv")
AgCensus_MasterDataFrame = pd.read_csv(r"\\ifs\links\P5510-OSPBD\Data and Analytics\Users\SierraM2\Exports\AgCensus_MasterDataFrame.csv", low_memory=False )


USDA_Pesticides['state'] = USDA_Pesticides['Sample ID'].str[:2] 
# print(USDA_Pesticides.head())


grouped_conc = USDA_Pesticides.groupby('state')['Concentration'].sum().reset_index()
print(grouped_conc.head())
grouped_conc.to_csv(r'C:\Users\sierram2\Downloads\test1.csv')


# Here we're assuming you might want to display the volume in a 1D format since it's by state
grouped_volume = grouped_conc.groupby('state')['Concentration'].sum().reset_index()

# Create a heat map
plt.figure(figsize=(10, 6))
# Use a bar plot to visualize the total volume by state since heatmap requires 2D data
sns.barplot(x='state', y='Concentration', data=grouped_volume, palette='YlGnBu')
plt.title('Total Pesticide Volume by State')
plt.xlabel('State')
plt.ylabel('Total Volume')
plt.xticks(rotation=45)
plt.show()

# Function to extract date from Sample ID
def extract_date(sample_ID):
    year = sample_ID[2:4]  # Extract year
    month = sample_ID[4:6]  # Extract month
    day = sample_ID[6:8]  # Extract day
    
    # Determine the full year
    if int(year) >= 24:  
        full_year = f"19{year}"
    else:  # Years 00-89 are 2000-2089
        full_year = f"20{year}"
    
    # Create a date string in 'YYYY-MM-DD' format
    date_str = f"{full_year}-{month}-{day}"
    
    return pd.to_datetime(date_str, errors='coerce')  # Convert to datetime, coerce errors

# Apply the function to create a new 'Date' column
USDA_Pesticides['Date'] = USDA_Pesticides['Sample ID'].apply(extract_date)

# Display the DataFrame
print(USDA_Pesticides)

################## finding the volume of the top 5 over time

# Assuming your USDA_Pesticides DataFrame is already loaded
# Ensure the 'Date' column is in datetime format
USDA_Pesticides['Date'] = pd.to_datetime(USDA_Pesticides['Date'])
USDA_Pesticides['Year_Month'] = USDA_Pesticides['Date'].dt.to_period('M')
print(USDA_Pesticides)

# Group by 'Pesticide Name' and sum the 'Concentration'
pesticide_totals = USDA_Pesticides.groupby('Pesticide Name', as_index=False)['Concentration'].sum()

# Sort the pesticides by concentration in descending order and select the top 5
top_5_pesticides = pesticide_totals.sort_values(by='Concentration', ascending=False).head(5)

# Extract the names of the top 5 pesticides
top_5_names = top_5_pesticides['Pesticide Name'].tolist()

# Filter the original DataFrame to include only the top 5 pesticides
filtered_data = USDA_Pesticides[USDA_Pesticides['Pesticide Name'].isin(top_5_names)]

# Group by 'Date' and 'Pesticide Name', summing the 'Concentration' for the filtered data
df_grouped = filtered_data.groupby(['Date', 'Pesticide Name'], as_index=False)['Concentration'].sum()
print(df_grouped)



# Set the plot style
sns.set(style='whitegrid')

# Create the plot
plt.figure(figsize=(14, 8))
sns.lineplot(data=df_grouped, x='Date', y='Concentration', hue='Pesticide Name', marker='o')

# Customize the plot
plt.title('Top 5 Pesticides Concentration Over Time', fontsize=16)
plt.xlabel('Date', fontsize=6)
plt.ylabel('Total Concentration', fontsize=14)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.legend(title='Pesticide Name', fontsize='small')  # Reduce legend font size
plt.tight_layout()  # Final adjustment

# Show the plot
plt.show()

#######################

# Assuming your USDA_Pesticides DataFrame is already loaded
# Ensure the 'Date' column is in datetime format
USDA_Pesticides['Date'] = pd.to_datetime(USDA_Pesticides['Date'])

# Filter for the years 2008 to 2012
start_date = '2008-01-01'
end_date = '2012-12-31'
filtered_df = USDA_Pesticides[(USDA_Pesticides['Date'] >= start_date) & (USDA_Pesticides['Date'] <= end_date)]

# Optionally, create a Year_Month column for the filtered DataFrame
filtered_df['Year_Month'] = filtered_df['Date'].dt.to_period('M')

# Print the filtered DataFrame
print(filtered_df)

# Group by 'Pesticide Name' and sum the 'Concentration'
pesticide_totals = filtered_df.groupby('Pesticide Name', as_index=False)['Concentration'].sum()

# Sort the pesticides by concentration in descending order and select the top 5
top_5_pesticides = pesticide_totals.sort_values(by='Concentration', ascending=False).head(5)

# Extract the names of the top 5 pesticides
top_5_names = top_5_pesticides['Pesticide Name'].tolist()

# Filter the original DataFrame to include only the top 5 pesticides
filtered_data = filtered_df[filtered_df['Pesticide Name'].isin(top_5_names)]

# Group by 'Date' and 'Pesticide Name', summing the 'Concentration' for the filtered data
df_grouped = filtered_data.groupby(['Date', 'Pesticide Name'], as_index=False)['Concentration'].sum()
print(df_grouped)



# Set the plot style
sns.set(style='whitegrid')

# Create the plot
plt.figure(figsize=(14, 8))
sns.lineplot(data=df_grouped, x='Date', y='Concentration', hue='Pesticide Name', marker='o')

# Customize the plot
plt.title('Top 5 Pesticide Concentrations Over Time (2008-2012)', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Total Concentration', fontsize=14)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.legend(title='Pesticide Name', fontsize='small')  # Reduce legend font size
plt.tight_layout()  # Final adjustment

# Show the plot
plt.show()


# Create a new DataFrame grouped by 'Year_Month' and summing the 'Concentration'
# First, ensure that 'Year_Month' is properly created from the 'Date' column
df_grouped['Year_Month'] = df_grouped['Date'].dt.to_period('M')

# Group by 'Year_Month' and sum the 'Concentration' for all pesticides
total_volume_by_month = df_grouped.groupby('Year_Month','state', as_index=False)['Concentration'].sum()
print(total_volume_by_month.head())

# Rename the concentration column for clarity
total_volume_by_month.rename(columns={'Concentration': 'Total_Volume'}, inplace=True)
print(total_volume_by_month.head())

butterfly_data = pd.read_csv(r"\\ifs\links\P5510-OSPBD\Data and Analytics\Users\SierraM2\Exports\datathon butterfly sightings 08-12.csv", low_memory=False )

butterfly_data['Date'] = pd.to_datetime(butterfly_data['Date'])

# Create a 'Year_Month' column for grouping
butterfly_data['Year_Month'] = butterfly_data['Date'].dt.to_period('M')

# Group by 'Year_Month' and sum the 'Amt Seen'
monthly_butterfly_volume = butterfly_data.groupby('Year_Month', as_index=False)['Amt Seen'].sum()

# Rename the column for clarity
monthly_butterfly_volume.rename(columns={'Amt Seen': 'Total_Seen'}, inplace=True)

# Print the new DataFrame
print(monthly_butterfly_volume.head())

merged_data = pd.merge(monthly_butterfly_volume, total_volume_by_month, on='Year_Month')
print(merged_data.head())


# Calculate the correlation
correlation = merged_data['Total_Seen'].corr(merged_data['Total_Volume'])

print(f"Correlation between Butterfly Volume and Pesticide Volume: {correlation:.2f}")



# Ensure the 'Year_Month' column is in string format or convert it to datetime
monthly_butterfly_volume['Year_Month'] = monthly_butterfly_volume['Year_Month'].astype(str)

# Create the plot for butterfly volume over time
plt.figure(figsize=(14, 8))

# Plot butterfly volume
sns.lineplot(data=monthly_butterfly_volume, x='Year_Month', y='Total_Seen', marker='o', color='blue')

# Customize the plot
plt.title('Monthly Butterfly Volume Over Time', fontsize=16)
plt.xlabel('Year-Month', fontsize=14)
plt.ylabel('Total Seen', fontsize=14)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout for better spacing

# Show the plot
plt.show()
# 1. Can you infer pesticide use by county based on the Pesticide Data Program
# (PDP)? If so, create a map illustrating this data. What additional data
#would be required to make this inference more precise? Study the file 115795-
#V3.zip.

# creating map



# what is missing?


#2. Conduct a statistical analysis to examine whether there is a significant cor-
#relation between pesticide use and the decline in monarch butterfly popula-
#tions.

# figure out what model fits this relationship



#3. One of your team members suggested that the National Institutes of Health
#(NIH) and the Centers for Disease Control and Prevention (CDC) maintain
#maps of disease incidence, such as Parkinson’s. There is speculation of a
#correlation between pesticide use and infant mortality. Investigate whether
#there is a connection between pesticide use, the decline in monarch butter-
#flies, and the incidence of human disease.


# is there a correlation between pesticide and infant morality



