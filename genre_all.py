import re
from difflib import SequenceMatcher

# Set of valid genres (case-insensitive)
VALID_GENRES = {
    "","hindi", "english", "international", "independent",
    "comedies", "action", "romance", "dramas", "thriller", "horror", "sci-fi", "crime", "fantasy",
    "bollywood", "hollywood","children" ,"family", "sports", "award-winning", "documentaries",
    "shorts", "stand-up comedy", "anime"
}

def is_valid_genre_input(genre_input):
    # Check if genre_input contains any digits (reject if yes)
    if re.search(r'\d', genre_input):
        return False
    # Check if genre_input contains any invalid characters besides letters, spaces, commas, hyphens
    if re.search(r'[^a-zA-Z\s,-]', genre_input):
        return False
    return True


def extract_valid_genres(raw_input):
    raw_input = raw_input.lower()

    # Normalize: turn hyphens/spaces into commas
    raw_input = re.sub(r'\s+|(?<=\w)-(?=\w)', ',', raw_input)

    user_genres = [g.strip() for g in raw_input.split(',') if g.strip()]
    valid_matches = []

    for user_genre in user_genres:
        best_score = 0
        best_match = None
        for valid in VALID_GENRES:
            score = SequenceMatcher(None, user_genre, valid).ratio()
            if score > best_score:
                best_score = score
                best_match = valid
        if best_score >= 0.6:  # You can tune this
            valid_matches.append(best_match)

    return list(set(valid_matches))  # Remove duplicates