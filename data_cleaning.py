import pandas as pd
import streamlit as st

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("data/netflix_titles.csv")

    # Clean the null values
    df['director'] = df['director'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df['date_added'] = df['date_added'].fillna('Unknown')
    df['duration'] = df['duration'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('NR')

    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    # Combine features for similarity matching
    df['combined_features'] = (df['listed_in'] + ' ' + df['description']).str.lower()

    return df

net_dataset = load_and_clean_data()








# import pandas as pd
# # import numpy as np

# net_dataset = pd.read_csv("data/netflix_titles.csv")
# net_dataset

# # Information about the dataset
# net_dataset.info()

# # Shape of the dataset
# net_dataset.shape

# # check for null values 
# net_dataset.isnull().sum()

# # clean the null values
# # cleaning the dataset to make sure no null values remain 
# net_dataset['director'] = net_dataset['director'].fillna('Unknown')
# net_dataset['country'] = net_dataset['country'].fillna('Unknown')
# net_dataset['date_added'] = net_dataset['date_added'].fillna('Unknown')
# net_dataset['duration'] = net_dataset['duration'].fillna('Unknown')
# net_dataset['rating'] = net_dataset['rating'].fillna('NR')

# # Data types (To understand the structure of your dataset)
# print(net_dataset.dtypes)

# # convert date_added from object to datetime64
# net_dataset['date_added'] = pd.to_datetime(net_dataset['date_added'], errors='coerce')
# net_dataset['date_added']

# net_dataset['combined_features'] = (net_dataset['listed_in'] + ' ' + net_dataset['description']).str.lower()



