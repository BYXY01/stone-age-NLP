"""Google search via Chrome browser (Selenium version)."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class GoogleSearcherChrome:
    """
    Google searcher using the Chrome browser.
    Selenium 4.6+ automatically downloads and manages the ChromeDriver.
    """

    def __init__(self, headless=True):
        """
        Initialize and start Chrome.
        :param headless: whether to run in headless mode (no browser window)
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')

        # Anti-detection options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Chrome User-Agent
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        try:
            self.driver = webdriver.Chrome(options=options)

            # CDP commands for anti-detection.
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                    window.chrome = { runtime: {} };
                """
            })

            print("✅ Chrome browser started successfully (headless mode).")
        except Exception as e:
            print(f"❌ Failed to start Chrome: {e}")
            print("\nHint: make sure Chrome/Chromium is installed on your system.")
            self.driver = None

    def search(self, keyword):
        """Run a search with a smart parsing strategy and deduplicate results."""
        if not self.driver:
            print("Browser not initialized, cannot search.")
            return []

        url = f"https://www.google.com/search?q={keyword}"
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#search, #rso'))
            )

            search_results = []
            seen_links = set()

            result_elements = self.driver.find_elements(By.CSS_SELECTOR, '#search div.g, #rso div.g')
            print(f"Strategy 1 (broad search) found {len(result_elements)} potential results.")

            if not result_elements:
                result_elements = self.driver.find_elements(By.CSS_SELECTOR, '#search div[data-hveid], #rso div[data-hveid]')
                print(f"Strategy 2 (exact search) found {len(result_elements)} potential results.")

            for element in result_elements:
                try:
                    # Get title and link
                    title_element = element.find_element(By.TAG_NAME, 'h3')
                    title = title_element.text.strip()

                    link = None
                    try:
                        link_element = title_element.find_element(By.XPATH, './ancestor::a | ./a')
                        link = link_element.get_attribute('href')
                    except Exception:
                        pass

                    if not link:
                        try:
                            link_element = element.find_element(By.CSS_SELECTOR, 'a[href^="http"]')
                            link = link_element.get_attribute('href')
                        except Exception:
                            pass

                    if not link or link in seen_links:
                        continue

                    seen_links.add(link)

                    # Simplified summary extraction.
                    summary = ""
                    try:
                        snippet = element.find_element(By.CSS_SELECTOR, '.VwiC3b, .aCOpRe')
                        summary = snippet.text.strip()
                    except Exception:
                        pass

                    if not summary:
                        all_text_lines = element.text.strip().split('\n')
                        if all_text_lines and title in all_text_lines[0]:
                            all_text_lines = all_text_lines[1:]
                        summary = ' '.join(all_text_lines).strip()[:200]

                    if title:
                        search_results.append({
                            'title': title,
                            'link': link,
                            'summary': summary
                        })
                except Exception:
                    continue

            print(f"After deduplication, parsed {len(search_results)} unique results.")
            return search_results

        except TimeoutException:
            print("Timed out waiting for the page to load.")
            return []
        except Exception as e:
            print(f"Error during search or parsing: {e}")
            return []

    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            print("✅ Chrome browser closed.")


# --- Usage example ---
if __name__ == "__main__":
    # 1. Create the Chrome searcher instance.
    searcher = GoogleSearcherChrome(headless=True)

    if searcher.driver:
        # 2. Run a search test.
        print("\n--- Search test ---")
        results = searcher.search(input())

        if results:
            print(f"\nSuccessfully fetched {len(results)} unique results:\n")
            for i, res in enumerate(results, 1):
                print(f"--- Result {i} ---")
                print(f"Title: {res['title']}")
                print(f"Link: {res['link']}")
                print(f"Summary: {res['summary']}")
                print()
        else:
            print("Could not fetch any search results.")

        # 3. Close the browser.
        searcher.close()
    else:
        print("Browser failed to start, cannot search.")
