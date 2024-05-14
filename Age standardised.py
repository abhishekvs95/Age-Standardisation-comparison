#!/usr/bin/env python
# coding: utf-8

# # Study on crude and age standardised death rates(ASDR) due to chronic obstructive pulmonary disease (COPD) for Uganda and USA, 2019

# ## Analysis Methodology and Results Interpretation
# 
# ### (i) Steps taken
# 
# Three data sources are used as provided. For population data, data having 5-year age groups were used. Pandas library was employed for data loading and manipulation. Separate dataframes were created for Uganda and the USA, incorporating population, chronic obstructive pulmonary disease(COPD) death rates, and the WHO standard population. The UN data was filtered for the two countries and the year 2019, with a new age category ('85+') formed for ages over 85. After removing unnecessary rows and columns for clarity, the UN, WHO, and COPD data were merged for both countries. Then Crude death rates and Age Standardised Death Rates(ASDR) are calculated using formulas below:
# 
#  Total deaths, D = (1/100) * Σ(DeathRate_i * Population_i)
# 
# Crude_death_rate_per_100000 = (D/Total_population_of_country) * 100000
# 
# ASDR = (1/100) * Σ(DeathRate_i * Population_Percentage_i)
# 
# ### (ii) Assumptions made
# 
# Assumptions made are: similar population data was used across the datasets; age standardisation is accurate to adjust for differences in population distributions; population remained stable for the year 2019 across studies.
# 
# ### (iii) Results interpretation
# 
# Crude Death rate per 100000 for Uganda was 5.8 and USA was 57.2. Age Standardised Death Rates(ASDR) for Uganda was 28.7 and for USA was 28.4. The variation can be ascribed to diverse factors. Population demographics play a pivotal role, with Uganda boasting a younger populace compared to the USA. This makes crude deaths higher in USA as it has more aged population who are more vulnerable to COPD. Convergence of ASDR can be due to advanced healthcare infrastructure in the USA facilitates improved COPD diagnosis and management, whereas Uganda grapples with disparities. Divergent risk factors like smoking and environmental pollutants further shape COPD prevalence. Discrepancies in data collection and socioeconomic disparities also influence mortality rates, accentuating the complexity of global health outcomes.

# ## 1. Loading Libraries (Pandas is all you need ;))

# In[76]:


import pandas as pd


# ## 2. Loading Datasets using pandas

# In[249]:


#Loading age specific death rate due to COPD
# Data accessed from https://owid.notion.site/Data-analysis-exercise-Our-World-in-Data-Junior-Data-Scientist-application-ab287a3c07264b4d91aadc436021b8c0
DR_COPD = pd.read_csv('/Users/abhishek/Downloads/Age_specific_DR_COPD_2019.csv')


# In[250]:


DR_COPD.head(20)


# In[212]:


#Renaming Age group column as this will be used for joining dataframes
DR_COPD = DR_COPD.rename(columns={'Age group (years)': 'Age group'})


# In[213]:


#Loading WHO age standardised population data
# Data accessed from https://cdn.who.int/media/docs/default-source/gho-documents/global-health-estimates/gpe_discussion_paper_series_paper31_2001_age_standardization_rates.pdf
who = pd.read_csv('/Users/abhishek/Downloads/WHO_age_standardisation.csv')


# In[214]:


who.head(20)


# In[215]:


# UN World Population Prospects 2022
# Population data used here can be downloaded from https://population.un.org/wpp/Download/Standard/CSV/#:~:text=1950%2D2100%2C%20medium%20(ZIP%2C%2012.38%20MB)
# Data from this source has 'AgeGrp' where population is divided into 5 year age groups 
popln = pd.read_csv('/Users/abhishek/Downloads/WPP2022_PopulationByAge5GroupSex_Medium.csv')


# In[216]:


print(popln.columns.values)


# ## 3. Processing Data

# In[ ]:


###  DATA PROCESSING STEPS ARE AS FOLLOWS ###
# 1. Create separate dataframes for USA and Uganda population to make understanding data easy
# 2. Filter Location for the two countries and Time (year) as 2019
# 3. Remove columns not necessary
# 4. Since WHO and COPD data has all age groups above 85 under one category of '85+',
# we need to group all ages under 85+ in the population data too
# This is done by creating a new row as dataframe which sums up all ages above 85
# and concatenating it with original data as new row. Then remove the rows used for calucaltion
# 5. Merge WHO and COPD dataframes with the two countries separately for easier calculation


# In[217]:


# Filtering and saving data related to Uganda for the year 2019
popln_uganda = popln[(popln['Location'] == 'Uganda') & (popln['Time'] == 2019)]


# In[219]:


# Using filter() to keep only desired columns
popln_uganda = popln_uganda.filter(['Location', 'AgeGrp', 'PopTotal'])


# In[220]:


popln_uganda.head(25)


# In[221]:


#Creating Age group of 85+ for making it similar to CPOD and WHO data
# Summing up Population in age categories from 85 upwards as 85+
popln_85_above_uganda = popln_uganda['PopTotal'].tail(4).sum()


