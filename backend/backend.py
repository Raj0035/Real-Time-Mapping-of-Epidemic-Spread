import feedparser
import openai
import json
from flask import Flask, jsonify


# Initialize OpenAI client with your API key
from openai import OpenAI
client = OpenAI(api_key="API-KEY")

# Flask app initialization
app = Flask(__name__)

# Keywords to search for in RSS feeds
KEYWORDS = [
    "disease outbreak", "pandemic", "epidemic", "virus spread", "infectious disease",
    "public health crisis", "WHO alert", "health emergency", "disease cluster",
    "new cases reported", "quarantine", "localized outbreak", "spread of infection",
    "rising cases", "disease spread", "disease spread in India", "Indian health crisis",
    "India outbreak", "viral outbreak in India", "India epidemic report",
    "disease cases rise in India", "India virus alert", "infection surge India",
    "health emergency India", "India pandemic update"
]

# RSS feed URLs
RSS_FEEDS = [
    "https://news.google.com/rss/search?q=",
    "https://www.theguardian.com/society/health/rss",
    "https://medicalxpress.com/rss-feed/",
    "https://timesofindia.indiatimes.com/rss.cms",
    "https://www.ndtv.com/rss",
    "https://aninews.in/rss",
]

# 1. Fetch Articles from RSS Feeds
def fetch_rss_articles_by_keywords(feed_urls, keywords):
    articles = []
    for keyword in keywords:
        print(f"Searching for keyword: {keyword}")
        for url in feed_urls:
            if "google.com/rss" in url:
                search_url = f"{url}+{keyword.replace(' ', '+')}"
            else:
                search_url = url

            print(f"Fetching feed from: {search_url}")
            feed = feedparser.parse(search_url)

            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                link = entry.get("link", "")
                date = entry.get("published", "Unknown Date")

                # Append only if all fields are valid
                if all([title, summary, link, date]):
                    articles.append({
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "date": date
                    })
    print(f"Total articles fetched: {len(articles)}")
    return articles

# 2. Filter Relevant Articles Using GPT-3.5
def filter_relevant_articles(articles):
    relevant_articles = []
    for article in articles:
        print(f"Filtering article: {article['title']}")
        prompt = (
            f"You are a helpful assistant. Review the following news article and determine if it is about a recent disease outbreak.\n\n"
            f"Title: {article['title']}\n"
            f"Summary: {article['summary']}\n"
            f"Date: {article['date']}\n\n"
            f"Only respond with 'yes' if this article is relevant and provides sufficient information about the disease name, location, number affected, and incidence date; otherwise respond with 'no'."
        )
        response = client.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=100
        )
        if "yes" in response.choices[0].text.lower():
            relevant_articles.append(article)
    print(f"Total relevant articles: {len(relevant_articles)}")
    return relevant_articles

# 3. Extract Disease Data Using GPT with City Enforcement
def extract_disease_data(articles):
    structured_data = []
    for article in articles:
        print(f"Extracting data from article: {article['title']}")
        prompt = (
            """Extract the following structured information from the article. 
            If the location mentioned is only a country, provide the country's capital city instead as the location. Only provide valid entries with all fields:
            {
               "date":"Date of the Disease Incidence", 
               "summary": "A one line summary of the data",
               "disease": "The disease that is being spread", 
               "location": "The location of the disease spread",
               "species":"Humans/animals", 
               "severity":"A severity rating from 1-5 on the basis of what disease it is and how many are being affected"
            }
            Article: Title: {title}, Summary: {summary}, Date: {date}.
            If no valid data is found, return 'invalid'.
            """.format(
                title=article["title"],
                summary=article["summary"],
                date=article["date"]
            )
        )
        response = client.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150
        )
        try:
            extracted_data = json.loads(response.choices[0].text)
            if all(extracted_data.values()):  # Ensure all fields are valid
                structured_data.append(extracted_data)
        except Exception as e:
            print(f"Error parsing data: {e}")
            continue  # Skip invalid entries
    print(f"Total structured data entries: {len(structured_data)}")
    return structured_data

# Flask route to serve data
@app.route('/api/data', methods=['GET'])
def get_disease_outbreaks():
    print("Starting RSS feed processing...")
    articles = fetch_rss_articles_by_keywords(RSS_FEEDS, KEYWORDS)
    relevant_articles = filter_relevant_articles(articles)
    structured_data = extract_disease_data(relevant_articles)

    # Print the structured data before sending as response
    print("Structured Data:")
    print(json.dumps(structured_data, indent=4))

    # Return the structured data as JSON
    print("Returning structured data to client.")
    return jsonify(structured_data)

# Run Flask App
if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
