import feedparser
import json
import time # Added
from datetime import datetime

# Removed old 'requests' and 'BeautifulSoup' imports as they are no longer needed for core functionality
# import requests
# from bs4 import BeautifulSoup
# import os # Not strictly necessary anymore unless other file operations are added

# RSS Feed URLs
FOX_NEWS_RSS = "https://moxie.foxnews.com/google-publisher/us.xml"
LOCAL10_RSS = "https://www.local10.com/arc/outboundfeeds/rss/category/news/?outputType=xml&size=20"
MIAMI_NEW_TIMES_RSS = "https://www.miaminewtimes.com/miami/Rss.xml?oid=6202154"
ORLANDO_WEEKLY_RSS = "https://www.orlandoweekly.com/orlando/Rss.xml?oid=2240408"
FLORIDA_STAR_RSS = "https://www.thefloridastar.com/category/news/feed/"

rss_sources = [
    {"name": "Fox News", "url": FOX_NEWS_RSS, "original_url": "https://www.foxnews.com/category/us/us-regions/southeast/florida"},
    {"name": "Local10", "url": LOCAL10_RSS, "original_url": "https://www.local10.com/news/florida/"},
    {"name": "Miami New Times", "url": MIAMI_NEW_TIMES_RSS, "original_url": "https://www.miaminewtimes.com/news"},
    {"name": "Orlando Weekly", "url": ORLANDO_WEEKLY_RSS, "original_url": "https://www.orlandoweekly.com/news"},
    {"name": "The Florida Star", "url": FLORIDA_STAR_RSS, "original_url": "https://thefloridastar.com/category/news/"}
    # Tampa Bay Times is excluded as no RSS feed was found.
]

# Old sources list commented out
# sources = [
#     "https://www.foxnews.com/category/us/us-regions/southeast/florida",
#     "https://www.local10.com/news/florida/",
#     "https://www.tampabay.com/news/florida/",
#     "https://www.miaminewtimes.com/news",
#     "https://www.orlandoweekly.com/news",
#     "https://thefloridastar.com/category/news/"
#     # Add more Florida news sources
# ]


def is_florida_man_story(title, text):
    keywords = [
        "florida man", "florida woman", "florida resident", "florida person", 
        "a florida", "gainesville", "jacksonville", "miami", "orlando", "tampa", 
        "arrested in florida", "florida sheriff", "bizarre florida", "strange florida"
    ]
    title_lower = title.lower()
    text_lower = text.lower()
    return any(keyword in title_lower or keyword in text_lower for keyword in keywords)


def scrape_stories():
    stories = []
    max_stories_per_feed = 50 # As per previous logic for HTML scraping iteration limit
    target_total_stories = 10

    for source_info in rss_sources:
        if len(stories) >= target_total_stories:
            print(f"Reached target of {target_total_stories} stories. Stopping.")
            break

        print(f"Fetching stories from {source_info['name']} ({source_info['url']})...")
        try:
            feed = feedparser.parse(source_info['url'])

            if feed.bozo:
                print(f"Warning: Feed for {source_info['name']} may be malformed. Bozo bit set with exception: {feed.bozo_exception}")

            if not feed.entries:
                print(f"No entries found for {source_info['name']}.")
                continue

            entries_logged_count = 0 # Initialize for each new feed

            for entry_idx, entry in enumerate(feed.entries):
                if entry_idx >= max_stories_per_feed:
                    print(f"Processed {max_stories_per_feed} entries for {source_info['name']}, moving to next source.")
                    break
                
                if len(stories) >= target_total_stories:
                    break # Break from entries loop if target met

                title = entry.title if hasattr(entry, 'title') else ""
                link = entry.link if hasattr(entry, 'link') else ""
                
                preview = ""
                if hasattr(entry, 'summary'):
                    preview = entry.summary
                elif hasattr(entry, 'description'):
                    preview = entry.description

                # Debug logging for the first 3 entries - REMOVED/COMMENTED OUT
                # if entries_logged_count < 3:
                #     print(f"DEBUG: Feed: {source_info['name']}")
                #     print(f"DEBUG: Entry Title: {title}") # title var already populated
                #     print(f"DEBUG: Entry Summary/Description: {preview if preview else 'No summary/description'}") # preview var already populated
                #     print("---") # Separator
                #     entries_logged_count += 1
                
                # Date parsing
                parsed_date_struct = entry.get('published_parsed') or entry.get('updated_parsed')
                story_date_iso = datetime.now().isoformat() # Default to now
                if parsed_date_struct:
                    try:
                        story_date_iso = datetime.fromtimestamp(time.mktime(parsed_date_struct)).isoformat()
                    except Exception as e_date:
                        print(f"Could not parse date for entry '{title}' from {source_info['name']}: {e_date}. Using current time.")
                
                if not title or not link:
                    # print(f"Skipping entry from {source_info['name']} due to missing title or link.")
                    continue

                if is_florida_man_story(title, preview):
                    story = {
                        'title': title,
                        'link': link,
                        'preview': preview,
                        'source': source_info['original_url'], # Use original website URL
                        'date': story_date_iso,
                        'location': extract_florida_location(title + " " + preview)
                    }
                    stories.append(story)
                    print(f"Added Florida Man story: {title}")
                    if len(stories) >= target_total_stories:
                        print(f"Reached target of {target_total_stories} stories. Stopping.")
                        break 
            
        except Exception as e:
            print(f"Error processing feed for {source_info['name']} ({source_info['url']}): {e}")

    return stories

# Add location extraction function
def extract_florida_location(text):
    florida_cities = ["miami", "orlando", "tampa", "jacksonville", "tallahassee", "gainesville"]
    text_lower = text.lower()

    for city in florida_cities:
        if city in text_lower:
            return city.capitalize()

    return "Florida"  # Default if no specific city found

def main():
    stories = scrape_stories()
    with open('florida_man_stories.json', 'w') as f:
        json.dump({'last_updated': datetime.now().isoformat(), 'stories': stories}, f, indent=2)


if __name__ == "__main__":
    main()