# In[222]:


# New dataframe where 85+ population is stored as row
df_popln_85_above_uganda = pd.DataFrame([['Uganda','85+',popln_85_above_uganda]], columns=['Location','AgeGrp','PopTotal'])


# In[223]:


# Removing all rows above 85 under AgeGrp from original dataframe
popln_uganda = popln_uganda[~popln_uganda['AgeGrp'].isin(['85-89', '90-94', '95-99', '100+'])]


# In[224]:


# Concatenating two dataframes so that we get standard Age groups
popln_uganda = pd.concat([popln_uganda, df_popln_85_above_uganda])


# In[225]:


#Renaming the AgeGrp column to Age group
popln_uganda = popln_uganda.rename(columns={'AgeGrp': 'Age group'})


# In[248]:


popln_uganda.head(20)


# In[227]:


### All the steps used to process Uganda was done for USA as well ###

#Filtering and saving data related to United States of America for the year 2019
popln_usa = popln[(popln['Location'] == 'United States of America') & (popln['Time'] == 2019)]


# In[228]:


popln_usa = popln_usa.filter(['Location', 'AgeGrp', 'PopTotal'])


# In[230]:


popln_85_above_usa = popln_usa['PopTotal'].tail(4).sum()


# In[231]:


new_row_usa = {'Location': 'United States of America', 'AgeGrp': '85+', 'PopTotal': popln_85_above_usa}
df_popln_85_above_usa = pd.DataFrame([['United States of America','85+',popln_85_above_usa]], columns=['Location','AgeGrp','PopTotal'])


# In[232]:


popln_usa = popln_usa[~popln_usa['AgeGrp'].isin(['85-89', '90-94', '95-99', '100+'])]


# In[233]:


popln_usa = pd.concat([popln_usa, df_popln_85_above_usa])


# In[234]:


popln_usa = popln_usa.rename(columns={'AgeGrp': 'Age group'})


# In[235]:


popln_usa.head(20)


# In[236]:


# Merging COPD, WHO with Population data of Uganda and USA for making calculations easier

COPD_uganda = pd.merge(DR_COPD, who, on='Age group')
COPD_uganda = pd.merge(COPD_uganda, popln_uganda, on='Age group')


# In[237]:


COPD_usa = pd.merge(DR_COPD, who, on='Age group')
COPD_usa = pd.merge(COPD_usa, popln_usa, on='Age group')


# In[238]:


COPD_uganda.head(20)


# In[239]:


COPD_usa.head(20)


# ## 4. Crude Death Rates

# In[ ]:


# The formula used for total deaths (D) is: 

# D = (1/100) * Σ(DeathRate_i * Population_i)

# 1/100 is used here for unit conversion as deaths were per 100000 and 
# population is provided in thousands

# Crude_death_rate_per_100000 = (D/Total_population_of_country) * 100000


# In[240]:


#calculation of crude death rates

#Total deaths in Uganda
COPD_uganda['Total Deaths'] = (COPD_uganda['Death rate, Uganda, 2019'] * COPD_uganda['PopTotal']) / 100
total_deaths_uganda = COPD_uganda['Total Deaths'].sum()
# Total population of Uganda as of 2019
total_population_uganda = (COPD_uganda['PopTotal'].sum())*1000
# Crude death rate per 100000 Uganda
crude_death_rate_uganda = round(total_deaths_uganda/total_population_uganda*100000, 1)
print("Crude Death Rates for Uganda per 100000:", crude_death_rate_uganda)


# In[241]:


#Crude death rate per 100000 USA
COPD_usa['Total Deaths'] = (COPD_usa['Death rate, United States, 2019'] * COPD_usa['PopTotal']) / 100
total_deaths_usa = COPD_usa['Total Deaths'].sum()
# Total population of USA as of 2019
total_population_usa = (COPD_usa['PopTotal'].sum())*1000
# Crude death rate per 100000 USA
crude_death_rate_usa = round(total_deaths_usa/total_population_usa*100000, 1)
print("Crude Death Rates for USA per 100000:", crude_death_rate_usa)


# ## 5. Age Standardised Death Rates

# In[ ]:


# For the Age Standardized Death Rate (ASDR) per 100000, the formula is: 

# ASDR = (1/100) * Σ(DeathRate_i * Population_Percentage_i)


# In[242]:


# Calculating Age Standardised Death Rates (ASDR)

COPD_uganda['ASDR'] = (COPD_uganda['Death rate, Uganda, 2019'] * COPD_uganda['WHO World Standard'])/100

COPD_usa['ASDR'] = (COPD_usa['Death rate, United States, 2019'] * COPD_uganda['WHO World Standard'])/100


# In[245]:


ASDR_uganda = COPD_uganda['ASDR'].sum()
ASDR_uganda = round(ASDR_uganda, 1)
ASDR_usa = COPD_usa['ASDR'].sum()
ASDR_usa = round(ASDR_usa, 1)


# In[247]:


print("ASDR Uganda per 100000:", ASDR_uganda)
print("ASDR USA per 100000:", ASDR_usa)

