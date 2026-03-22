# -*- coding: utf-8 -*-
"""
数据模型定义
使用SQLAlchemy定义电影实体类
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()


class Movie(Base):
    """电影实体类"""
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    rank = Column(Integer, unique=True, nullable=False, comment='排名')
    title = Column(String(255), nullable=False, comment='电影名称')
    original_title = Column(String(255), comment='原名')
    director = Column(String(255), comment='导演')
    actors = Column(Text, comment='主演')
    year = Column(String(20), comment='年份')
    country = Column(String(100), comment='国家/地区')
    genre = Column(String(100), comment='类型')
    rating = Column(Float, comment='评分')
    rating_count = Column(BigInteger, comment='评价人数')
    quote = Column(Text, comment='经典台词')
    poster_url = Column(String(500), comment='海报链接')
    
    def __repr__(self):
        return f"<Movie(rank={self.rank}, title='{self.title}', rating={self.rating})>"
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'rank': self.rank,
            'title': self.title,
            'original_title': self.original_title,
            'director': self.director,
            'actors': self.actors,
            'year': self.year,
            'country': self.country,
            'genre': self.genre,
            'rating': self.rating,
            'rating_count': self.rating_count,
            'quote': self.quote,
            'poster_url': self.poster_url,
        }


# 创建数据库引擎
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

# 创建会话工厂
Session = sessionmaker(bind=engine)


def init_db():
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(engine)
    print("✅ 数据库表创建成功或已存在")


def get_session():
    """获取数据库会话"""
    return Session()
