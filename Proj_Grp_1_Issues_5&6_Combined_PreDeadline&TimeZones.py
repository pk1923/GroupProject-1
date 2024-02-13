#!/usr/bin/env python
# coding: utf-8

# # 1. Install necessary packages and libraries
# Run the following four installs only once

# In[1]:


get_ipython().system('pip install geopy')


# In[2]:


get_ipython().system('pip install tzwhere')


# In[3]:


get_ipython().system('pip install timezonefinder')


# In[4]:


get_ipython().system('pip install pytz')


# In[1]:


import pandas as pd
import datetime
import pytz
import plotly.graph_objects as go
import pandas as pd
import ipywidgets as widgets
import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

import numpy as np


# # 2. Define Variables

# In[2]:


# Initialize Nominatim and TimezoneFinder
geolocator = Nominatim(user_agent="geocity")
tf = TimezoneFinder()


# # 3. Make the Functions

# In[3]:


def get_timezone_from_city(city):
    location = geolocator.geocode(city)
    if location:
        timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
        return timezone_str
    return None

# Function to standardize city names
def standardize_city_name(city):
    city = city.lower()
    if city in ["saranda", "sarande"]:
        return "Sarandë, Albania"
    return city

def get_predeadline(deadline, buffer_days=1):
    """Subtract buffer days from deadline date to get the pre-deadline date."""
    return deadline - datetime.timedelta(days=buffer_days)


# # 4. Load CSV and convert DATE column to datetimes

# In[4]:


file_path = "GP1 Dataset_ Assignments.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')
df['DATE'] = pd.to_datetime(df['DATE'])

dfs = []
timezones = set(df['TIMEZONE'])
for i in timezones:
    df1 = df.loc[df['TIMEZONE'] == i].copy()
    df1['DATE'] = df['DATE'].dt.tz_localize(i)
    df1['DATE'] = df1['DATE'] + datetime.timedelta(hours=23,minutes=59)
    dfs.append(df1)
    
df_merged = pd.concat([dfs[0],dfs[1]])
df_merged.sort_index(inplace=True)
df = df_merged
df


# # 5. Ask the user for their city

# In[7]:


user_city = standardize_city_name(input("Enter the city you are in: "))
user_timezone = get_timezone_from_city(user_city)
print(user_timezone)


# # 6. Convert due dates to the user's local timezone and calculate for pre-deadline dates

# In[8]:


if user_timezone:
    user_tz = pytz.timezone(user_timezone)
else:
    user_tz = datetime.datetime.now().astimezone().tzinfo

df['LOCAL_DUE_DATE'] = df['DATE'].apply(lambda x: x.astimezone(user_tz))
df['PREDEADLINE'] = df['LOCAL_DUE_DATE'].apply(lambda x: get_predeadline(x))

# Define the order of the columns, including the new PREDEADLINE column
column_order = ['ITEM#', 'COURSE', 'ASSIGNMENT NAME', 'DESCRIPTION', 'DATE', 'LOCAL_DUE_DATE', 'PREDEADLINE', 'DONE']

# Reorder the DataFrame according to the defined column order
df = df[column_order]

# Print the DataFrame to check the results
print(df.head())


# # 7. Save the modified DataFrame to a new file

# In[74]:


#new_file_path = file_path.rsplit('\\', 1)[0] + '\\GP1 Dataset_ Assignments_PreDeadline.csv'
df.to_csv('GP1 Dataset_ Assignments_PreDeadline.csv', index=False)
#print(f"File saved as: {new_file_path}")

