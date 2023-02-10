#!/usr/bin/env python
# coding: utf-8

# ## Finding Heavy Traffic Indicators on the I-94
# We are going to look at and analyze a dataset about the westbound traffic on I-94 Interstate highway. The dataset has been made available at: https://archive.ics.uci.edu/ml/datasets/Metro+Interstate+Traffic+Volume
# 
# The goal of our analysis is to try to determine a few indicators of heavy traffic on the I-94. These indicators could include type of weather, time of day, time of week, etc.

# In[2]:


#import libraries
import pandas as pd

#read the data
traffic = pd.read_csv('Metro_Interstate_Traffic_Volume.csv')

#view first 5 rows
print(traffic.head(5))

#view last 5 rows
print(traffic.tail(5))

#find more info on data set
print(traffic.info())


# The data set has 48204 rows and 9 columns. Each row describes traffic and weather data every hour starting at `2012-10-02 09:00:00` and ending at `2018-09-30 23:00:00`. This represents the hourly data for almost 6 years.
# 
# The data was recorded at a station midway between Mineapolis and St.Paul - because of this we wont make generalizations about the I-94 as a whole.

# In[3]:


#import libraries
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

#plot histogram to see distribution of traffic_volume column
plt.hist(traffic['traffic_volume'])
plt.show()

#look up some key statistics on traffic_volume column
print(traffic['traffic_volume'].describe())


# Westbound traffic on the I-94's highest volume was 7280 cars in one hour. The lowest amount was 0. 25% of the time westbound traffic had at least 1193 cars in an hour, but on average there was about 3260 cars in an hour, and 75% of the time there was 4933 cars per hour. These are large differences. One possibility that could contribute to varying volume of cars could be the time of day. Let's see if there is a noticeable difference in the volume of cars traveling westbound and the I-94 near Mineapolis and St. Paul

# ## Traffic Volume: Day vs. Night
# To look into the difference of traffic volume between day and night we will need to split the data into two parts.
# - Daytime data: 7am-7pm
# - Nighttime data: 7pm to 7am

# In[4]:


#convert date_time column to datetime data type
traffic['date_time'] = pd.to_datetime(traffic['date_time'])

#isolate night traffic data
night = traffic[(traffic['date_time'].dt.hour >= 19) | (traffic['date_time'].dt.hour < 7)]
print(night.shape)

#isolate the day traffic data
day = traffic[(traffic['date_time'].dt.hour < 19) & (traffic['date_time'].dt.hour >= 7)]
print(day.shape)


# In[5]:


plt.figure(figsize=(11,3.5))

plt.subplot(1,2,1)
plt.hist(day['traffic_volume'])
plt.title('Traffic Volume: 7am-7pm')
plt.xlabel('Traffic Volume')
plt.ylabel('Frequency')
plt.xlim(-100, 7500)

plt.subplot(1,2,2)
plt.hist(night['traffic_volume'])
plt.title('Traffic Volume: 7pm-7am')
plt.xlabel('Traffic Volume')
plt.ylabel('Frequency')
plt.xlim(-100, 7500)

plt.show()


# In[6]:


print('Daytime Traffic Volume Data')
print(day['traffic_volume'].describe())
print('\n')
print('Nighttime Traffic Volume Data')
print(night['traffic_volume'].describe())


# The histogram that shows the distribution of traffic volume during the day is left skewed. This means that most of the traffic volume values are high — there are 4,252 or more cars passing the station each hour 75% of the time (because 25% of values are less than 4,252).
# 
# The histogram displaying the nighttime data is right skewed. This means that most of the traffic volume values are low — 75% of the time, the number of cars that passed the station each hour was less than 2,819.
# 
# Although there are still measurements of over 5,000 cars per hour, the traffic at night is generally light. Our goal is to find indicators of heavy traffic, so we'll only focus on the daytime data moving forward.

# ## Time Indicators
# Previously, we determined that the traffic at night is generally light. Our goal is to find indicators of heavy traffic, so we decided to only focus on the daytime data moving forward.
# 
# One of the possible indicators of heavy traffic is time. There might be more people on the road in a certain month, on a certain day, or at a certain time of the day.
# 
# We're going to look at a few line plots showing how the traffic volume changed according to the following parameters:
# 
# - Month
# - Day of the week
# - Time of day

# In[10]:


#get monthly traffic averages for daytime traffic
day['month'] = day['date_time'].dt.month
by_month = day.groupby('month').mean()
by_month['traffic_volume']


# In[14]:


plt.plot(by_month.index, by_month['traffic_volume'])
plt.show()


# It appears that there is less traffic in the winter months(November-March) One outlier is the month of July. For some reason there is a sever drop off in traffic in july. Lets try to look at the month of July and see how traffic changed over the years.

