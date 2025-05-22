sources = [
    "https://www.foxnews.com/category/us/us-regions/southeast/florida",
    "https://www.local10.com/news/florida/",
    "https://www.tampabay.com/news/florida/",
    "https://www.miaminewtimes.com/news",
    "https://www.orlandoweekly.com/news",
    "https://thefloridastar.com/category/news/"
    # Add more Florida news sources
]

def scrape_stories():
    for source in sources:
        try:
            response = requests.get(source, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            site_selectors = {}

            if "miaminewtimes.com/news" in source:
                site_selectors = {
                    'article': 'div.section-story-package-story', # Placeholder
                    'title': 'div.story-headline > a',       # Placeholder
                    'link_is_article': False,                 # Link is usually within title_elem for this structure
                    'preview': 'div.story-dek'                # Placeholder
                }
                articles = soup.select(site_selectors['article'])
            elif "orlandoweekly.com/news" in source:
                site_selectors = {
                    'article': 'div.article-list-item',    # Placeholder
                    'title': 'a.story-title',              # Placeholder
                    'link_is_article': False,                # Link is usually within title_elem
                    'preview': 'div.story-lead'            # Placeholder
                }
                articles = soup.select(site_selectors['article'])
            elif "thefloridastar.com/category/news/" in source:
                site_selectors = {
                    'article': 'article.post',             # Placeholder
                    'title': 'h2.entry-title > a',       # Placeholder
                    'link_is_article': False,                # Link is usually within title_elem
                    'preview': 'div.entry-summary'         # Placeholder
                }
                articles = soup.select(site_selectors['article'])
            else:
                # Fallback to generic selectors
                articles = soup.select('article') or soup.select('.story') or soup.select('.news-item')
                site_selectors = { # Define for consistent access pattern later
                    'article': None, # Not used for selection here, but for structure
                    'title': 'h2, .title', # Combined for select_one
                    'link_is_article': False, # Default assumption
                    'preview': 'p, .summary' # Combined for select_one
                }


            for article_idx, article in enumerate(articles[:50]):
                title_elem = None
                link_elem = None # For specific link elements if not the article or title_elem
                preview_elem = None
                title = ""
                link = ""
                preview = ""

                try:
                    if "miaminewtimes.com/news" in source or \
                       "orlandoweekly.com/news" in source or \
                       "thefloridastar.com/category/news/" in source:
                        
                        title_elem = article.select_one(site_selectors['title'])
                        if title_elem:
                            title = title_elem.text.strip()
                            # Link is typically href of the title element for these structures
                            if title_elem.has_attr('href'):
                                link = title_elem['href']
                            else: # Check if parent is a link
                                parent_link = title_elem.find_parent('a')
                                if parent_link and parent_link.has_attr('href'):
                                    link = parent_link['href']
                        
                        preview_elem = article.select_one(site_selectors['preview'])
                        if preview_elem:
                            preview = preview_elem.text.strip()

                    else: # Fallback for original generic selectors
                        title_elem = article.select_one(site_selectors['title'])
                        if title_elem:
                            title = title_elem.text.strip()
                        
                        # Generic link finding:
                        # 1. Try a direct child <a> tag
                        # 2. Try if article itself is <a>
                        # 3. Try any <a> tag within article
                        link_tag = article.select_one('a') 
                        if link_tag and link_tag.has_attr('href'):
                            link = link_tag['href']
                        elif article.has_attr('href'): # If article element is the link
                            link = article['href']
                        else: # Last resort search anywhere inside
                            any_link_tag = article.find('a')
                            if any_link_tag and any_link_tag.has_attr('href'):
                                link = any_link_tag['href']
                            else:
                                print(f"No link found for article in {source} with title: {title if title else 'N/A'}")
                                continue
                        
                        preview_elem = article.select_one(site_selectors['preview'])
                        if preview_elem:
                            preview = preview_elem.text.strip()

                    if not title:
                        # print(f"No title found for an article in {source}, skipping.")
                        continue
                    
                    if not link:
                        # print(f"No link found for article in {source} with title: {title}, skipping.")
                        continue

                    # Make link absolute if it's relative
                    if link.startswith('//'): # Protocol relative URL
                        parsed_source_url = requests.utils.urlparse(source)
                        link = f"{parsed_source_url.scheme}:{link}"
                    elif link.startswith('/'):
                        parsed_source_url = requests.utils.urlparse(source)
                        base_url = f"{parsed_source_url.scheme}://{parsed_source_url.netloc}"
                        link = base_url + link
                    elif not link.startswith(('http://', 'https://')):
                        # Handle cases like 'www.example.com/story' or 'news/story.html'
                        parsed_source_url = requests.utils.urlparse(source)
                        base_url = f"{parsed_source_url.scheme}://{parsed_source_url.netloc}"
                        # Resolve relative path from the source URL's path
                        link = requests.compat.urljoin(source, link)


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
                except Exception as e_article:
                    print(f"Error processing article #{article_idx} from {source}: {e_article}. Title: '{title}', Link: '{link}'")
                    # continue to next article

        except requests.exceptions.RequestException as e_http:
            print(f"HTTP Error scraping {source}: {e_http}")
        except Exception as e_source:
            print(f"General Error scraping {source}: {e_source}")


    return stories
