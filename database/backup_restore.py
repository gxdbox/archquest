"""
数据库备份和恢复工具
防止数据丢失
"""
import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "game.db"
BACKUP_DIR = Path(__file__).parent / "backups"


def ensure_backup_dir():
    """确保备份目录存在"""
    BACKUP_DIR.mkdir(exist_ok=True)


def backup_database():
    """备份数据库"""
    if not DB_PATH.exists():
        print("⚠️  数据库文件不存在，无需备份")
        return None
    
    ensure_backup_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"game_backup_{timestamp}.db"
    
    try:
        shutil.copy2(DB_PATH, backup_path)
        print(f"✅ 数据库已备份到: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ 备份失败: {e}")
        return None


def list_backups():
    """列出所有备份"""
    if not BACKUP_DIR.exists():
        return []
    
    backups = sorted(BACKUP_DIR.glob("game_backup_*.db"), reverse=True)
    return backups


def restore_from_backup(backup_path=None):
    """从备份恢复数据库"""
    if backup_path is None:
        # 使用最新的备份
        backups = list_backups()
        if not backups:
            print("❌ 没有可用的备份")
            return False
        backup_path = backups[0]
    
    try:
        # 如果当前数据库存在，先备份
        if DB_PATH.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            old_backup = BACKUP_DIR / f"game_before_restore_{timestamp}.db"
            shutil.copy2(DB_PATH, old_backup)
            print(f"📦 当前数据库已备份到: {old_backup}")
        
        # 恢复备份
        shutil.copy2(backup_path, DB_PATH)
        print(f"✅ 数据库已从备份恢复: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ 恢复失败: {e}")
        return False


def fix_database_permissions():
    """修复数据库权限问题"""
    if not DB_PATH.exists():
        print("⚠️  数据库文件不存在")
        return False
    
    try:
        # 尝试打开数据库进行写入测试
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 测试写入
        cursor.execute("CREATE TABLE IF NOT EXISTS _permission_test (id INTEGER)")
        cursor.execute("DROP TABLE _permission_test")
        conn.commit()
        conn.close()
        
        print("✅ 数据库权限正常")
        return True
    except sqlite3.OperationalError as e:
        if "readonly" in str(e).lower():
            print("❌ 检测到数据库只读问题")
            
            # 先备份
            backup_path = backup_database()
            if not backup_path:
                print("❌ 无法备份数据库，中止修复")
                return False
            
            # 尝试修复权限
            try:
                os.chmod(DB_PATH, 0o644)
                os.chmod(DB_PATH.parent, 0o755)
                
                # 再次测试
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS _permission_test (id INTEGER)")
                cursor.execute("DROP TABLE _permission_test")
                conn.commit()
                conn.close()
                
                print("✅ 数据库权限已修复")
                return True
            except Exception as fix_error:
                print(f"❌ 权限修复失败: {fix_error}")
                print(f"💡 建议从备份恢复: {backup_path}")
                return False
        else:
            print(f"❌ 数据库错误: {e}")
            return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False


def auto_backup_on_startup():
    """启动时自动备份"""
    if DB_PATH.exists():
        # 检查今天是否已经备份过
        today = datetime.now().strftime("%Y%m%d")
        backups = list_backups()
        
        today_backups = [b for b in backups if today in b.name]
        
        if not today_backups:
            print("📦 执行每日自动备份...")
            backup_database()
        else:
            print(f"✅ 今日已有备份: {today_backups[0].name}")
    
    # 清理旧备份（保留最近10个）
    cleanup_old_backups(keep=10)


def cleanup_old_backups(keep=10):
    """清理旧备份，保留最近的几个"""
    backups = list_backups()
    if len(backups) > keep:
        for old_backup in backups[keep:]:
            try:
                old_backup.unlink()
                print(f"🗑️  删除旧备份: {old_backup.name}")
            except Exception as e:
                print(f"⚠️  删除备份失败: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python backup_restore.py backup          # 备份数据库")
        print("  python backup_restore.py restore         # 从最新备份恢复")
        print("  python backup_restore.py list            # 列出所有备份")
        print("  python backup_restore.py fix             # 修复权限问题")
        print("  python backup_restore.py auto            # 自动备份（启动时）")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "backup":
        backup_database()
    elif command == "restore":
        restore_from_backup()
    elif command == "list":
        backups = list_backups()
        if backups:
            print("📦 可用的备份:")
            for i, backup in enumerate(backups, 1):
                size = backup.stat().st_size / 1024
                mtime = datetime.fromtimestamp(backup.stat().st_mtime)
                print(f"  {i}. {backup.name} ({size:.1f} KB, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print("没有可用的备份")
    elif command == "fix":
        fix_database_permissions()
    elif command == "auto":
        auto_backup_on_startup()
    else:
        print(f"未知命令: {command}")
        sys.exit(1)
