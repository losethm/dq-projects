#!/usr/bin/env python
# coding: utf-8

# ## Finding the Two Best Markets to Advertise in for an E-learning Product
# 
# In this project I will be trying to figure out the two best markets to advertise our product in - I am working for an e-learning company that offers online courses on programming. Most courses are on mobile and web development, but some other domains are also convered sauich as game development and data science.

# ### Understanding The Data
# To avoid spending money on organizing a survey, we'll first try to make use of existing data to determine whether we can reach any reliable result.
# 
# One good candidate for our purpose is [freeCodeCamp's 2017 New Coder Survey](https://medium.freecodecamp.org/we-asked-20-000-people-who-they-are-and-how-theyre-learning-to-code-fff5d668969). [freeCodeCamp](https://www.freecodecamp.org/) is a free e-learning platform that offers courses on web development. Because they run [a popular Medium publication](https://medium.freecodecamp.org/) (over 400,000 followers), their survey attracted new coders with varying interests (not only web development), which is ideal for the purpose of our analysis.
# 
# The survey data is publicly available in [this GitHub repository](https://github.com/freeCodeCamp/2017-new-coder-survey). Below, we'll do a quick exploration of the `2017-fCC-New-Coders-Survey-Data.csv` file stored in the `clean-data` folder of the repository we just mentioned. We'll read in the file using the direct link [here](https://raw.githubusercontent.com/freeCodeCamp/2017-new-coder-survey/master/clean-data/2017-fCC-New-Coders-Survey-Data.csv).
# 

# In[57]:


# reading in data and importing lbiraries
import pandas as pd
import matplotlib.pyplot as plt


get_ipython().magic('matplotlib inline')
direct_link = 'https://raw.githubusercontent.com/freeCodeCamp/2017-new-coder-survey/master/clean-data/2017-fCC-New-Coders-Survey-Data.csv'
fcc = pd.read_csv(direct_link, low_memory = 0)

print(fcc.shape)
pd.options.display.max_columns = 150
fcc.head()


# ### Checking for Sample Representativity
# As we mentioned earlier, most of the courses we offer are on web and mobile development, but we also cover many other domains, like data science, game development, etc. For the purpose of our analysis, we want to answer questions about a population of new coders that are interested in the subjects we teach. We'd like to know:
# - Where are these new coders located.
# - What are the locations with the greatest number of new coders.
# - How much money new coders are willing to spend on learning.
# 
# Before starting to analyze the sample data we have, we need to clarify whether it's representative for our population of interest and it has the right categories of people for our purpose.

# In[58]:


fcc['JobRoleInterest'].value_counts(normalize=True) * 100


# - There is a lot of interest in web development(full-stack, front-end, back-end).
# - There is a moderate amount of interest in Data Science
# - There is some interest in game development.
# 
# Many respondents are interested in more than one subject. Let's see how many respondents picked multiple interests.

# In[59]:


# Split each string in the 'JobRoleInterest' column
interests_no_nulls = fcc['JobRoleInterest'].dropna()
splitted_interests = interests_no_nulls.str.split(',')

# Frequency table for the var describing the number of options
n_of_options = splitted_interests.apply(lambda x: len(x)) # x is a list of job options
n_of_options.value_counts(normalize = True).sort_index() * 100


# Only 31.7% of respondents had a clear idea of what type of programming they wanted to learn, but it is clear the vast majority of students are unsure and have mixed interests. Mixed interests isn't a bad thing because we offer many different courses so students could take more than one if they chose to.
# 
# Since our main focus for courses is web and mobile development lets see how many respondents chose at least on of these two options.

# In[60]:


# Frequency table
web_or_mobile = interests_no_nulls.str.contains(
    'Web Developer|Mobile Developer') # returns an array of booleans
freq_table = web_or_mobile.value_counts(normalize = True) * 100
print(freq_table)

# Graph for the frequency table above
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

freq_table.plot.bar()
plt.title('Most Participants are Interested in \nWeb or Mobile Development',
          y = 1.08) # y pads the title upward
plt.ylabel('Percentage', fontsize = 12)
plt.xticks([0,1],['Web or mobile\ndevelopment', 'Other subject'],
           rotation = 0) # the initial xtick labels were True and False
plt.ylim([0,100])
plt.show()


