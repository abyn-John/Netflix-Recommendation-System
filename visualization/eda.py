from data_cleaning import net_dataset
# import pandas as pd
# import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt

# To know the split between Movies and TV Shows.
print(net_dataset['type'].value_counts())  # Movies vs TV Shows

# graph of Moveis vs TV Shows
movie_TV = net_dataset['type'].value_counts()
sns.barplot(x=movie_TV.index,y=movie_TV.values)

print(net_dataset['rating'].value_counts())  # e.g., TV-MA, PG, etc.To understand content ratings

# vectorized approach of getting the longest movie
# Step 1: Filter only movies
movies_df = net_dataset[net_dataset['type'] == 'Movie'].copy()

# Step 2: Extract number from 'duration' using regex
movies_df['duration_mins'] = movies_df['duration'].str.extract(r'(\d+)').astype(float)

# Step 3: Find the movie with the longest duration
longest_movie = movies_df[movies_df['duration_mins'] == movies_df['duration_mins'].max()]


# shortest movie 
movie_list = net_dataset[net_dataset['type'] == 'Movie'].copy()
movie_list['duration_mins'] = movie_list['duration'].str.extract(r'(\d+)').astype(float)
movie_list[movie_list['duration_mins'] == movie_list['duration_mins'].min()]


# Longest TV Show
tv_list = net_dataset[net_dataset['type'] == 'TV Show'].copy()
tv_list['show_duration'] = tv_list['duration'].str.extract(r'(\d)').astype(float)
tv_list[tv_list['show_duration'] == tv_list['show_duration'].max()]


# Shortest TV Show
tv_list = net_dataset[net_dataset['type'] == 'TV Show'].copy()
tv_list['show_duration'] = tv_list['duration'].str.extract(r'(\d)').astype(float)
tv_list[tv_list['show_duration'] == tv_list['show_duration'].min()]


# Bar chart of movies (rating wise)
movie_rating_wise = net_dataset[net_dataset['type'] == 'Movie']['rating'].value_counts()
sns.barplot( y=movie_rating_wise.index, x=movie_rating_wise.values)

# Bar chart of TV Show (rating wise)
movie_rating_wise = net_dataset[net_dataset['type'] == 'TV Show']['rating'].value_counts()
sns.barplot( y=movie_rating_wise.index, x=movie_rating_wise.values)


#  bar chart for movie (country wise)
movie_con_wise = net_dataset[net_dataset['type'] == 'Movie'].copy()
movie_con_wise['country'] = movie_con_wise['country'].str.split(',')
movie = movie_con_wise.explode('country')
movie['country'] = movie['country'].str.strip()

# Drop rows where country is 'Unknown'
movie = movie[movie['country'] != 'Unknown']

movie_country_wise = movie['country'].value_counts()

movie_country_wise

plt.figure(figsize=(12,6))
movie_country_wise.head(10).plot(kind='bar')
plt.title('Top 10 Countries Producing Movies')
plt.ylabel('Number of Movies')
plt.xlabel('Country')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Country wise TV Show
tv_show = net_dataset[net_dataset['type'] == 'TV Show'].copy()
tv_show['country'] = tv_show['country'].str.split(',')
tv_show = tv_show.explode('country')
tv_show['country'] = tv_show['country'].str.strip()
tv_show = tv_show[tv_show['country'] != 'Unknown']
tv_con = tv_show['country'].value_counts()

plt.figure(figsize=(12,6))
tv_con.head(10).plot(kind='bar')
plt.title('Top 10 TV Show Producing Movies')
plt.ylabel('Number of Movies')
plt.xlabel('Country')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


