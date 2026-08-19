"""Google search scraper (requests + BeautifulSoup version)."""

import requests
from bs4 import BeautifulSoup
import urllib.parse


def get_google_search_smart(keyword):
    """
    Fetch Google search results using a heuristic approach that does not rely
    on a specific CSS class.

    :param keyword: search keyword
    :return: list of dicts with 'title', 'link' and 'summary'
    """
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://www.google.com/search?q={encoded_keyword}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        search_results = []

        # Step 1: locate the main result container.
        main_content = soup.find('div', id='search') or soup.find('div', id='rso')
        if not main_content:
            print("Main search container (#search / #rso) not found; the page structure may have changed.")
            return []

        # Step 2: find all divs that contain an <h3> tag (likely search results).
        potential_results = main_content.find_all('div', recursive=False)
        actual_results = []
        for div in potential_results:
            if div.find('h3'):
                actual_results.append(div)

        print(f"Found {len(actual_results)} potential results via heuristic analysis.")

        # Step 3: extract info from each result unit.
        for item in actual_results:
            title_tag = item.find('h3')
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)

            # The link is usually inside the first <a> tag in the h3.
            link_tag = title_tag.find('a')
            link = link_tag.get('href') if link_tag else None

            # The snippet is usually in a div with a muted-text style class.
            summary_tag = item.find('div', class_='VwiC3b')
            if not summary_tag:
                summary_tag = item.find('span', class_='aCOpRe')

            summary = ""
            if summary_tag:
                summary = summary_tag.get_text(strip=True)
            else:
                # Fallback: any text besides the title (rough but better than nothing).
                all_text = item.get_text(strip=True, separator=' ')
                summary = all_text.replace(title, '').strip()[:200]

            if title and link:
                search_results.append({
                    'title': title,
                    'link': link,
                    'summary': summary
                })

        return search_results

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Parsing error: {e}")
        return None


# --- Usage example ---
if __name__ == "__main__":
    search_keyword = input()
    results = get_google_search_smart(search_keyword)

    if results:
        print(f"Successfully fetched {len(results)} results about '{search_keyword}':\n")
        for i, res in enumerate(results, 1):
            print(f"--- Result {i} ---")
            print(f"Title: {res['title']}")
            print(f"Link: {res['link']}")
            print(f"Summary: {res['summary']}\n")
    else:
        print("Could not fetch any search results.")