# Roughly 86% of people surveyed are interested in either Web or Mobile development.
# 
# Next lets try to figure out what are the best markets to invest money in for advertising our courses. We want to find out:
# 
# - Where are new coders located
# - What are the locations with the most new coders
# - How much money are new coders willing to spend on learning.

# ### New Coders - Locations and Densities
# 
# Let's find out where new coders are located, and how many of them are in each location.
# 
# Our dataset the country that each customer is located in. For our analysis we will consider each country as an individual market, so we will try to find the two best countries to advertise in.

# In[61]:


fcc_good = fcc[fcc['JobRoleInterest'].notnull()].copy()

absolute_frequencies = fcc_good['CountryLive'].value_counts()
relative_frequencies = fcc_good['CountryLive'].value_counts(normalize = True) * 100

pd.DataFrame(data = {'Absolute Frequency': absolute_frequencies,
                    'Percentage': relative_frequencies}
            )


# Almost 46% of our potential customers are located in the US. India has the 2nd highest customer density with 7.7% which is closely followed by United Kingdom(4.6%) and Canada(3.8%)

# ### Which Customers are Willing to Spend on Learning

# Our company sells subscriptions for our service at $59/month. The column 'MoneyForLearning' shows the amount that customers have spent since they have started coding up until the survey.
# 
# Let's narrow down our analysis and only look at the four countries that have the highest frequency in our frequency table.
# 
# We're going to create a new column called 'MoneyForProgramming' that divides the money a respondent has spent on learning programming by the amount of months they have been learning how to program. This will give us an estimate on how much they are willing to spend per month.

# In[62]:


# Replace 0s with 1s to avoid division by 0
fcc_good['MonthsProgramming'].replace(0,1, inplace = True)

# New column for the amount of money each student spends each month
fcc_good['money_per_month'] = fcc_good['MoneyForLearning'] / fcc_good['MonthsProgramming']
fcc_good['money_per_month'].isnull().sum()


# We have 675 rows with null values for our new column. We're going to remove these for our analysis.

# In[63]:


# Keep only the rows with non-nulls in the `money_per_month` column 
fcc_good = fcc_good[fcc_good['money_per_month'].notnull()]


# In[64]:


# Remove the rows with null values in 'CountryLive'
fcc_good = fcc_good[fcc_good['CountryLive'].notnull()]

# Frequency table to check if we still have enough data
fcc_good['CountryLive'].value_counts().head()


# In[65]:


# Mean sum of money spent by students each month
countries_mean = fcc_good.groupby('CountryLive').mean()
countries_mean['money_per_month'][['United States of America',
                            'India', 'United Kingdom',
                            'Canada']]


# The results for India's money spent per month learning programming compared to Canada or the UK is quite surprising considering socio-economic factors such as GDP per capita, as India is quite low comparatively to Canada and the UK we would expect them to be less willing to spend.
# 
# Let's see if there are any extreme outliers skewing the data.

# In[66]:


# Isolate only the countries of interest
only_4 = fcc_good[fcc_good['CountryLive'].str.contains('United States of America|India|United Kingdom|Canada')]

