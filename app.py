import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup
import requests
from googlesearch import search
from collections import Counter
from heapq import nlargest
from sklearn.feature_extraction.text import TfidfVectorizer

# Function to search for articles based on user query
def search_for_articles(query, num_articles=4):
    try:
        search_results = search(query, num=num_articles, stop=num_articles)
        return search_results
    except Exception as e:
        st.error(f"Error occurred during article search: {e}")
        return []

# Function to fetch the text content of an article given its URL
def get_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ''
        for paragraph in paragraphs:
            article_text += paragraph.get_text()
        return article_text
    except Exception as e:
        st.error(f"Error occurred while fetching article text from {url}: {e}")
        return ''

# Function to summarize an article
def summarize_article(article_text, target_length=150):
    try:
        sentences = sent_tokenize(article_text)
        words = word_tokenize(article_text.lower())
        stop_words = set(stopwords.words('english'))
        word_freq = {}
        for word in words:
            if word not in stop_words:
                if word not in word_freq:
                    word_freq[word] = 1
                else:
                    word_freq[word] += 1

        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    if len(sentence.split(' ')) < 30:
                        if sentence not in sentence_scores:
                            sentence_scores[sentence] = word_freq[word]
                        else:
                            sentence_scores[sentence] += word_freq[word]

        summarized_sentences = []
        summary_length = 0
        for sentence in sentences:
            if summary_length + len(sentence.split()) <= target_length:
                summarized_sentences.append(sentence)
                summary_length += len(sentence.split())
            else:
                break

        summarized_article = ' '.join(summarized_sentences)
        return summarized_article
    except Exception as e:
        st.error(f"Error occurred while summarizing article: {e}")
        return ''

# Function to get keywords from an article
def get_keywords(article_text, num_keywords=5):
    try:
        words = word_tokenize(article_text.lower())
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word not in stop_words]
        word_freq = Counter(filtered_words)
        keywords = nlargest(num_keywords, word_freq, key=word_freq.get)
        return keywords
    except Exception as e:
        st.error(f"Error occurred while extracting keywords: {e}")
        return []

# Function to suggest related articles based on the current article's keywords
def suggest_articles(articles, current_text, num_suggestions=3):
    try:
        current_keywords = set(get_keywords(current_text))

        suggested_articles = []
        for article in articles:
            article_text = get_article_text(article)
            if not article_text:
                st.warning(f"Empty text for article: {article}")
                continue

            article_keywords = set(get_keywords(article_text))
            similarity_score = len(current_keywords.intersection(article_keywords))
            suggested_articles.append((article, similarity_score))

        suggested_articles.sort(key=lambda x: x[1], reverse=True)

        # Display only the titles of suggested articles
        return [article[0].split(" - ")[0] for article in suggested_articles[:num_suggestions]]
    except Exception as e:
        st.error(f"Error occurred while suggesting articles: {e}")
        return []

# Function to display results in an enhanced UI
def display_results(summary, article_links, suggested_articles):
    st.subheader("Summarized Article")
    st.markdown(summary, unsafe_allow_html=True)

    st.subheader("Links to Articles Used")
    for link in article_links:
        st.write(link)

    st.subheader("Suggested Articles")
    if suggested_articles:
        for suggested_article in suggested_articles:
            st.write(suggested_article)
    else:
        st.warning("No suggested articles found.")

# Main function for the Streamlit application
def main():
    try:
        nltk.download('punkt')
        nltk.download('stopwords')

        st.title("Article Summarizer")
        st.markdown(
            "Welcome to the Article Summarizer! Enter a topic of interest, and we'll find relevant articles, summarize them, and suggest related content."
        )

        # User input for topic search
        query = st.text_input("Enter the topic to search for:")

        # Slider for adjusting summarization length
        summarization_length = st.slider(
            "Select Summarization Length", min_value=50, max_value=500, value=150, step=10
        )

        # Button to trigger the search and summarization process
        if st.button("Search"):
            articles = search_for_articles(query)
            if articles:
                summary = ''
                article_links = []
                for article in articles:
                    article_text = get_article_text(article)
                    if article_text:
                        summary += summarize_article(article_text, target_length=summarization_length) + '\n'
                        article_links.append(article)

                if summary:
                    suggested_articles = suggest_articles(articles, summary)
                    display_results(summary, article_links, suggested_articles)
                else:
                    st.warning("No relevant articles found.")
            else:
                st.warning("No relevant articles found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
