"""
数据库初始化脚本
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Base, User, Progress, Skill

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), "game.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# 创建引擎
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database():
    """初始化数据库，创建所有表"""
    # 导入备份恢复工具
    try:
        from database.backup_restore import auto_backup_on_startup, fix_database_permissions
        
        # 启动时自动备份
        auto_backup_on_startup()
        
        # 检查并修复权限
        if os.path.exists(DB_PATH):
            fix_database_permissions()
    except Exception as e:
        print(f"⚠️ 备份/权限检查失败: {e}")
    
    Base.metadata.create_all(bind=engine)
    print(f"✅ 数据库初始化完成: {DB_PATH}")


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    """直接获取数据库会话（非生成器）"""
    return SessionLocal()


if __name__ == "__main__":
    init_database()
    print("🎮 Architecture RPG 数据库已就绪！")
