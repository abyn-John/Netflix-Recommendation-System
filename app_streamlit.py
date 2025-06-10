import streamlit as st
from data_cleaning import net_dataset
from utils.similarity import build_similarity_matrix
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
from genre_all import extract_valid_genres, is_valid_genre_input, VALID_GENRES

# Prepare similarity matrix
cv, count_matrix, similarity_matrix = build_similarity_matrix(net_dataset)

def get_recommendations(title,num_recs=6):
    title = title.lower()
    movie_titles = net_dataset['title'].tolist()
    title_map = {t.lower(): t for t in movie_titles}
        # Get best match with score threshold
    best_match = None
    best_score = 0
    for t in title_map:
        score = SequenceMatcher(None, title, t).ratio()
        if score > best_score:
            best_score = score
            best_match = t

    if best_score < 0.8:  # you can tweak this threshold
        return None, None, None
    
    match_title = title_map[best_match]
    index = net_dataset[net_dataset['title'] == match_title].index[0]
    similarity_scores = list(enumerate(similarity_matrix[index]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:num_recs+1]
    recommendations = [net_dataset.iloc[i]['title'] for i, _ in sorted_scores]
    type1 = [net_dataset.iloc[i]['type'] for i, _ in sorted_scores]
    return match_title, recommendations, type1

def get_genre_recommendations(genre, num_recs=5):
    user_matrix = cv.transform([genre])
    similarities = cosine_similarity(user_matrix, count_matrix)
    scores = list(enumerate(similarities[0]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:num_recs]
    recommendations = [net_dataset.iloc[i]['title'] for i, _ in sorted_scores]
    type1 = [net_dataset.iloc[i]['type'] for i, _ in sorted_scores]
    return recommendations, type1


def main():
    st.title("🎬 Netflix Movie Recommender")

    # Initialize state
    if 'movie_not_found' not in st.session_state:
        st.session_state.movie_not_found = False

    # Inputs
    user_input = st.text_input("Enter a Movie Name", key="movie_input")

    num_recs = st.slider("Number of recommendations:", 1, 25, 5)

    # If movie not found, show genre input with dropdown
    genre_input = None
    if st.session_state.movie_not_found:
        col1, col2 = st.columns([2, 2])
        with col1:
            genre_input = st.text_input("Movie not found. Enter a Genre (e.g., Comedy, Drama):", key="genre_input")
        with col2:
            dropdown_genre = st.selectbox("Or pick a genre:", sorted(list(VALID_GENRES)))
            if dropdown_genre and dropdown_genre.lower() not in genre_input.lower():
                genre_input += f", {dropdown_genre}"

    if st.button("Recommend"):
        if st.session_state.movie_not_found and genre_input:
            if not is_valid_genre_input(genre_input):
                st.warning("Please enter valid genres without numbers or special symbols.")
            else:
                valid_genres = extract_valid_genres(genre_input)
                if not valid_genres:
                    st.warning("No valid genres found. Please enter valid genre(s).")
                else:
                    genre_str = ', '.join(valid_genres)
                    genre_recs, type1 = get_genre_recommendations(genre_str, num_recs)
                    st.subheader(f"Top {num_recs} recommendations for: {genre_str.title()}")
                    for rec_title, rec_type in zip(genre_recs, type1):
                        st.write("🎯", rec_title, f"({rec_type})")
                    # st.session_state.movie_not_found = False

        elif user_input:
            match_title, recommendations, type1 = get_recommendations(user_input,num_recs)
            if recommendations:
                st.subheader(f"Because you watched: {match_title}")
                for rec_title, rec_type in zip(recommendations, type1):
                        st.write("✅", rec_title, f"({rec_type})")
                st.session_state.movie_not_found = False
            else:
                st.session_state.movie_not_found = True
                st.rerun()

if __name__ == "__main__":
    main()
