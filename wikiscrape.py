import wikipedia
import json
import os
import time
from tqdm import tqdm


TOPICS = {
    "health": [
        "disease", "mental health", "epidemic", "cardiology",
        "public health", "medical conditions", "infectious diseases",
        "WHO health statistics", "healthcare", "nutrition and health",
        "disease outbreaks", "health science", "epidemiology", 
        "global health", "medical treatments", "human body health"
    ],

    "environment": [
        "global warming", "climate change", "endangered species",
        "deforestation", "pollution", "biodiversity", "ecosystems",
        "environmental protection", "greenhouse gases", 
        "sustainability", "environmental science",
        "ocean life", "wildlife conservation", "air quality"
    ],

    "technology": [
        "AI", "robotics", "software", "internet",
        "machine learning", "computer science", 
        "quantum computing", "electronics", "mobile technology",
        "information technology", "cybersecurity", 
        "digital transformation", "web development",
        "technology innovations", "cloud computing"
    ],

    "economy": [
        "stock market", "inflation", "crypto",
        "job markets", "macroeconomics", "microeconomics",
        "economic indicators", "financial crisis", 
        "international trade", "global economy",
        "economic policy", "banking industry", 
        "labor markets", "GDP statistics", "fiscal policy"
    ],

    "entertainment": [
        "music industry", "movies", "celebrity",
        "streaming platforms", "television shows", 
        "pop culture", "film industry", 
        "video games", "animation", "comedy",
        "Hollywood", "Bollywood", "media production",
        "entertainment awards", "performing arts"
    ],

    "sports": [
        "cricket", "football", "tennis", "olympics",
        "basketball", "athletics", "sports analytics",
        "sports teams", "sports tournaments", 
        "athletes", "FIFA", "NBA", "NFL",
        "sports history", "sports championships"
    ],

    "politics": [
        "elections", "public policy", "UN",
        "international relations", "government systems",
        "political science", "democracy", 
        "foreign policy", "political parties", 
        "global politics", "public administration",
        "diplomacy", "geopolitics", "political theory"
    ],

    "education": [
        "literacy rates", "online education", "student loans",
        "higher education", "schools and universities", 
        "academic research", "learning methods",
        "education policy", "teaching strategies",
        "curriculum development", "educational psychology",
        "global education", "student performance",
        "STEM education", "distance learning"
    ],

    "travel": [
        "tourist destinations", "airline industry", "travel trends",
        "world tourism", "travel safety", "airports",
        "travel guides", "backpacking", 
        "world heritage sites", "hospitality industry",
        "tour packages", "international tourism",
        "travel planning", "aviation", "vacation spots"
    ],

    "food": [
        "food security", "crop yield", "nutrition",
        "global hunger", "agriculture", 
        "food science", "dietary habits",
        "food production", "organic farming",
        "crops and harvest", "food supply chain",
        "malnutrition", "global food system",
        "healthy diet", "food preservation","food industry","food technology",
        "food standards","nutrition science","agricultural products"
    ]
}

MIN_DOCS = 5000
MIN_SUMMARY_LEN = 200
MAX_SHORT_DOC_PERCENT = 5  # <5% short summaries

os.makedirs("wiki_docs", exist_ok=True)


def scrape_topic(topic, queries):
    documents = {}
    attempted_titles = set()  

    print(f"\n------------------------------")
    print(f"Scraping topic: {topic}")
    print(f"------------------------------\n")

    for query in queries:
        print(f"Searching for: {query}")
       
        search_results = wikipedia.search(query, results=500)

        for title in tqdm(search_results):
            if title in attempted_titles:
                continue
            attempted_titles.add(title)

            if len(documents) >= MIN_DOCS:
                break

            try:
                page = wikipedia.page(title, auto_suggest=False)
                summary = page.summary
                content = page.content
                url = page.url

                
                if len(summary) < MIN_SUMMARY_LEN:
                    continue

                
                documents[title] = {
                    "title": title,
                    "summary": summary,
                    "content": content,
                    "url": url
                }

            except Exception:
                continue

        if len(documents) >= MIN_DOCS:
            break
    if len(documents) < MIN_DOCS:
        print(f"\n Not enough docs for {topic}. Expanding search automatically...")

        extra_results = wikipedia.search(topic, results=2000)

        for title in tqdm(extra_results):
            if len(documents) >= MIN_DOCS:
                break

            if title in attempted_titles:
                continue

            attempted_titles.add(title)

            try:
                page = wikipedia.page(title, auto_suggest=False)
                summary = page.summary
                content = page.content
                url = page.url

                if len(summary) < MIN_SUMMARY_LEN:
                    continue

                documents[title] = {
                    "title": title,
                    "summary": summary,
                    "content": content,
                    "url": url
                }

            except:
                continue

    total_docs = len(documents)
    short_docs = sum(1 for d in documents.values() if len(d["summary"]) < MIN_SUMMARY_LEN)

    short_percent = (short_docs / total_docs) * 100 if total_docs > 0 else 0

    print(f"\n Topic: {topic}")
    print(f"✔ Total documents collected: {total_docs}")
    print(f"✔ Short documents (<200 chars): {short_docs} ({short_percent:.2f}%)")

    if short_percent > MAX_SHORT_DOC_PERCENT:
        print(f" ERROR: Too many short documents! Regenerate recommended.")
    else:
        print(f" Passed size quality check")

    with open(f"wiki_docs/{topic}.json", "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2)

    print(f"\n Saved {total_docs} documents to wiki_docs/{topic}.json\n")


if _name_ == "_main_":
    for topic, query_list in TOPICS.items():
        scrape_topic(topic, query_list)
        time.sleep(2)