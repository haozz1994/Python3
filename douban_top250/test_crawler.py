# -*- coding: utf-8 -*-
"""
测试爬虫，检查豆瓣页面结构
"""

import requests
from bs4 import BeautifulSoup
from config import BASE_URL, HEADERS

def test_page():
    """测试获取页面内容"""
    url = f"{BASE_URL}?start=0"
    
    print(f"正在请求: {url}")
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        response = session.get(url, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(response.content)} 字节")
        
        # 使用二进制内容手动解码
        html_content = response.content.decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 检查标题
        title = soup.find('title')
        print(f"页面标题: {title.text if title else '无标题'}")
        
        # 检查是否有电影元素
        items = soup.find_all('div', class_='item')
        print(f"找到 {len(items)} 个 div.item 元素")
        
        # 如果没有，检查其他可能的选择器
        if not items:
            items_li = soup.find_all('li', class_='item')
            print(f"找到 {len(items_li)} 个 li.item 元素")
            
            # 检查页面中所有的 class 包含 item 的元素
            all_items = soup.find_all(class_='item')
            print(f"找到 {len(all_items)} 个 class='item' 的元素")
        
        # 如果找到了，打印第一个的结构
        if items:
            print("\n第一个电影元素的HTML结构:")
            print(items[0].prettify()[:1000])
            
            # 检查关键元素
            item = items[0]
            print("\n关键元素检查:")
            print(f"  - em (排名): {item.find('em')}")
            print(f"  - span.title (标题): {item.find('span', class_='title')}")
            print(f"  - div.bd: {item.find('div', class_='bd')}")
            print(f"  - span.rating_num (评分): {item.find('span', class_='rating_num')}")
        
        # 保存完整页面用于分析
        with open('test_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("\n✅ 页面已保存到 test_page.html")
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == '__main__':
    test_page()
