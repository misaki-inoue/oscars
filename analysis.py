# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 16:12:16 2023

@author: misak
"""
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as stats
import cpi
import seaborn as sns 

os.chdir("C:\\Users\\misak\Desktop\myproject\oscar")

movies = pd.read_csv("movies.csv")
oscars = pd.read_csv("the_oscar_award.csv")

#### Which director/actor/actress has received the most number of nominees?

def find_top(category, top_n):
    cat = oscars[oscars["category"]==category]
    top_cat = cat.groupby(['name'])['name'].count().reset_index(name='awards') \
        .sort_values(by="awards", ascending=False).head(top_n)
    return top_cat

oscars[oscars['category']=="ACTOR"]['year_ceremony'].max()
oscars[oscars['category']=="ACTOR IN A LEADING ROLE"]['year_ceremony'].min()

top_actors_lead = find_top("ACTOR IN A LEADING ROLE",5) # IN A LEADING ROLE started from 1977
top_actress_lead = find_top("ACTRESS IN A LEADING ROLE",5)
top_actors = find_top("ACTOR", 5)
top_actress = find_top("ACTRESS",5)

top_actors_all = pd.concat([top_actors, top_actors_lead]) \
    .sort_values('awards', ascending=False).reset_index(drop=True)
top_actress_all = pd.concat([top_actress, top_actress_lead]) \
    .sort_values('awards', ascending=False).reset_index(drop=True)
    
top_directors = find_top("DIRECTING",5).reset_index(drop=True)

#### Gantt chart with top 3 director, actor, actress

top3_actors = top_actors_all.iloc[:5,:].copy()
top3_actors["type"] = "Best Actor"
top3_actress = top_actress_all.iloc[:4,:].copy()
top3_actress["type"] = "Best Actress"
top3_directors = top_directors.iloc[:4,:].copy()
top3_directors["type"] = "Best Director"

top = pd.concat([top3_actors, top3_actress, top3_directors])

def first_nominated(row):
    name = row['name']
    matching_row = oscars[oscars['name'] == name]
    if not matching_row.empty:
        ceremony_year = matching_row['year_ceremony'].values[0]
        return ceremony_year
    else:
        return None

top['first'] = top.apply(first_nominated, axis=1)

def last_nominated(row):
    name = row['name']
    oscars_reversed = oscars[::-1]
    matching_row = oscars_reversed[oscars_reversed['name'] == name]
    if not matching_row.empty:
        ceremony_year = matching_row['year_ceremony'].values[0]
        return ceremony_year
    else:
        return None

top['last'] = top.apply(last_nominated, axis=1)

top['duration'] = top['last'] - top['first'] + 1
top['from_start'] = top['first'] - 1928


type_colors = {'Best Director': 'c', 'Best Actress': 'y', 'Best Actor': 'm'}
patches = []
for i in type_colors:
    patches.append(matplotlib.patches.Patch(color=type_colors[i]))

fig, ax = plt.subplots()
for index, row in top.iterrows():
    plt.barh(y=row['name'], width=row['duration'], left=row['first'] , color=type_colors[row['type']])
plt.gca().invert_yaxis()
plt.title('Time between first and last Oscar nomination')
ax.legend(handles=patches, labels=type_colors.keys(), fontsize=11)
plt.show()

#### What genre is most popular in each of the "big five" category? (stacked bar chart)

oscars_short = oscars[(oscars['year_film'] >= 1980) & (oscars['year_film'] <= 2019)]

oscars_merged = pd.merge(oscars_short, movies, 
                         left_on=oscars_short["film"].str.lower(),
                         right_on=movies["name"].str.lower(),
                         how="left",
                         suffixes=('','_film')) #this method ignores cases during merge but does not modify original dataframes

cols_to_drop = ['key_0', 'name_film', 'year', 'star', 'writer']
oscars_merged = oscars_merged.drop(cols_to_drop, axis=1)

oscars_merged['main_category'] = oscars_merged['category'].str.replace(r'\s*\([^)]*\)$', '', regex=True)

big_five = ['ACTOR IN A LEADING ROLE', 'ACTRESS IN A LEADING ROLE', 'BEST PICTURE',
            'DIRECTING', 'WRITING']

oscars_bigfive = oscars_merged[oscars_merged['main_category'].isin(big_five)]

bigfive_genre = oscars_bigfive.groupby(['main_category','genre'])['genre'].count().unstack()


ax = bigfive_genre.plot.bar(stacked=True)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Genre')
ax.set_xlabel('Award Categories')
ax.set_title("Number of Nominated Movies by Categories and Genre")
plt.show()


#### Correlation between IMDb score and likelihood of winning?

oscars_score = oscars_merged.dropna(subset=['rating']) # 3513 out of 4718

win_score = oscars_score[oscars_score['winner']==True]['score']
lose_score = oscars_score[oscars_score['winner']==False]['score']

print(stats.mannwhitneyu(win_score,lose_score))
 # mann-whitney test for unequal size

#### Correlation between gross revenue and likelihood of winning?
oscars_merged_g = oscars_merged.dropna(subset=['gross']) 
oscars_revenue = oscars_merged_g[['year_ceremony','winner','gross']]

oscars_revenue['adjusted'] = oscars_revenue.apply(
    lambda x: cpi.inflate(x.gross, x.year_ceremony), axis=1
    )

win_revenue = oscars_revenue[oscars_revenue['winner']==True]['adjusted']
lose_revenue = oscars_revenue[oscars_revenue['winner']==False]['adjusted']

print(stats.mannwhitneyu(win_revenue,lose_revenue))

#### Box plots for the two correlation

score = oscars_score[['winner','score']]
revenue = oscars_revenue[['winner','adjusted']]
revenue['adjusted'] = revenue['adjusted'] / 1e9

fig, axes = plt.subplots(1, 2, figsize=(9,5))

sns.boxplot(data=score, x='winner', y='score', ax=axes[0])
axes[0].set_title('IMDb Score of Nominees and Winners')
axes[0].set_xlabel('Awarded')
axes[0].set_ylabel('IMDb Score')

sns.boxplot(data=revenue, x='winner', y='adjusted', ax=axes[1])
axes[1].set_title('Adjusted Gross Revenue of \n Nominees and Winners')
axes[1].set_xlabel('Awarded')
axes[1].set_ylabel('Adjusted Gross Revenue (Billion$)')
axes[1].ticklabel_format(axis='y', useOffset=False)
