import feedparser
import json
import time # Added
from datetime import datetime

rss_sources = [
    {"name": "Fox News", "url": "https://moxie.foxnews.com/google-publisher/us.xml", "original_url": "https://www.foxnews.com/category/us/us-regions/southeast/florida"},
    {"name": "Local10", "url": "https://www.local10.com/arc/outboundfeeds/rss/category/news/?outputType=xml&size=20", "original_url": "https://www.local10.com/news/florida/"},
    {"name": "Miami New Times", "url": "https://www.miaminewtimes.com/miami/Rss.xml?oid=6202154", "original_url": "https://www.miaminewtimes.com/news"},
    {"name": "Orlando Weekly", "url": "https://www.orlandoweekly.com/orlando/Rss.xml?oid=2240408", "original_url": "https://www.orlandoweekly.com/news"},
    {"name": "The Florida Star", "url": "https://www.thefloridastar.com/category/news/feed/", "original_url": "https://thefloridastar.com/category/news/"},
    # Tampa Bay Times is excluded as no RSS feed was found.
    # New sources added:
    {"name": "Metro Weekly", "url": "https://www.metroweekly.com/feed/", "original_url": "https://www.metroweekly.com/"},
    {"name": "ClickOrlando", "url": "https://www.clickorlando.com/arc/outboundfeeds/rss/category/news/?outputType=xml&size=50", "original_url": "https://www.clickorlando.com/"},
    {"name": "Yahoo News", "url": "https://news.yahoo.com/rss", "original_url": "https://www.yahoo.com/news/"},
    {"name": "WFTV", "url": "https://www.wftv.com/feed/", "original_url": "https://www.wftv.com/"},
    {"name": "NBC Miami", "url": "https://www.nbcmiami.com/?rss=y", "original_url": "https://www.nbcmiami.com/"}
]


def is_florida_man_story(title, text):
    keywords = [
        "florida man", "florida woman"
    ]
    title_lower = title.lower()
    text_lower = text.lower()
    return any(keyword in title_lower or keyword in text_lower for keyword in keywords)


def scrape_stories():
    stories = []
    max_stories_per_feed = 200 # As per previous logic for HTML scraping iteration limit
    target_total_stories = 10

    for source_info in rss_sources:
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

                title = entry.title if hasattr(entry, 'title') else ""
                link = entry.link if hasattr(entry, 'link') else ""
                
                preview = ""
                if hasattr(entry, 'summary'):
                    preview = entry.summary
                elif hasattr(entry, 'description'):
                    preview = entry.description

                # Date parsing
                parsed_date_struct = entry.get('published_parsed') or entry.get('updated_parsed')
                story_date_iso = datetime.now().isoformat() # Default to now
                if parsed_date_struct:
                    try:
                        story_date_iso = datetime.fromtimestamp(time.mktime(parsed_date_struct)).isoformat()
                    except Exception as e_date:
                        print(f"Could not parse date for entry '{title}' from {source_info['name']}: {e_date}. Using current time.")
                
                if not title or not link:
                    continue

                if is_florida_man_story(title, preview):
                    # Truncate preview to 4 lines
                    lines = preview.split('\n')
                    if len(lines) > 4:
                        truncated_preview = '\n'.join(lines[:4])
                    else:
                        truncated_preview = preview

                    story = {
                        'title': title,
                        'link': link,
                        'preview': truncated_preview,
                        'source': source_info['original_url'], # Use original website URL
                        'date': story_date_iso,
                        'location': extract_florida_location(title + " " + preview)
                    }
                    stories.append(story)
                    print(f"Added Florida Man story: {title}")
            
        except Exception as e:
            print(f"Error processing feed for {source_info['name']} ({source_info['url']}): {e}")

    # Sort stories by date and truncate if necessary
    initial_story_count = len(stories)
    stories.sort(key=lambda x: datetime.fromisoformat(x['date']), reverse=True)
    
    if initial_story_count > target_total_stories:
        stories = stories[:target_total_stories]
        print(f"Found {initial_story_count} stories, keeping the newest {target_total_stories}.")
    
    return stories


def extract_florida_location(text):
    florida_locations = [
        "Miami", "Orlando", "Tampa", "Jacksonville", "Gainesville", 
        "St. Petersburg", "Tallahassee", "Fort Lauderdale", "Sarasota", 
        "Pensacola", "Key West", "Palm Beach", "Broward County", "Miami-Dade County"
    ]
    text_lower = text.lower()
    for location in florida_locations:
        if location.lower() in text_lower:
            return location
    return "Florida"

if __name__ == "__main__":
    stories = scrape_stories()
    output = {
        'last_updated': datetime.now().isoformat(),
        'stories': stories
    }
    with open('florida_man_stories.json', 'w') as f:
        json.dump(output, f, indent=2)
    print("Scraping complete. Output saved to florida_man_stories.json")
