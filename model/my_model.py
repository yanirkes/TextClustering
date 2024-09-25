import random
import numpy as np

import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import string
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class claimsModel:
    def __init__(self, df_):
        """
        Initialize the claimsModel class with the input DataFrame.
        - Preprocess text data and store in 'processed_text' column.
        - Initialize the TF-IDF vectorizer and Kmeans model.
        """
        self.df_ = df_
        self.df_['processed_text'] = self.df_['text'].apply(self.preprocess_text)
        self.tf_model = TfidfVectorizer()
        self.X, self.cosine_similarities = self.vectorize_x()  # Vectorize the preprocessed text
        self.kmeans_model = None  # Build Kmeans model and assign clusters

    @staticmethod
    def preprocess_text(text):
        """
        Preprocess the input text:
        - Convert to lowercase, remove punctuation, and stopwords.
        - Return the processed text as a single string.
        """
        stop_words = set(stopwords.words('english'))
        stop_words.update(['claim', 'claims', 'claims1', 'first', 'second'])  # Custom stopwords

        # Remove punctuation and convert to lowercase
        punctuation_table = str.maketrans('', '', string.punctuation)
        text = text.lower().translate(punctuation_table)

        # Tokenize and filter out stopwords
        words = word_tokenize(text)
        words = [word for word in words if word not in stop_words]

        return ' '.join(words)  # Return the cleaned text

    def vectorize_x(self):
        """
        Vectorize the processed text data using TF-IDF.
        Returns the transformed document-term matrix.
        """
        X = self.tf_model.fit_transform(self.df_['processed_text'])
        cosine_similarities = cosine_similarity(X)

        return X, cosine_similarities

    def extract_top_keywords_per_cluster(self, num_keywords=2):
        """
        Extract top keywords for each cluster based on TF-IDF scores.
        - Ignores the noise cluster (-1).
        - Returns a dictionary mapping each cluster to its top keywords.
        """
        cluster_keywords = {}
        clusters = self.df_['topic'].values  # Cluster labels from Kmeans

        for cluster_num in np.unique(clusters):
            if cluster_num == -1:
                continue  # Ignore noise points

            # Get documents belonging to the current cluster
            cluster_docs = self.X[clusters == cluster_num]

            # Compute the mean TF-IDF score for each term in the cluster
            mean_tfidf = cluster_docs.mean(axis=0).A1
            top_indices = mean_tfidf.argsort()[-num_keywords:][::-1]  # Get indices of top keywords

            # Extract the top keywords for the cluster
            top_keywords = [self.tf_model.get_feature_names_out()[i] for i in top_indices]
            cluster_keywords[cluster_num] = ' '.join(top_keywords)

        return cluster_keywords

    def build_model(self, k):
        """
        Build and fit the Kmeans model.
        - Assign cluster labels to the 'topic' column in the DataFrame.
        - Extract top keywords for each cluster and store them in 'topic'.
        Returns the fitted Kmeans model.
        """
        kmeans_model = KMeans(n_clusters=k, random_state=42)
        kmeans_model.fit(self.cosine_similarities)
        clusters = kmeans_model.predict(self.cosine_similarities)
        self.df_['topic'] = clusters  # Store cluster labels

        # Extract keywords and assign them to the 'topic' column
        cluster_keywords = self.extract_top_keywords_per_cluster(num_keywords=3)
        cluster_keywords[-1] = 'others'  # Assign 'others' to noise points
        self.df_['topic'] = list(map(lambda x: cluster_keywords[x], self.df_['topic']))

        return kmeans_model

    def predict(self, x):
        """
        Predict random topics from the list of unique topics in the DataFrame.
        - Used for generating predictions for new data points.
        Returns a list of random topic predictions.
        """
        unique_topics = self.df_['topic'].unique().tolist()

        # Helper function to predict a random topic
        def predict_():
            ind = random.randint(0, len(unique_topics) - 1)
            return unique_topics[ind]

        return [predict_() for _ in x]  # Generate predictions for each input item
