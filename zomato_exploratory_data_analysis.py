#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install geopy')
get_ipython().system('pip install folium')

import folium


# In[ ]:


# import the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from IPython.core.display import display, HTML


# In[ ]:


# load the data
zomato = pd.read_csv(r"C:\Users\ssindhu\Downloads\zomato_data.csv")
geographical = pd.read_csv(r"C:\Users\ssindhu\Downloads\Geographical Coordinates.csv")


# In[ ]:


print(zomato.head())  # Check the first 5 rows
print(zomato.info())  # Data types and missing values
print(zomato.describe())  # Descriptive statistics for numerical columns


# In[ ]:


#Check for missing data
missing_data = zomato.isnull().sum()
print("Missing data in each column:")
print(missing_data)


# In[ ]:


# Step 5: Handle missing data correctly (no inplace)
# First, clean the 'rate' column to extract numeric values
zomato['rate'] = zomato['rate'].astype(str).str.extract(r'(\d+\.\d+)')
zomato['rate'] = pd.to_numeric(zomato['rate'], errors='coerce')


# In[ ]:


# Clean 'approx_costfor_two_people' (remove commas and convert to float)
zomato['approx_costfor_two_people'] = zomato['approx_costfor_two_people'].astype(str).str.replace(',', '')
zomato['approx_costfor_two_people'] = pd.to_numeric(zomato['approx_costfor_two_people'], errors='coerce')


# In[ ]:


# Fill missing values
zomato['rate'] = zomato['rate'].fillna(zomato['rate'].median())
zomato['approx_costfor_two_people'] = zomato['approx_costfor_two_people'].fillna(zomato['approx_costfor_two_people'].median())
zomato['votes'] = zomato['votes'].fillna(zomato['votes'].median())
zomato['dish_liked'] = zomato['dish_liked'].fillna('Not Available')
zomato['cuisines'] = zomato['cuisines'].fillna('Other')
zomato['rest_type'] = zomato['rest_type'].fillna('Unknown')


# In[ ]:


# Data Visualizations

# Distribution of Ratings

plt.figure(figsize=(10, 6))
sns.histplot(zomato['rate'], bins=30, kde=True)
plt.title('Distribution of Restaurant Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()


# In[ ]:


#Distribution of Approximate Cost for Two People
plt.figure(figsize=(10, 6))
sns.histplot(zomato['approx_costfor_two_people'], bins=30, kde=True, color='green')
plt.title('Distribution of Approximate Cost for Two People')
plt.xlabel('Cost (INR)')
plt.ylabel('Frequency')
plt.show()


# In[ ]:


#Distribution of Restaurant Types
plt.figure(figsize=(10, 12))
sns.countplot(data=zomato, y='rest_type', order=zomato['rest_type'].value_counts().index, palette='viridis')
plt.title('Distribution of Restaurant Types')
plt.xlabel('Count')
plt.ylabel('Restaurant Type')
plt.show()


# In[ ]:


# Most Common Cuisines Offered
plt.figure(figsize=(10, 6))
top_cuisines = zomato['cuisines'].value_counts().head(10)
sns.barplot(x=top_cuisines.values, y=top_cuisines.index, palette='Blues_d')
plt.title('Top 10 Cuisines Offered by Restaurants')
plt.xlabel('Count')
plt.ylabel('Cuisine')
plt.show()


# In[ ]:


# Geospatial Distribution of Restaurants
merged_df = pd.merge(zomato, geographical, on='listed_incity', how='left')
merged_df


# In[ ]:


print(merged_df.columns)


# In[ ]:


# Create a map centered on Bangalore
bangalore_map = folium.Map(location=[12.9716, 77.5946], zoom_start=12)
bangalore_map


# In[ ]:


# Plot restaurants
for _, row in merged_df.iterrows():
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
        popup_text = f"Restaurant Type: {row['rest_type']}<br>Cuisines: {row['cuisines']}"
        folium.Marker([row['Latitude'], row['Longitude']], popup=popup_text).add_to(bangalore_map)


# In[ ]:


# Save the map
bangalore_map.save("restaurant_map.html")


# In[ ]:


from IPython.display import display, HTML

# Display the map as HTML using the full path
display(HTML(r"C:\Users\ssindhu\restaurant_map.html"))


# In[ ]:


# Correlation Analysis
correlation_matrix = zomato[['rate', 'approx_costfor_two_people', 'votes']].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Numerical Features')
plt.show()


# In[ ]:





# In[ ]:


# Outlier Detection
plt.figure(figsize=(10, 6))
sns.boxplot(x=zomato['approx_costfor_two_people'])
plt.title('Boxplot for Approximate Cost for Two People')
plt.show()


# In[ ]:


plt.figure(figsize=(10, 6))
sns.boxplot(x=zomato['rate'])
plt.title('Boxplot for Restaurant Ratings')
plt.show()