# Box plots to visualize distributions
import seaborn as sns
sns.boxplot(y = 'money_per_month', x = 'CountryLive',
            data = only_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
         fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada']) # avoids tick labels overlap
plt.show()


# It's hard to see on the plot above if there's anything wrong with the data for the United Kingdom, India, or Canada, but we can see immediately that there's something really off for the US: two persons spend each month are willing to spend 50,000 or more for learning. Its not impossible but unlikely so lets stick with values less than 20,000 per month.

# In[67]:


# Isolate only those participants who spend less than 10000 per month
fcc_good = fcc_good[fcc_good['money_per_month'] < 20000]


# In[68]:


# Recompute mean sum of money spent by students each month
countries_mean = fcc_good.groupby('CountryLive').mean()
countries_mean['money_per_month'][['United States of America',
                            'India', 'United Kingdom',
                            'Canada']]


# In[69]:


# Isolate again the countries of interest
only_4 = fcc_good[fcc_good['CountryLive'].str.contains(
    'United States of America|India|United Kingdom|Canada')]

# Box plots to visualize distributions
sns.boxplot(y = 'money_per_month', x = 'CountryLive',
            data = only_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
         fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada']) # avoids tick labels overlap
plt.show()


# In[ ]:





# We can see some extreme outliers in India(values over $2500/month). This is relatively high for India. Lets investigate and see if these respondents attended any bootcamps.

# In[70]:


# Inspect the extreme outliers for India
india_outliers = only_4[
    (only_4['CountryLive'] == 'India') & 
    (only_4['money_per_month'] >= 2500)]
india_outliers


# None of these respondents attended any bootcamps. It's hard to know if these people actually did spend this much money or not. It's also possible that they did not understand the question from the survey - as it asked how much they have spent so far aside from tuition - perhaps they were enrolled in university and misunderstood. I have decided to remove these rows as well.

# In[71]:


# Remove the outliers for India
only_4 = only_4.drop(india_outliers.index) # using the row labels


# Lets also look at the extreme outliers for the US which includes any values over $6000.

# In[72]:


us_outliers = only_4[
    (only_4['CountryLive'] == 'United States of America') &
    (only_4['money_per_month'] >= 6000)
]

us_outliers


# Out of the 11 extreme outliers 6 of them attended a bootcamp which explains the higher amount of money spent for learning. For the other 5, like the India outlier's it is hard to figure out from the data where they could have spent that much money on learning, so I will remove these rows as well.
# 
# The data shows that eight respondents had only been programming for at most three months, and if they did attend a bootcamp during this time it would explain why their money spent per month was so high and it is likely unrealistic as once their bootcamp was completed their spending would have had a steep decline.
# 
# I am going to remove respondents that:
# - Didnt attend any bootcamps
# - Had been programming for three months or less at the time they completed the survey.

# In[73]:


no_bootcamp = only_4[
    (only_4['CountryLive'] == 'United States of America') &
    (only_4['money_per_month'] >= 6000) &
    (only_4['AttendedBootcamp'] == 0 )
]

only_4 = only_4.drop(no_bootcamp.index)

less_than_3_months = only_4[
    (only_4['CountryLive'] == 'United States of America') &
    (only_4['money_per_month'] >= 6000) &
    (only_4['MonthsProgramming'] <= 3)
]

only_4 = only_4.drop(less_than_3_months.index)


# Next let's look at Canada's outliers - that is a person who spends more than roughly $5000/month.

# In[76]:


canada_outliers = only_4[
    (only_4['CountryLive'] == 'Canada') &
    (only_4['money_per_month'] >= 5000)
]
canada_outliers


# This person is similar to some of the outliers in the US. They recently attended a bootcamp and have only been programming for two months. I will remove this outlier.

# In[78]:


only_4 = only_4.drop(canada_outliers.index)


# Now I am going to recompute the mean values of each country without the outliers.

# In[80]:


# Recompute mean sum of money spent by students each month
only_4.groupby('CountryLive').mean()['money_per_month']


# In[82]:


# Visualize the distributions again
sns.boxplot(y = 'money_per_month', x = 'CountryLive',
            data = only_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
          fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada']) # avoids tick labels overlap
plt.show()


# ### Choosing the Best Two Markets

# The US is obviously a country that we should be focusing our advertising in. There are a lot of new coders in the country, and they are willing to spend the most amount of money per month on coding ($143) compared to the other four countries.
# 
# For the 2nd country it's not as clear who we should focus our advertising budget on. I do think that we should not consider the UK at this time, as they are only willing to spend $45 on average per month and our monthly subscription is 59.
# 
# Going by the amount of money new coders are willing to spend per month Canada is enticing compared to India is $93 compared to 65, but we also need to consider that India could be a better choice due to its much larger population and looking at the table below has almost double the number of respondents to the survey than Canada.

# In[84]:


# Frequency table for the 'CountryLive' column
only_4['CountryLive'].value_counts(normalize = True) * 100


# ### Final Recommendations

# I think that we have several different options to split our advertising budget, they are as follows:
# 
# 1. Advertise in the US, India and Canada and split the budget
#     - 60% for the US, 25% for India, 15% for Canada
# 2. Advertise Only in the US and India or US and Canada
#     - 70% for the US 30% for India
#     - 75% for the US 25% for Canada
# 3. Advertise only in the US
# 
# I think that this analysis could be forwarded to the marketing team and let them decide the best course of action. We could also try to run a survey in the US, India and Canada to gather more information.
