# -*- coding: utf-8 -*-
"""
豆瓣电影Top250爬虫主程序

使用方法:
    1. 修改 config.py 中的数据库配置
    2. 确保MySQL已启动并创建了数据库
    3. 安装依赖: pip install -r requirements.txt
    4. 运行: python main.py
"""

import sys
from crawler import DoubanCrawler
from database import MovieRepository, init_database


def print_menu():
    """打印菜单"""
    print("\n" + "=" * 50)
    print("      豆瓣电影 Top250 爬虫")
    print("=" * 50)
    print("1. 爬取电影数据并保存到数据库")
    print("2. 查看所有电影")
    print("3. 查看电影统计")
    print("4. 按类型筛选电影")
    print("5. 按年份筛选电影")
    print("6. 删除所有数据")
    print("0. 退出")
    print("=" * 50)


def crawl_and_save():
    """爬取并保存电影数据"""
    print("\n🚀 开始爬取豆瓣Top250电影...")
    
    # 初始化数据库
    init_database()
    
    # 爬取数据
    crawler = DoubanCrawler()
    movies = crawler.crawl_all_movies()
    
    if movies:
        # 保存到数据库
        with MovieRepository() as repo:
            repo.save_movies(movies)
        print(f"\n✅ 成功保存 {len(movies)} 部电影到数据库")
    else:
        print("\n❌ 未获取到任何电影数据")


def show_all_movies():
    """显示所有电影"""
    with MovieRepository() as repo:
        movies = repo.get_all_movies()
        
        if not movies:
            print("\n⚠️ 数据库中没有电影数据，请先爬取数据")
            return
        
        print(f"\n📽️ 共 {len(movies)} 部电影：\n")
        print(f"{'排名':<6}{'评分':<8}{'名称':<30}{'年份':<10}{'类型':<20}")
        print("-" * 80)
        
        for movie in movies:
            title = movie.title[:28] + ".." if len(movie.title) > 30 else movie.title
            genre = movie.genre[:18] + ".." if movie.genre and len(movie.genre) > 20 else (movie.genre or "")
            print(f"{movie.rank:<6}{movie.rating:<8}{title:<30}{movie.year or '':<10}{genre:<20}")


def show_statistics():
    """显示电影统计"""
    with MovieRepository() as repo:
        count = repo.get_movie_count()
        
        if count == 0:
            print("\n⚠️ 数据库中没有电影数据")
            return
        
        print(f"\n📊 数据库统计：")
        print(f"   电影总数: {count}")
        
        # 评分最高的10部
        print("\n🏆 评分最高的10部电影：")
        top_movies = repo.get_top_rated(10)
        for i, movie in enumerate(top_movies, 1):
            print(f"   {i}. {movie.title} ({movie.rating}分)")


def filter_by_genre():
    """按类型筛选"""
    genre = input("\n请输入电影类型 (如: 剧情, 喜剧, 动作): ").strip()
    
    if not genre:
        print("⚠️ 类型不能为空")
        return
    
    with MovieRepository() as repo:
        movies = repo.get_movies_by_genre(genre)
        
        if not movies:
            print(f"\n⚠️ 没有找到类型为 '{genre}' 的电影")
            return
        
        print(f"\n🎬 类型 '{genre}' 的电影 ({len(movies)}部)：")
        for movie in movies:
            print(f"   第{movie.rank}名: {movie.title} ({movie.rating}分)")


def filter_by_year():
    """按年份筛选"""
    year = input("\n请输入年份 (如: 1994, 2019): ").strip()
    
    if not year:
        print("⚠️ 年份不能为空")
        return
    
    with MovieRepository() as repo:
        movies = repo.get_movies_by_year(year)
        
        if not movies:
            print(f"\n⚠️ 没有找到年份为 '{year}' 的电影")
            return
        
        print(f"\n📅 年份 '{year}' 的电影 ({len(movies)}部)：")
        for movie in movies:
            print(f"   第{movie.rank}名: {movie.title} ({movie.rating}分)")


def delete_all():
    """删除所有数据"""
    confirm = input("\n⚠️ 确定要删除所有电影数据吗? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        with MovieRepository() as repo:
            count = repo.delete_all_movies()
            print(f"✅ 已删除 {count} 部电影")
    else:
        print("已取消删除操作")


def main():
    """主函数"""
    print("\n🎬 欢迎使用豆瓣电影Top250爬虫")
    
    while True:
        print_menu()
        choice = input("请选择操作 (0-6): ").strip()
        
        if choice == '1':
            crawl_and_save()
        elif choice == '2':
            show_all_movies()
        elif choice == '3':
            show_statistics()
        elif choice == '4':
            filter_by_genre()
        elif choice == '5':
            filter_by_year()
        elif choice == '6':
            delete_all()
        elif choice == '0':
            print("\n👋 再见！")
            sys.exit(0)
        else:
            print("\n⚠️ 无效的选择，请重新输入")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
