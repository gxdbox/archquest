# 📦 数据库备份和恢复指南

## 🎯 功能说明

ArchQuest 现在具备完整的数据库备份和恢复机制，**确保你的游戏进度永不丢失**。

## ✨ 自动功能

### 1. **启动时自动备份**
每次启动项目时，系统会自动：
- 检查是否已有当日备份
- 如果没有，自动创建备份
- 保留最近 10 个备份文件
- 自动清理旧备份

### 2. **权限自动修复**
如果检测到数据库权限问题，系统会：
- 先自动备份当前数据库
- 尝试修复权限
- 如果修复失败，提示从备份恢复

## 🛠️ 手动操作

### 备份数据库

```bash
cd /Users/pony/Documents/code/ai/it_architecture/archquest
python3 database/backup_restore.py backup
```

### 查看所有备份

```bash
python3 database/backup_restore.py list
```

输出示例：
```
📦 可用的备份:
  1. game_backup_20251228_091234.db (28.0 KB, 2025-12-28 09:12:34)
  2. game_backup_20251227_153045.db (25.5 KB, 2025-12-27 15:30:45)
  3. game_backup_20251227_090000.db (20.1 KB, 2025-12-27 09:00:00)
```

### 从最新备份恢复

```bash
python3 database/backup_restore.py restore
```

### 修复权限问题

```bash
python3 database/backup_restore.py fix
```

## 📁 备份文件位置

所有备份文件存储在：
```
archquest/database/backups/
```

备份文件命名格式：
```
game_backup_YYYYMMDD_HHMMSS.db
```

## 🔄 工作流程

### 正常启动流程

```
启动项目
  ↓
检查数据库是否存在
  ↓
执行每日自动备份（如果需要）
  ↓
检查数据库权限
  ↓
如果有问题 → 自动备份 → 尝试修复
  ↓
启动服务
```

### 权限问题处理流程

```
检测到权限问题
  ↓
立即备份当前数据库
  ↓
尝试修复权限（chmod）
  ↓
测试写入是否成功
  ↓
成功 → 继续运行
失败 → 提示用户从备份恢复
```

## 🚨 紧急恢复

如果遇到数据库损坏或丢失：

1. **查看可用备份**
   ```bash
   python3 database/backup_restore.py list
   ```

2. **恢复最新备份**
   ```bash
   python3 database/backup_restore.py restore
   ```

3. **重启服务**
   ```bash
   ./start.sh
   ```

## 💡 最佳实践

### 1. **定期手动备份重要进度**
在完成重要关卡后，手动创建备份：
```bash
python3 database/backup_restore.py backup
```

### 2. **保留重要备份**
系统会自动清理旧备份（保留最近10个），如果有特别重要的备份，可以：
- 复制到其他位置
- 重命名（不以 `game_backup_` 开头）

### 3. **定期检查备份**
```bash
python3 database/backup_restore.py list
```

## 📊 备份策略

- **自动备份频率**: 每天首次启动时
- **保留数量**: 最近 10 个备份
- **备份时机**: 
  - 启动时（每日首次）
  - 检测到权限问题时
  - 恢复数据库前

## ⚙️ 技术细节

### 备份内容
- 完整的 SQLite 数据库文件
- 包含所有用户数据、进度、技能等

### 权限检查
- 测试数据库写入权限
- 检查目录权限
- 自动修复常见权限问题

### 安全性
- 恢复前自动备份当前数据库
- 所有操作都有错误处理
- 失败时保留原始数据

## 🔍 故障排查

### 问题：备份失败

**可能原因**：
- 磁盘空间不足
- 备份目录权限问题

**解决方案**：
```bash
# 检查磁盘空间
df -h

# 检查备份目录权限
ls -la database/backups/

# 手动创建备份目录
mkdir -p database/backups
chmod 755 database/backups
```

### 问题：恢复失败

**可能原因**：
- 备份文件损坏
- 目标位置权限问题

**解决方案**：
```bash
# 尝试其他备份
python3 database/backup_restore.py list
# 手动复制备份文件
cp database/backups/game_backup_XXXXXX.db database/game.db
```

### 问题：权限修复失败

**解决方案**：
```bash
# 手动修复权限
chmod 644 database/game.db
chmod 755 database/

# 如果还不行，从备份恢复
python3 database/backup_restore.py restore
```

## 📝 注意事项

1. **备份文件不会自动同步到 Git**（已在 .gitignore 中配置）
2. **重要数据请额外备份到云端或其他位置**
3. **系统会自动清理旧备份，重要备份请手动保存**
4. **恢复操作会覆盖当前数据库，请谨慎操作**

## 🎉 总结

有了这套备份机制，你再也不用担心数据丢失了！系统会：
- ✅ 自动备份
- ✅ 自动修复权限
- ✅ 保留历史版本
- ✅ 提供手动恢复工具

安心玩游戏，学习架构设计吧！🚀
