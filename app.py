from flask import Flask, render_template, request
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask application
app = Flask(__name__)

# Load the saved models
tfidf = joblib.load('fitted_tfidf_vectorizer.pkl')  # Use the newly fitted vectorizer
cosine_sim = joblib.load('cosine_similarity_matrix.pkl')
df = joblib.load('movies_dataframe.pkl')

# Create a reverse map of indices and movie titles for easy lookup
indices = pd.Series(df.index, index=df['Film']).drop_duplicates()

# Function to recommend movies
def recommend_movies(title, min_rating=0, year=None, genre=None):
    # Check if movie exists in dataset
    if title not in indices:
        # If not found, calculate similarity for all movie titles
        title_list = df['Film'].tolist()
        title_vector = tfidf.transform([title])  # Transform user input

        # Compute cosine similarity of the input title with all movie titles
        similarity_scores = cosine_similarity(title_vector, tfidf.transform(df['Content'].fillna('')))
        similar_indices = similarity_scores[0].argsort()[-5:][::-1]  # Get indices of top 5 similar movies
        similar_movies = df['Film'].iloc[similar_indices].tolist()
        
        return similar_movies

    # If found, proceed with normal recommendation
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    df_filtered = df
    if year:
        df_filtered = df_filtered[df_filtered['Year'] == year]
    if genre:
        df_filtered = df_filtered[df_filtered['Genre'].str.contains(genre, case=False)]
    if min_rating:
        df_filtered = df_filtered[df_filtered['Audience score %'] >= min_rating]

    df_filtered = df_filtered.reset_index()
    sim_scores = [(i, sim) for i, sim in sim_scores if i in df_filtered.index]

    sim_scores = sim_scores[1:6]  # Exclude the input movie itself
    movie_indices = [i[0] for i in sim_scores]
    return df['Film'].iloc[movie_indices].tolist()

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form.get('title')
    genre = request.form.get('genre')
    year = request.form.get('year')
    min_rating = request.form.get('min_rating', 0)

    recommendations = recommend_movies(title, min_rating=int(min_rating), year=int(year) if year else None, genre=genre)
    
    return render_template('results.html', title=title, recommendations=recommendations)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
