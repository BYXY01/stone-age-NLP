import requests
from bs4 import BeautifulSoup
import urllib.parse


def get_baidu_search_smart(keyword):
    """
    使用更智能的启发式方法获取百度搜索结果，降低对特定class的依赖。

    :param keyword: 搜索关键词
    :return: 包含标题、链接、摘要的字典列表
    """
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://www.baidu.com/s?wd={encoded_keyword}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        search_results = []

        # 步骤1：定位主容器。这个ID相对稳定。
        main_content = soup.find('div', id='content_left')
        if not main_content:
            print("未找到主内容容器 #content_left，页面结构可能已大变。")
            return []

        # 步骤2：寻找所有包含 <h3> 标签的 div，这很可能是搜索结果
        # 使用 lambda 函数进行更灵活的查找
        potential_results = main_content.find_all('div', recursive=False)
        actual_results = []
        for div in potential_results:
            if div.find('h3'):
                actual_results.append(div)

        print(f"通过智能分析找到 {len(actual_results)} 个潜在结果。")

        # 步骤3：从每个结果单元中提取信息
        for item in actual_results:
            title_tag = item.find('h3')
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)

            # 链接通常在 h3 内的第一个 a 标签里
            link_tag = title_tag.find('a')
            link = link_tag.get('href') if link_tag else None

            # 摘要的class名变化多端，我们尝试多种可能
            summary_tag = (item.find('div', class_='c-abstract') or
                           item.find('div', class_='c-span-last') or
                           item.find('span', class_='content-right_8Zs40'))

            summary = ""
            if summary_tag:
                summary = summary_tag.get_text(strip=True)
            else:
                # 如果都找不到，尝试获取标题之外的文本（这很粗糙，但聊胜于无）
                all_text = item.get_text(strip=True, separator=' ')
                summary = all_text.replace(title, '').strip()[:200]  # 限制长度

            if title and link:
                search_results.append({
                    'title': title,
                    'link': link,
                    'summary': summary
                })

        return search_results

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None
    except Exception as e:
        print(f"解析出错: {e}")
        return None


# --- 使用示例 ---
if __name__ == "__main__":
    search_keyword = input()
    results = get_baidu_search_smart(search_keyword)

    if results:
        print(f"成功获取到关于 '{search_keyword}' 的 {len(results)} 条结果：\n")
        for i, res in enumerate(results, 1):
            print(f"--- 结果 {i} ---")
            print(f"标题: {res['title']}")
            print(f"链接: {res['link']}")
            print(f"摘要: {res['summary']}\n")
    else:
        print("未能获取到搜索结果。")
