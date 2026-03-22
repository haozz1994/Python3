# -*- coding: utf-8 -*-
"""
豆瓣电影爬虫模块
负责爬取豆瓣Top250电影信息
"""

import re
import time
import random
import requests
from bs4 import BeautifulSoup
from models import Movie
from config import BASE_URL, HEADERS, PAGE_SIZE, TOTAL_PAGES, REQUEST_DELAY


class DoubanCrawler:
    """豆瓣电影爬虫类"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def crawl_all_movies(self):
        """
        爬取所有Top250电影
        
        Returns:
            list: Movie对象列表
        """
        all_movies = []

        for page in range(TOTAL_PAGES):
            start = page * PAGE_SIZE
            url = f"{BASE_URL}?start={start}"

            print(f"🔄 正在爬取第 {page + 1}/{TOTAL_PAGES} 页...")

            try:
                movies = self._crawl_page(url)
                all_movies.extend(movies)
                print(f"   ✅ 本页获取 {len(movies)} 部电影")

                # 添加随机延迟，避免请求过快被封
                if page < TOTAL_PAGES - 1:
                    delay = random.uniform(*REQUEST_DELAY)
                    time.sleep(delay)

            except Exception as e:
                print(f"   ❌ 爬取第 {page + 1} 页失败: {e}")

        print(f"\n✅ 爬取完成，共获取 {len(all_movies)} 部电影")
        return all_movies

    def _crawl_page(self, url):
        """
        爬取单页电影
        
        Args:
            url: 页面URL
            
        Returns:
            list: Movie对象列表
        """
        response = self.session.get(url, timeout=30)
        response.raise_for_status()

        # 让requests自动处理编码
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='item')

        movies = []
        for item in items:
            try:
                movie = self._parse_movie(item)
                if movie:
                    movies.append(movie)
            except Exception as e:
                print(f"   ⚠️ 解析电影信息失败: {e}")

        return movies

    def _parse_movie(self, item):
        """
        解析单个电影元素
        
        Args:
            item: BeautifulSoup元素对象
            
        Returns:
            Movie: 电影对象
        """
        movie = Movie()

        # 排名
        rank_em = item.find('em')
        movie.rank = int(rank_em.text) if rank_em else 0

        # 标题
        title_span = item.find('span', class_='title')
        movie.title = title_span.text if title_span else ""

        # 原名（如果有）
        title_spans = item.find_all('span', class_='title')
        if len(title_spans) > 1:
            original = title_spans[1].text.replace('/', '').strip()
            movie.original_title = original

        # 海报链接
        img = item.find('img')
        movie.poster_url = img.get('src') if img else ""

        # 其他信息（导演、主演、年份、国家、类型）
        info_p = item.find('div', class_='bd').find('p')
        if info_p:
            self._parse_movie_info(movie, info_p.get_text())

        # 评分
        rating_span = item.find('span', class_='rating_num')
        movie.rating = float(rating_span.text) if rating_span else 0.0

        # 评价人数
        star_div = item.find('div', class_='star')
        if star_div:
            spans = star_div.find_all('span')
            if len(spans) >= 4:
                rating_count_text = spans[3].text
                movie.rating_count = self._parse_rating_count(rating_count_text)

        # 经典台词
        quote_span = item.find('span', class_='inq')
        movie.quote = quote_span.text if quote_span else None

        return movie

    def _parse_movie_info(self, movie, info_text):
        """
        解析电影详细信息
        
        Args:
            movie: Movie对象
            info_text: 信息文本
        """
        lines = [line.strip() for line in info_text.split('\n') if line.strip()]

        if len(lines) >= 1:
            # 第一行：导演和主演
            self._parse_director_and_actors(movie, lines[0])

        if len(lines) >= 2:
            # 第二行：年份、国家、类型
            self._parse_year_country_genre(movie, lines[1])

    def _parse_director_and_actors(self, movie, text):
        """
        解析导演和主演
        
        Args:
            movie: Movie对象
            text: 文本内容
        """
        # 移除 "导演:" 前缀
        text = text.replace('导演:', '').strip()

        # 分割导演和主演
        if '主演:' in text:
            parts = text.split('主演:', 1)
            movie.director = parts[0].strip()
            movie.actors = parts[1].strip()
        else:
            movie.director = text
            movie.actors = None

    def _parse_year_country_genre(self, movie, text):
        """
        解析年份、国家、类型
        
        Args:
            movie: Movie对象
            text: 文本内容
        """
        # 分割字段
        parts = [p.strip() for p in text.split('/')]

        if len(parts) >= 1:
            movie.year = parts[0]
        if len(parts) >= 2:
            movie.country = parts[1]
        if len(parts) >= 3:
            movie.genre = parts[2]

    def _parse_rating_count(self, text):
        """
        解析评价人数
        
        Args:
            text: 文本内容，如 "1234567人评价"
            
        Returns:
            int: 评价人数
        """
        match = re.search(r'(\d+)', text)
        return int(match.group(1)) if match else 0
