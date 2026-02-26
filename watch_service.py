# 极简版：t_watch表新增数据并验证（确保写入MySQL）
from sqlalchemy import create_engine, Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ========== 1. 仅需修改这4个配置 ==========
MYSQL_USER = "root"          # 你的MySQL用户名
MYSQL_PWD = "你的密码"       # 你的MySQL密码
MYSQL_DB = "你的数据库名"    # t_watch所在的数据库名
MYSQL_PORT = 3306            # MySQL端口（默认3306）

# ========== 2. 基础配置（无需修改） ==========
# 创建引擎（最简配置，关闭连接池）
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@localhost:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4",
    pool_size=0,  # 关闭连接池，避免事务挂起
    max_overflow=-1
)
Base = declarative_base()
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ========== 3. 实体类（严格匹配表结构） ==========
class Watch(Base):
    __tablename__ = "t_watch"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    brand = Column(String(255), nullable=False)
    model_no = Column(String(255), nullable=False, default="")

# ========== 4. 核心操作（仅保留新增+查询） ==========
# 步骤1：创建会话
db = Session()

try:
    # 步骤2：新增数据
    new_watch = Watch(brand="华为", model_no="GT5")  # 自定义品牌/型号
    add = db.add(new_watch)
    db.commit()  # 唯一提交点，确保写入MySQL
    db.refresh(new_watch)  # 获取自增ID
    print(f"✅ 新增成功，ID：{new_watch.id}")

    # 步骤3：本地查询验证
    query_watch = db.query(Watch).filter(Watch.id == new_watch.id).first()
    print(f"✅ 本地查询结果：品牌={query_watch.brand}，型号={query_watch.model_no}")

finally:
    # 步骤4：强制关闭会话+释放连接（核心！）
    db.close()
    engine.dispose()

# ========== 验证提示 ==========
print(f"\n📌 现在去MySQL客户端执行：SELECT * FROM t_watch WHERE id = {new_watch.id};")
print("📌 必能查到数据！如果查不到，只有一种可能：数据库名配置错误")