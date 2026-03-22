# douban_top250 - 豆瓣电影Top250爬虫

## 项目概述

基于 Python 的豆瓣电影 Top250 爬虫程序，使用 requests + BeautifulSoup 爬取电影信息，通过 SQLAlchemy ORM 保存到本地 MySQL 数据库。

**技术栈**: Python 3.x | requests | BeautifulSoup4 | SQLAlchemy | MySQL

---

## 功能特性

- **完整数据爬取**: 自动爬取豆瓣电影 Top250 全部数据（10页，250部电影）
- **智能防封**: 随机 2-4 秒请求延迟，模拟浏览器 User-Agent
- **数据持久化**: 使用 SQLAlchemy ORM 保存到 MySQL，支持增量更新
- **交互式菜单**: 命令行交互界面，支持数据查询、筛选、统计
- **多维度筛选**: 支持按电影类型、年份筛选查询

---

## 项目结构

```
douban_top250/
├── requirements.txt    # 依赖包列表
├── config.py         # 配置文件（数据库、爬虫设置）
├── models.py         # 数据模型（Movie实体类）
├── crawler.py        # 爬虫模块
├── database.py       # 数据库操作模块
├── main.py           # 主程序入口
└── repowiki.md       # 项目文档
```

---

## 模块说明

### config.py - 配置模块

集中管理数据库连接和爬虫配置参数。

**主要配置项**:
- `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_USER` / `MYSQL_PASSWORD` / `MYSQL_DATABASE` - MySQL 连接配置
- `BASE_URL` - 豆瓣 Top250 基础 URL
- `HEADERS` - HTTP 请求头（模拟浏览器）
- `PAGE_SIZE` / `TOTAL_PAGES` - 分页参数
- `REQUEST_DELAY` - 请求间隔（随机 2-4 秒）

### models.py - 数据模型

使用 SQLAlchemy 定义 Movie 实体类，自动映射到 MySQL 表结构。

**Movie 字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| rank | Integer | 排名（唯一） |
| title | String(255) | 电影名称 |
| original_title | String(255) | 原名 |
| director | String(255) | 导演 |
| actors | Text | 主演 |
| year | String(20) | 年份 |
| country | String(100) | 国家/地区 |
| genre | String(100) | 类型 |
| rating | Float | 评分 |
| rating_count | BigInteger | 评价人数 |
| quote | Text | 经典台词 |
| poster_url | String(500) | 海报链接 |

### crawler.py - 爬虫模块

`DoubanCrawler` 类负责爬取豆瓣电影数据。

**核心方法**:
- `crawl_all_movies()` - 爬取全部 250 部电影
- `_crawl_page(url)` - 爬取单页数据
- `_parse_movie(item)` - 解析单个电影元素
- `_parse_movie_info()` / `_parse_director_and_actors()` / `_parse_year_country_genre()` - 信息解析

### database.py - 数据库操作

`MovieRepository` 类封装数据库 CRUD 操作，支持上下文管理器。

**核心方法**:
- `save_movies(movies)` - 批量保存/更新电影
- `get_all_movies()` - 获取所有电影
- `get_movie_by_rank(rank)` - 按排名查询
- `get_movie_count()` - 获取总数
- `get_top_rated(limit)` - 获取评分最高电影
- `get_movies_by_year(year)` - 按年份筛选
- `get_movies_by_genre(genre)` - 按类型筛选
- `delete_all_movies()` - 删除所有数据

### main.py - 主程序入口

提供交互式命令行菜单，整合爬虫和数据库操作。

**菜单功能**:
1. 爬取电影数据并保存到数据库
2. 查看所有电影
3. 查看电影统计
4. 按类型筛选电影
5. 按年份筛选电影
6. 删除所有数据
0. 退出

---

## 快速开始

### 1. 安装依赖

```bash
cd douban_top250
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `config.py`，修改 MySQL 连接配置：

```python
MYSQL_USER = "root"           # 你的MySQL用户名
MYSQL_PASSWORD = "123456"     # 你的MySQL密码
MYSQL_DATABASE = "douban"     # 数据库名
```

### 3. 创建数据库

在 MySQL 中执行：

```sql
CREATE DATABASE douban CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 运行程序

```bash
python main.py
```

---

## 使用示例

### 爬取数据

选择菜单 `1`，程序会自动：
1. 初始化数据库表（如果不存在）
2. 依次爬取 10 页数据
3. 保存到 MySQL 数据库

```
🚀 开始爬取豆瓣Top250电影...
✅ 数据库表创建成功或已存在
🔄 正在爬取第 1/10 页...
   ✅ 本页获取 25 部电影
🔄 正在爬取第 2/10 页...
   ✅ 本页获取 25 部电影
...
✅ 爬取完成，共获取 250 部电影
✅ 成功保存 250 部新电影，更新 0 部电影
```

### 查看统计

选择菜单 `3`，查看数据库统计信息：

```
📊 数据库统计：
   电影总数: 250

🏆 评分最高的10部电影：
   1. 肖申克的救赎 (9.7分)
   2. 霸王别姬 (9.6分)
   3. 阿甘正传 (9.5分)
   ...
```

### 按类型筛选

选择菜单 `4`，输入类型如 `剧情`：

```
请输入电影类型 (如: 剧情, 喜剧, 动作): 剧情

🎬 类型 '剧情' 的电影 (XX部)：
   第1名: 肖申克的救赎 (9.7分)
   第2名: 霸王别姬 (9.6分)
   ...
```

---

## 依赖清单

| 包名 | 版本 | 用途 |
|------|------|------|
| requests | >=2.31.0 | HTTP 请求 |
| beautifulsoup4 | >=4.12.2 | HTML 解析 |
| lxml | >=4.9.3 | XML/HTML 解析器 |
| pymysql | >=1.1.0 | MySQL 驱动 |
| sqlalchemy | >=2.0.23 | ORM 框架 |

---

## 注意事项

1. **反爬策略**: 程序已内置随机延迟（2-4秒），请勿频繁运行
2. **数据库编码**: 确保 MySQL 使用 utf8mb4 编码以支持特殊字符
3. **网络环境**: 豆瓣可能有反爬机制，如遇 403 错误请稍后再试
4. **数据更新**: 支持重复运行，会自动更新已有数据

---

## 扩展开发

### 添加新的查询条件

在 `database.py` 的 `MovieRepository` 类中添加新方法：

```python
def get_movies_by_director(self, director):
    """根据导演查询电影"""
    return self.session.query(Movie).filter(
        Movie.director.contains(director)
    ).order_by(Movie.rank).all()
```

### 导出数据到 CSV

在 `main.py` 中添加导出功能：

```python
import csv

def export_to_csv():
    with MovieRepository() as repo:
        movies = repo.get_all_movies()
        with open('movies.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['排名', '名称', '评分', '年份'])
            for m in movies:
                writer.writerow([m.rank, m.title, m.rating, m.year])
```

---

## 数据表结构

```sql
CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    rank INT UNIQUE NOT NULL COMMENT '排名',
    title VARCHAR(255) NOT NULL COMMENT '电影名称',
    original_title VARCHAR(255) COMMENT '原名',
    director VARCHAR(255) COMMENT '导演',
    actors TEXT COMMENT '主演',
    year VARCHAR(20) COMMENT '年份',
    country VARCHAR(100) COMMENT '国家/地区',
    genre VARCHAR(100) COMMENT '类型',
    rating DECIMAL(3,1) COMMENT '评分',
    rating_count BIGINT COMMENT '评价人数',
    quote TEXT COMMENT '经典台词',
    poster_url VARCHAR(500) COMMENT '海报链接',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣电影Top250';
```
