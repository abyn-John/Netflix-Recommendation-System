# utils/similarity.py
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_resource
def build_similarity_matrix(data, feature_column='combined_features'):
    cv = CountVectorizer(stop_words='english')
    count_matrix = cv.fit_transform(data[feature_column])
    similarity_matrix = cosine_similarity(count_matrix)
    return cv, count_matrix, similarity_matrix
