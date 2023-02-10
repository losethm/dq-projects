#!/usr/bin/env python
# coding: utf-8

# # Read in the data

# In[31]:


import pandas as pd
import numpy
import re
import matplotlib.pyplot as plt

data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]

data = {}

for f in data_files:
    d = pd.read_csv("schools/{0}".format(f))
    data[f.replace(".csv", "")] = d


# # Read in the surveys

# In[32]:


all_survey = pd.read_csv("schools/survey_all.txt", delimiter="\t", encoding='windows-1252')
d75_survey = pd.read_csv("schools/survey_d75.txt", delimiter="\t", encoding='windows-1252')
survey = pd.concat([all_survey, d75_survey], axis=0)

survey["DBN"] = survey["dbn"]

survey_fields = [
    "DBN", 
    "rr_s", 
    "rr_t", 
    "rr_p", 
    "N_s", 
    "N_t", 
    "N_p", 
    "saf_p_11", 
    "com_p_11", 
    "eng_p_11", 
    "aca_p_11", 
    "saf_t_11", 
    "com_t_11", 
    "eng_t_11", 
    "aca_t_11", 
    "saf_s_11", 
    "com_s_11", 
    "eng_s_11", 
    "aca_s_11", 
    "saf_tot_11", 
    "com_tot_11", 
    "eng_tot_11", 
    "aca_tot_11",
]
survey = survey.loc[:,survey_fields]
data["survey"] = survey


# # Add DBN columns

# In[33]:


data["hs_directory"]["DBN"] = data["hs_directory"]["dbn"]

def pad_csd(num):
    string_representation = str(num)
    if len(string_representation) > 1:
        return string_representation
    else:
        return "0" + string_representation
    
data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(pad_csd)
data["class_size"]["DBN"] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]


# # Convert columns to numeric

# In[34]:


cols = ['SAT Math Avg. Score', 'SAT Critical Reading Avg. Score', 'SAT Writing Avg. Score']
for c in cols:
    data["sat_results"][c] = pd.to_numeric(data["sat_results"][c], errors="coerce")

data['sat_results']['sat_score'] = data['sat_results'][cols[0]] + data['sat_results'][cols[1]] + data['sat_results'][cols[2]]

def find_lat(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lat = coords[0].split(",")[0].replace("(", "")
    return lat

def find_lon(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lon = coords[0].split(",")[1].replace(")", "").strip()
    return lon

data["hs_directory"]["lat"] = data["hs_directory"]["Location 1"].apply(find_lat)
data["hs_directory"]["lon"] = data["hs_directory"]["Location 1"].apply(find_lon)

data["hs_directory"]["lat"] = pd.to_numeric(data["hs_directory"]["lat"], errors="coerce")
data["hs_directory"]["lon"] = pd.to_numeric(data["hs_directory"]["lon"], errors="coerce")


# # Condense datasets

# In[35]:


class_size = data["class_size"]
class_size = class_size[class_size["GRADE "] == "09-12"]
class_size = class_size[class_size["PROGRAM TYPE"] == "GEN ED"]

class_size = class_size.groupby("DBN").agg(numpy.mean)
class_size.reset_index(inplace=True)
data["class_size"] = class_size

data["demographics"] = data["demographics"][data["demographics"]["schoolyear"] == 20112012]

data["graduation"] = data["graduation"][data["graduation"]["Cohort"] == "2006"]
data["graduation"] = data["graduation"][data["graduation"]["Demographic"] == "Total Cohort"]


# # Convert AP scores to numeric

# In[36]:


cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']

for col in cols:
    data["ap_2010"][col] = pd.to_numeric(data["ap_2010"][col], errors="coerce")


# # Combine the datasets

# In[37]:


combined = data["sat_results"]

combined = combined.merge(data["ap_2010"], on="DBN", how="left")
combined = combined.merge(data["graduation"], on="DBN", how="left")

to_merge = ["class_size", "demographics", "survey", "hs_directory"]

for m in to_merge:
    combined = combined.merge(data[m], on="DBN", how="inner")

combined = combined.fillna(combined.mean())
combined = combined.fillna(0)


# # Add a school district column for mapping

# In[38]:


def get_first_two_chars(dbn):
    return dbn[0:2]

combined["school_dist"] = combined["DBN"].apply(get_first_two_chars)


# # Find correlations

# In[39]:


correlations = combined.corr()
correlations = correlations["sat_score"]
print(correlations)


# # Plotting survey correlations

# In[40]:


# Remove DBN since it's a unique identifier, not a useful numerical value for correlation.
survey_fields.remove("DBN")


# In[42]:


get_ipython().run_line_magic('matplotlib', 'inline')

combined.corr()['sat_score'][survey_fields].plot.bar()


# The columns `N_s`, `N_t` and `N_p` all have relatively high correlations to `sat_score`. These columns represent the number of students, teacher and parents that responded to the survey. It makes sense to me that students that responded to the survey had better sat scores as you could infer students that responded to the survey are also more likely to put more time into their studies.
# 
# `saf_t` and `saf_s` are also relatively highly correlated to sat scores. This makes sense as students that do not feel safe in their learning environment are likely not going to perform well on tests.
# 
# `aca_s` corresponds to students academic expectations. Students that have higher expectations likely put in more work and therefore scored higher on their sats.

# In[44]:


plt.scatter(combined['saf_s_11'], combined['sat_score'])

plt.show()


# Looking at the figure above we can see that there is a weak positive correlation between `saf_s`(student safety and respect score) and SAT scores.

# In[49]:


boros = combined.groupby('boro').agg(numpy.mean)['saf_s_11']
print(boros)


# The average SAT score by borough increases slightly as the safety score increases. The borough with the lowest safety score was Brooklyn at about 6.37, and the highest was Manhattan at about 6.83.

# # Exploring Race and SAT Scores

# In[57]:


race_fields = [
    'white_per',
    'asian_per',
    'black_per',
    'hispanic_per'
]

combined.corr()['sat_score'][race_fields].plot.bar()


# It appears that a higher percentage of white or asian students at a school correlates to higher SAT scores. Inversely, a higher percentage of black and hispanic students at a school correlates negatively with SAT scores.

# In[59]:


combined.plot.scatter('hispanic_per', 'sat_score')


# Looking at the table above we can see a cluster of schools that have an extremely high hispanic pop(>95%) and very low SAT scores. Lets look closer and see if we can find out anything about these schools.

# In[62]:


print(combined[combined['hispanic_per'] > 95]['SCHOOL NAME'])


# After looking on google and wikipedia most of these schools are for recent immigrants to the US. Likely these students English is not great and would contribute to lower SAT scores.

# In[64]:


print(combined[(combined['hispanic_per'] < 10) & (combined['sat_score'] > 1800)]['SCHOOL NAME'])


# All the schools above are schools that specialize in math and science and only admit students that achieve certain scores on entrance exams. 

# # Exploring Gender and SAT Scores

# In[66]:


genders = ['male_per', 'female_per']
combined.corr()['sat_score'][genders].plot.bar()


# It appears that schools with a higher percentage of females have a slightly positive correlation to SAT scores, and schools with a high percentage of males had a slightly negative correlation to SAT scores.

# In[70]:


combined.plot.scatter('female_per','sat_score')


# In[71]:


print(combined[(combined['female_per'] > 60) & (combined['sat_score'] > 1700)]['SCHOOL NAME'])

