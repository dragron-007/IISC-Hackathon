import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup
import requests
from googlesearch import search
from collections import Counter
from heapq import nlargest

def search_for_articles(query, num_articles=4):
    try:
        search_results = search(query, num=num_articles, stop=num_articles)
        return search_results
    except Exception as e:
        print(f"Error occurred during article search: {e}")
        return []

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
        print(f"Error occurred while fetching article text from {url}: {e}")
        return ''

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
        print(f"Error occurred while summarizing article: {e}")
        return ''

def get_keywords(article_text, num_keywords=5):
    try:
        words = word_tokenize(article_text.lower())
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word not in stop_words]
        word_freq = Counter(filtered_words)
        keywords = nlargest(num_keywords, word_freq, key=word_freq.get)
        return keywords
    except Exception as e:
        print(f"Error occurred while extracting keywords: {e}")
        return []

def suggest_articles(articles, current_text, num_suggestions=4):
    try:
        current_keywords = get_keywords(current_text)
        suggested_articles = []
        for article in articles:
            article_text = get_article_text(article)
            article_keywords = get_keywords(article_text)
            similarity_score = len(set(current_keywords) & set(article_keywords))
            suggested_articles.append((article, similarity_score))
        suggested_articles.sort(key=lambda x: x[1], reverse=True)
        return [article[0] for article in suggested_articles[:num_suggestions]]
    except Exception as e:
        print(f"Error occurred while suggesting articles: {e}")
        return []

def main():
    try:
        nltk.download('punkt')
        nltk.download('stopwords')

        query = input("Enter the topic to search for: ")
        articles = search_for_articles(query)
        if articles:
            summary = ''
            article_links = []
            for article in articles:
                article_text = get_article_text(article)
                if article_text:
                    summary += summarize_article(article_text) + '\n'
                    article_links.append(article)
            if summary:
                print("Summarized Article:\n", summary)
                print("Links to articles used:")
                for link in article_links:
                    print(link)
                print("Suggested Articles:")
                suggested_articles = suggest_articles(articles, summary)
                for suggested_article in suggested_articles:
                    print(suggested_article)
            else:
                print("No relevant articles found.")
        else:
            print("No relevant articles found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
