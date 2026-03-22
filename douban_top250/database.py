# -*- coding: utf-8 -*-
"""
数据库操作模块
负责电影的增删改查操作
"""

from sqlalchemy import func
from models import Movie, get_session, init_db


class MovieRepository:
    """电影数据仓库类"""
    
    def __init__(self):
        self.session = get_session()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
    
    def save_movies(self, movies):
        """
        批量保存电影
        
        Args:
            movies: Movie对象列表
        """
        count = 0
        for movie in movies:
            # 检查是否已存在
            existing = self.session.query(Movie).filter_by(rank=movie.rank).first()
            if existing:
                # 更新现有记录
                existing.title = movie.title
                existing.original_title = movie.original_title
                existing.director = movie.director
                existing.actors = movie.actors
                existing.year = movie.year
                existing.country = movie.country
                existing.genre = movie.genre
                existing.rating = movie.rating
                existing.rating_count = movie.rating_count
                existing.quote = movie.quote
                existing.poster_url = movie.poster_url
            else:
                # 插入新记录
                self.session.add(movie)
                count += 1
        
        self.session.commit()
        print(f"✅ 成功保存 {count} 部新电影，更新 {len(movies) - count} 部电影")
    
    def get_all_movies(self):
        """
        获取所有电影
        
        Returns:
            list: Movie对象列表
        """
        return self.session.query(Movie).order_by(Movie.rank).all()
    
    def get_movie_by_rank(self, rank):
        """
        根据排名获取电影
        
        Args:
            rank: 排名
            
        Returns:
            Movie: 电影对象或None
        """
        return self.session.query(Movie).filter_by(rank=rank).first()
    
    def get_movie_count(self):
        """
        获取电影总数
        
        Returns:
            int: 电影数量
        """
        return self.session.query(func.count(Movie.id)).scalar()
    
    def get_top_rated(self, limit=10):
        """
        获取评分最高的电影
        
        Args:
            limit: 数量限制
            
        Returns:
            list: Movie对象列表
        """
        return self.session.query(Movie).order_by(Movie.rating.desc()).limit(limit).all()
    
    def get_movies_by_year(self, year):
        """
        根据年份获取电影
        
        Args:
            year: 年份
            
        Returns:
            list: Movie对象列表
        """
        return self.session.query(Movie).filter(Movie.year.contains(year)).order_by(Movie.rank).all()
    
    def get_movies_by_genre(self, genre):
        """
        根据类型获取电影
        
        Args:
            genre: 类型
            
        Returns:
            list: Movie对象列表
        """
        return self.session.query(Movie).filter(Movie.genre.contains(genre)).order_by(Movie.rank).all()
    
    def delete_all_movies(self):
        """删除所有电影"""
        count = self.session.query(Movie).delete()
        self.session.commit()
        print(f"✅ 已删除 {count} 部电影")
        return count


def init_database():
    """初始化数据库"""
    init_db()
