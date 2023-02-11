#!/usr/bin/env python
# coding: utf-8

# # Analyzing Star Wars Survey Data

# In[109]:


#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# In[110]:


#read the data
star_wars = pd.read_csv("star_wars.csv", encoding="ISO-8859-1")


# In[111]:


star_wars.head(10)


# In[112]:


star_wars.columns


# ### Cleaning and Mapping Yes/No Columns

# In[113]:


#create mapping for yes/no columns
yes_no = {
    "Yes": True,
    "No": False
}

#convert columns to bool type with True or False values
star_wars['Have you seen any of the 6 films in the Star Wars franchise?'] = star_wars['Have you seen any of the 6 films in the Star Wars franchise?'].map(yes_no)
star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'] = star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'].map(yes_no)


# In[114]:


#check if above worked
star_wars['Have you seen any of the 6 films in the Star Wars franchise?'].value_counts(dropna=False)


# In[115]:


star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'].value_counts(dropna=False)


# ### Cleaning and Mapping Checkbox Columns

# In[116]:


#column names
names = star_wars.columns[3:9]
names


# In[117]:


#map for new column names
name_map = {
    "Which of the following Star Wars films have you seen? Please select all that apply.":"seen_1",
    'Unnamed: 4' : 'seen_2',
    "Unnamed: 5" : "seen_3",
    "Unnamed: 6" : 'seen_4',
    "Unnamed: 7" : 'seen_5',
    'Unnamed: 8' : 'seen_6'
}

#rename columns using map above
star_wars = star_wars.rename(columns=name_map)


# In[118]:


#check column names
star_wars.columns


# In[119]:


#mapping col values
seen_mapping = {
    "Star Wars: Episode I  The Phantom Menace": True,
    np.nan: False,
    "Star Wars: Episode II  Attack of the Clones": True,
    "Star Wars: Episode III  Revenge of the Sith": True,
    "Star Wars: Episode IV  A New Hope": True,
    "Star Wars: Episode V The Empire Strikes Back": True,
    "Star Wars: Episode VI Return of the Jedi": True
}


# In[120]:


#apply map to columns
for col in star_wars.columns[3:9]:
    star_wars[col] = star_wars[col].map(seen_mapping)

#check
star_wars.head()


# ### Cleaning the Ranking Columns

# In[121]:


#convert columns to type float
star_wars[star_wars.columns[9:15]] = star_wars[star_wars.columns[9:15]].astype(float)


# In[122]:


#create ranking map for name changes
star_wars = star_wars.rename(columns={
        "Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.": "ranking_1",
        "Unnamed: 10": "ranking_2",
        "Unnamed: 11": "ranking_3",
        "Unnamed: 12": "ranking_4",
        "Unnamed: 13": "ranking_5",
        "Unnamed: 14": "ranking_6"
        })
star_wars.columns[9:15]


# ### Finding the Highest Ranked Movies

# In[127]:


movie_rank_cols = star_wars[['ranking_1','ranking_2', 'ranking_2', 'ranking_3', 'ranking_4', 'ranking_5', 'ranking_6']].mean()

movie_rank_cols


# In[135]:


get_ipython().run_line_magic('matplotlib', 'inline')

plt.bar(range(6), star_wars[star_wars.columns[9:15]].mean())

plt.show()


# #### Observation
# So it appears that Episodes 4,5 and 6 and ranked on average higher than 1, 2 and 3. Episide 5 was the highest rated movie overall and episode 3 was the lowest. Episode 4, 5 and 6 are all of the original old Star Wars movies and 1, 2 and 3 are the newer ones. It's hard to say why these movies from different eras were rated differently. Perhaps nostalgia played a role in the ratings differences.

# ### Finding the Most Viewed Movie

# In[137]:


plt.bar(range(6), star_wars[star_wars.columns[3:9]].sum())
plt.show()


# #### Observation
# More people have seen the older movies than the newer ones so that reinforces the idea that the older movies were more popular.

# ### Exploring Gender Specific Results

# In[138]:


#two new dataframes with data from male and female survey takers
males = star_wars[star_wars['Gender'] == 'Male']
females = star_wars[star_wars['Gender'] == 'Female']


# In[156]:


#
fig, ax = plt.subplots(1,2, figsize=(12,5))



#plot male movie rankings
ax[0].bar(range(6), males[males.columns[9:15]].mean())
ax[0].set_title('Movie Rankings by Males')

#plot female movie rankings
ax[1].bar(range(6), females[females.columns[9:15]].mean())
ax[1].set_title('Movie Ranking by Females')

plt.show()


# #### Observation
# Males were very clear cut in their opinions, rating the older movies much higher overall than the newer ones. Females were also similar in their rankings, but actually rated Episode I better than Episode III. Both males and females agreed that Episide II was the worst of the movies, and Episode IV was the best. Both males and females seemed to prefer the older movies to the new ones.

# In[158]:


fig, ax = plt.subplots(1,2, figsize=(12,5))



#plot male movie rankings
ax[0].bar(range(6), males[males.columns[3:9]].sum())
ax[0].set_title('Most Viewed by Males')

#plot female movie rankings
ax[1].bar(range(6), females[females.columns[3:9]].sum())
ax[1].set_title('Most Viewed by Females')

plt.show()


# #### Observation
# Both males and females viewed the older movies on average more than the newer ones. Overall the older movies were more popular than the newer ones. Episode IV was viewed the most by both groups.

# In[ ]:




