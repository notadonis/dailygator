import feedparser

rss_sources = [
    {"name": "Fox News", "url": "https://moxie.foxnews.com/google-publisher/us.xml", "original_url": "https://www.foxnews.com/category/us/us-regions/southeast/florida"},
    {"name": "Local10", "url": "https://www.local10.com/arc/outboundfeeds/rss/category/news/?outputType=xml&size=20", "original_url": "https://www.local10.com/news/florida/"},
    {"name": "Miami New Times", "url": "https://www.miaminewtimes.com/miami/Rss.xml?oid=6202154", "original_url": "https://www.miaminewtimes.com/news"},
    {"name": "Orlando Weekly", "url": "https://www.orlandoweekly.com/orlando/Rss.xml?oid=2240408", "original_url": "https://www.orlandoweekly.com/news"},
    {"name": "The Florida Star", "url": "https://www.thefloridastar.com/category/news/feed/", "original_url": "https://thefloridastar.com/category/news/"}
]

if __name__ == "__main__":
    for source_info in rss_sources:
        print(f"Processing feed: {source_info['name']} - {source_info['url']}")
        try:
            feed = feedparser.parse(source_info['url'])

            if feed.bozo:
                print(f"  Warning: Feed may be malformed. Bozo bit set with exception: {feed.bozo_exception}")
                # Decide if to continue or skip based on severity, for now, we'll try to process entries
            
            if feed.entries:
                print(f"  Successfully parsed. Found {len(feed.entries)} entries.")
                for i, entry in enumerate(feed.entries[:3]): # Iterate through the first 3 entries
                    title = entry.title if hasattr(entry, 'title') else "No title"
                    summary = entry.summary if hasattr(entry, 'summary') else (entry.description if hasattr(entry, 'description') else "No summary/description")
                    
                    print(f"  --- Entry {i+1} ---")
                    print(f"  Title: {title}")
                    print(f"  Summary: {summary}")
            else:
                print(f"  No entries found for this feed.")

        except Exception as e:
            print(f"  Error parsing feed {source_info['name']}: {e}")
        
        print("=====================================")
