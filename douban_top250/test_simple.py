# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

url = "https://movie.douban.com/top250?start=0"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print(f"请求: {url}")
resp = requests.get(url, headers=headers, timeout=30)
print(f"状态码: {resp.status_code}")
print(f"编码: {resp.encoding}")
print(f"内容长度: {len(resp.text)}")

# 尝试不同编码
for enc in ['utf-8', 'gbk', 'gb2312', resp.encoding]:
    try:
        text = resp.content.decode(enc)
        print(f"\n使用 {enc} 解码成功")
        if '肖申克' in text or '豆瓣' in text:
            print(f"✅ 找到中文内容！")
            soup = BeautifulSoup(text, 'html.parser')
            items = soup.find_all('div', class_='item')
            print(f"找到 {len(items)} 个电影")
            if items:
                title = items[0].find('span', class_='title')
                print(f"第一部电影: {title.text if title else '无标题'}")
            break
    except Exception as e:
        print(f"{enc} 解码失败: {e}")
