# -*- coding: utf-8 -*-
"""
@author: marina 
"""

import pandas as pd

file_in = "../input_dataset/Global Peace Index 2023.csv"
peace_index_df = pd.read_csv(file_in)

file_in = "../input_dataset/whr_200522.csv"
happiness_df = pd.read_csv(file_in)

file_in = "../input_dataset/continents2.csv"
continent_df = pd.read_csv(file_in)

file_in = "../input_dataset/world_wide_self_harm_and_substance_deaths.csv"
selfharm_subs_abuse_df = pd.read_csv(file_in)

######################################################
# Perform a selection from 2020 in the peace_index_df and happiness_df 
# to then merge with selfharm_substance_abuse_df.
peace_index_df_filtered = peace_index_df[(peace_index_df['year'] <= 2020) &
                                         (peace_index_df['year'] >= 2019)].copy()

happiness_df_filtered = happiness_df[(happiness_df['year'] <= 2020) &
                                     (happiness_df['year'] >= 2019)].copy()

######################################################
## Initial merge of peace_index_df and happiness_df
peace_index_df_filtered.rename(columns={'iso3c': 'ISO_Code',
                                        'year': 'Year'}, 
                               inplace=True)

happiness_df_filtered.rename(columns={'Iso alpha': 'ISO_Code',
                                      'year': 'Year'}, 
                          inplace=True)

df_peace_happiness = pd.merge(peace_index_df_filtered, happiness_df_filtered,
                              on=['ISO_Code', 'Year'])

# Remove the duplicated column with the country name.
df_peace_happiness.drop('Country', axis=1, inplace=True)

######################################################
# Selection from 2019 to 2020 in selfharm_substance_abuse_df and filter for the self-harm causes
selfharm_subs_abuse_df_filtered = selfharm_subs_abuse_df[(selfharm_subs_abuse_df['Year'] <= 2020) &
                                                         (selfharm_subs_abuse_df['Year'] >= 2019)].copy() 

selfharm_df_filtered = selfharm_subs_abuse_df_filtered.loc[selfharm_subs_abuse_df_filtered['Cause'] == 'Intentional self-harm']

######################################################
## Combine selfharm_subs_abuse_df_filtered with continent_df to include hierarchical variables.

continent_df.rename(columns={'alpha-3': 'ISO_Code'}, inplace=True)
continent_df =  continent_df.loc[:, ['ISO_Code', 'region', 'sub-region']]

selfharm_df_filtered = pd.merge(selfharm_df_filtered, continent_df, on=['ISO_Code'])

######################################################
# Remove rows that do not provide relevant information for the analysis.
exclude_values = ['All', 'Unspecified']
selfharm_df_filtered = selfharm_df_filtered[~selfharm_df_filtered['Sex'].isin(exclude_values)]

exclude_values = ['Unknown', '0', '1', '2', '4', '1-4', '85+']
selfharm_df_filtered = selfharm_df_filtered[~selfharm_df_filtered['Age_Range'].isin(exclude_values)]

                       
######################################################
## Merge of selfharm_df_filtered and df_peace_happiness
df_peace_happiness_selfharm = pd.merge(selfharm_df_filtered, 
                                                  df_peace_happiness,
                                                  on=['ISO_Code', 'Year'])

df_peace_happiness_selfharm.drop('Country name', axis=1, inplace=True)

######################################################
## Save final dataframe
df_peace_happiness_selfharm.to_csv("../output_dataset/self_harm_deaths_with_happiness_and_peace_indexs_2019_2020.csv")
