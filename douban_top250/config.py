# -*- coding: utf-8 -*-
"""
配置文件
包含数据库连接和爬虫配置
"""

# ========== MySQL 数据库配置（请修改为你的配置）==========
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"           # 修改为你的MySQL用户名
MYSQL_PASSWORD = "123456"     # 修改为你的MySQL密码
MYSQL_DATABASE = "douban"     # 数据库名

# 数据库连接URL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

# ========== 爬虫配置 ==========
# 豆瓣电影Top250基础URL
BASE_URL = "https://movie.douban.com/top250"

# 请求头（模拟浏览器访问）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# 每页电影数量
PAGE_SIZE = 25

# 总页数（Top250共10页）
TOTAL_PAGES = 10

# 请求间隔（秒），避免请求过快被封
REQUEST_DELAY = (2, 4)  # 随机延迟2-4秒