# In[19]:


day['year'] = day['date_time'].dt.year
july_only = day[day['month'] == 7]
july_only.groupby('year').mean()['traffic_volume'].plot.line()
plt.show()


# In[ ]:





# Looking at the chart above traffic seemed high in all years in July except for 2016. It is likely the highway was under construction or closed for parts of July in 2016.

# ## Time Indicators - Day of the week

# In[20]:


day['day_of_week'] = day['date_time'].dt.dayofweek
by_day_of_week = day.groupby('day_of_week').mean()
by_day_of_week['traffic_volume'].plot.line()
plt.show()


# Traffic seems to be heaviest on business days Mon-Fri remaining almost above 5000 cars/h. On weekends we see a 20-30% drop in 
# traffic ranging between 4000-3500 cars/h on Saturday and Sunday respectively.

# ## Time Indicators - Time of Day
# Now we are going to see if the time of day effects the flow of traffic at all, but we are going to split business days and weekends and look at them seperately.

# In[23]:


#create hour column
day['hour'] = day['date_time'].dt.hour
business_days = day.copy()[day['day_of_week'] <= 4] #day 4 == Friday
weekend_day = day.copy()[day['day_of_week'] >= 5] #day 5 == Saturday
by_hour_business = business_days.groupby('hour').mean()
by_hour_weekend = weekend_day.groupby('hour').mean()

print(by_hour_business['traffic_volume'])
print(by_hour_weekend['traffic_volume'])


# In[35]:


plt.figure(figsize=(11,3.5))

plt.subplot(1,2,1)
by_hour_business['traffic_volume'].plot.line()
plt.ylim(1500, 6500)
plt.xlim(6,20)
plt.ylabel('Traffic Volume')
plt.xlabel('Hour')
plt.title('Business day traffic hourly traffic volume')

plt.subplot(1,2,2)
by_hour_weekend['traffic_volume'].plot.line()
plt.ylim(1500, 6500)
plt.xlim(6,20)
plt.xlabel('Hour')
plt.ylabel('Traffic Volume')
plt.title('Weekend hourly traffic volume')
plt.show()


# We can see as noted earlier, traffic volume on the weekend overall is much lower than on business days. Business days are busiest around 7-8 and again around 4-5. These times represent when most people are making their daily commute to and from work. One Difference between weekend traffic is that it actually peaks around 12pm and stays around that level for 4 hours and then begins to drop off again.
# 
# To summarize our findings so far:
# - Traffic is higher during warmer months
# - Traffic is higher during business days
# - Traffic is highest on business days around 07:00 and 16:00
# 

# ## Weather Indicators
# Another possible indicator of heavy traffic is weather. The dataset provides us with a few useful columns about weather: `temp, rain_1h, snow_1h, clouds_all, weather_main, weather_description`.
# 
# A few of these columns are numerical so let's start by looking up their correlation values with `traffic_volume`.

# In[37]:


#find correlation of all columns to traffic_volume
day.corr()['traffic_volume']


# The `temp` column shows the highest correlation to traffic volume, but it is only +0.13. Overall it appears there is a very weak correlation of weather on traffic volume.

# In[48]:


#scatter plot of temp vs traffic volume
plt.scatter(day['traffic_volume'], day['temp'])
plt.xlabel('Traffic Volume')
plt.ylabel('Temp')
plt.ylim(220, 320)
plt.show()


# ## Types of Weather
# Lets take a look at the average traffic volume based on the type of weather and see if there are any outliers.

# In[54]:


by_weather_main = day.groupby('weather_main').mean()
by_weather_description = day.groupby('weather_description').mean()

by_weather_main['traffic_volume'].plot.barh()
plt.title('Traffic Volume by Type of Weather')
plt.xlabel('Traffic Volume')
plt.ylabel('Weather Type')
plt.show()


# In[55]:


by_weather_description['traffic_volume'].plot.barh(figsize=(5,10))
plt.show()


# It looks like there are three weather types where traffic volume exceeds 5,000:
# 
# - Shower snow
# - Light rain and snow
# - Proximity thunderstorm with drizzle
# 
# It's not clear why these weather types have the highest average traffic values — this is bad weather, but not that bad. Perhaps more people take their cars out of the garage when the weather is bad instead of riding a bike or walking.

# ## Conclusion
# - Time indicators
#  - The traffic is usually heavier during warm months (March–October) compared to cold months (November–February).
#  - The traffic is usually heavier on business days compared to the weekends.
#  - On business days, the rush hours are around 7 and 16.
# - Weather indicators
#  - Shower snow
#  - Light rain and snow
#  - Proximity thunderstorm with drizzle
