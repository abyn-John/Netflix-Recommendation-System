from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_cleaning import net_dataset

# Vectorize the combined column for recommendation system
cv = CountVectorizer(stop_words='english')
count_matrix = cv.fit_transform(net_dataset['combined_features'])
# dense_matrix = count_matrix.todense()
# print(dense_matrix[:3, :3])

# similarity score 
similarity_matrix = cosine_similarity(count_matrix)

# Recommendation system
def recommendation_system(user_input):
    value = net_dataset[net_dataset['title'].str.lower() == user_input.lower()]
    if value.empty:
        genre = input('Enter the genre of the film:').lower()
        user_matrix = cv.transform([genre])
        comparision_similarities = cosine_similarity(user_matrix, count_matrix)
        comparision_similarities = list(enumerate(comparision_similarities[0]))
        comparision_result = sorted(comparision_similarities, key=lambda x:x[1], reverse=True)[:5]
        print(f"We do not have '{user_input}' but you might like:")
        for i , k in comparision_result:
            print(net_dataset.iloc[i]['title'])
        return
    try:
        index = value.index[0]
        similarities = list(enumerate(similarity_matrix[index]))
        result = sorted(similarities,key=lambda x:x[1] ,reverse=True)[1:6]
        print('Similar Movies to Explore:')
        for i,k in result:
            print(net_dataset.iloc[i]['title'])
    except (ValueError, TypeError) as e:
        print("Error while finding recommendations:", str(e))
        
# txt = input('Enter a Movie Name')
# recommendation_system(txt) 