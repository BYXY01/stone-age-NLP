from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os


class BaiduSearcherEdge:
    """
    使用系统自带的 Edge 浏览器的百度搜索器。
    启动更快，无需额外配置。
    """

    def __init__(self, headless=True):
        """
        初始化并启动 Edge 浏览器。
        :param headless: 是否使用无头模式（不显示浏览器窗口）
        """
        # --- 关键修改：使用 EdgeOptions ---
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')

        # Edge 的反检测选项
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Edge 的 User-Agent
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        )

        try:
            # --- 关键修改：使用 Edge ---
            # Selenium 4.6+ 会自动下载和管理 Edge 驱动
            self.driver = webdriver.Edge(options=options)

            # Edge 也支持 CDP 命令进行反检测
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    Object.defineProperty(navigator, 'plugins', { get: () => [ {0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"}, description: "Portable Document Format", filename: "internal-pdf-viewer", length: 1, name: "Chrome PDF Plugin"} ] });
                    Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en-US', 'en'] });
                    window.chrome = { runtime: {} };
                """
            })

            print("✅ Edge 浏览器已成功启动（系统自带，快速模式）。")
        except Exception as e:
            print(f"❌ Edge 浏览器启动失败: {e}")
            print("\n提示：请确保你的系统已安装 Microsoft Edge。")
            self.driver = None

    def search(self, keyword):
        """使用智能解析策略执行搜索，并自动去重"""
        if not self.driver:
            print("浏览器未初始化，无法搜索。")
            return []

        url = f"https://www.baidu.com/s?wd={keyword}"
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'content_left'))
            )

            search_results = []
            seen_links = set()

            result_elements = self.driver.find_elements(By.CSS_SELECTOR, '#content_left div:has(h3)')
            print(f"策略1（宽泛查找）找到 {len(result_elements)} 个潜在结果。")

            if not result_elements:
                result_elements = self.driver.find_elements(By.CSS_SELECTOR, '#content_left .result.c-container')
                print(f"策略2（精确查找）找到 {len(result_elements)} 个潜在结果。")

            for element in result_elements:
                try:
                    # 获取标题和链接
                    title_element = element.find_element(By.TAG_NAME, 'h3')
                    title = title_element.text.strip()

                    link = None
                    try:
                        link_element = title_element.find_element(By.TAG_NAME, 'a')
                        link = link_element.get_attribute('href')
                    except:
                        pass

                    if not link:
                        try:
                            link_element = element.find_element(By.CSS_SELECTOR, 'a[href]')
                            link = link_element.get_attribute('href')
                        except:
                            pass

                    if not link or link in seen_links:
                        continue

                    seen_links.add(link)

                    # --- 简化的摘要和来源提取 ---
                    # 获取整个元素的文本，并按行分割
                    all_text_lines = element.text.strip().split('\n')

                    # 移除标题行
                    if title in all_text_lines[0]:
                        all_text_lines = all_text_lines[1:]

                    # 最后一行作为来源
                    source = ""
                    if all_text_lines:
                        source = all_text_lines[-1].strip()
                        # 如果最后一行太长或包含链接，可能不是来源
                        if len(source) > 50 or 'http' in source:
                            source = ""
                        else:
                            # 移除最后一行，剩下的作为摘要
                            all_text_lines = all_text_lines[:-1]

                    # 剩下的行合并作为摘要
                    summary = ' '.join(all_text_lines).strip()

                    # 清理摘要中的一些无用信息
                    summary = summary.replace('详情', '').replace('更多', '').replace('>>', '').strip()

                    if title:
                        search_results.append({
                            'title': title,
                            'link': link,
                            'summary': summary,
                            'source': source
                        })
                except Exception:
                    continue

            print(f"去重后，成功解析出 {len(search_results)} 个唯一结果。")
            return search_results

        except TimeoutException:
            print("等待页面加载超时。")
            return []
        except Exception as e:
            print(f"搜索或解析过程中出错: {e}")
            return []

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("✅ Edge 浏览器已关闭。")


# --- 使用示例 ---
if __name__ == "__main__":
    # 1. 创建 Edge 搜索器实例
    searcher = BaiduSearcherEdge(headless=True)

    if searcher.driver:
        # 2. 执行搜索测试
        print("\n--- 搜索测试 ---")
        results = searcher.search(input())

        if results:
            print(f"\n成功获取到 {len(results)} 条唯一结果：\n")
            for i, res in enumerate(results, 1):
                print(f"--- 结果 {i} ---")
                print(f"标题: {res['title']}")
                print(f"链接: {res['link']}")
                print(f"摘要: {res['summary']}")
                if res['source']:
                    print(f"来源: {res['source']}")
                print()
        else:
            print("未能获取到搜索结果。")

        # 3. 关闭浏览器
        searcher.close()
    else:
        print("浏览器启动失败，无法进行搜索。")
