import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# List of Florida news sources to check
sources = [
    "https://www.foxnews.com/category/us/us-regions/southeast/florida",
    "https://www.local10.com/news/florida/",
    "https://www.tampabay.com/news/florida/"
    # Add more Florida news sources
]

def is_florida_man_story(title, text):
    keywords = ["florida man", "florida woman", "florida resident", "florida person"]
    title_lower = title.lower()
    text_lower = text.lower()
    
    return any(keyword in title_lower or keyword in text_lower for keyword in keywords)

stories = []

for source in sources:
    try:
        response = requests.get(source, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract articles (customize selectors based on each site)
        articles = soup.select('article') or soup.select('.story') or soup.select('.news-item')
        
        for article in articles[:10]:  # Limit to first 10 articles per source
            title_elem = article.select_one('h2') or article.select_one('.title')
            if not title_elem:
                continue
                
            title = title_elem.text.strip()
            link = article.select_one('a')['href']
            
            # Make link absolute if it's relative
            if link.startswith('/'):
                link = source.split('/')[0] + '//' + source.split('/')[2] + link
            
            # Get article preview
            preview_elem = article.select_one('p') or article.select_one('.summary')
            preview = preview_elem.text.strip() if preview_elem else ""
            
            # Check if it's a Florida Man story
            if is_florida_man_story(title, preview):
                stories.append({
                    'title': title,
                    'link': link,
                    'preview': preview,
                    'source': source,
                    'date': datetime.now().isoformat(),
                    'location': extract_florida_location(title + " " + preview)
                })
    except Exception as e:
        print(f"Error scraping {source}: {e}")

# Add location extraction function
def extract_florida_location(text):
    florida_cities = ["miami", "orlando", "tampa", "jacksonville", "tallahassee", "gainesville"]
    text_lower = text.lower()
    
    for city in florida_cities:
        if city in text_lower:
            return city.capitalize()
    
    return "Florida"  # Default if no specific city found

# Save to JSON file
with open('florida_man_stories.json', 'w') as f:
    json.dump({'last_updated': datetime.now().isoformat(), 'stories': stories}, f, indent=2)
