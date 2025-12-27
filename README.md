# 🎮 ArchQuest

<div align="center">

**Master Software Architecture Through RPG Adventure**

*通过 RPG 冒险掌握软件架构*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)

[English](#english) | [中文](#中文)

</div>

---

## English

### 📖 About

ArchQuest is an RPG-style learning platform that teaches software architecture design through gamification. Based on the ABSD (Architecture-Based Software Development) methodology, you'll grow from a junior architect to a chief architect by completing four challenging quests under the guidance of CTO Wang.

### ✨ Features

- 🤖 **AI-Powered**: Utilizes local Ollama (qwen:7b) for dynamic story generation, quest creation, and answer evaluation
- 🎮 **RPG Mechanics**: Experience system, level progression, and skill tree
- 🎭 **Immersive Experience**: Full guidance from CTO Wang NPC
- 💼 **Real-World Scenarios**: Based on actual architecture design challenges

### 🎯 Four Quests

1. **📋 Business Requirements Analysis** - Learn to analyze and understand business needs
2. **⭐ Quality Attributes Identification** - Identify system quality attribute requirements
3. **🏛️ Architecture Style & Component Design** - Choose appropriate architecture styles and design components
4. **🔍 Architecture Evaluation (ATAM)** - Evaluate architecture using ATAM methodology

### 🛠️ Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: SQLite + SQLAlchemy
- **AI Model**: Ollama (qwen:7b)
- **Architecture**: DDD + Layered Architecture

### 🚀 Quick Start

#### Prerequisites

- Python 3.9+
- Ollama installed and running

#### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/archquest.git
cd archquest

# Install dependencies
pip install -r requirements.txt

# Start Ollama service
ollama serve

# Pull the model (in another terminal)
ollama pull qwen:7b
```

#### Run the Application

```bash
# Start backend (Terminal 1)
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (Terminal 2)
python3 -m streamlit run frontend/app.py --server.port 8501
```

#### Access

- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

### 📁 Project Structure

```
archquest/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── ollama_api.py        # Ollama API wrapper
│   └── engine/
│       ├── game_engine.py   # Game engine
│       ├── evaluator.py     # Answer evaluator
│       └── progression.py   # Progress system
├── frontend/
│   └── app.py               # Streamlit frontend
├── database/
│   ├── init_db.py           # Database initialization
│   └── models.py            # SQLAlchemy models
├── data/
│   ├── skill_tree.json      # Skill tree configuration
│   └── quests/              # Quest definitions
├── requirements.txt
└── README.md
```

### 🌳 Skill Tree

| Skill | Unlock Level | Description |
|-------|--------------|-------------|
| Requirements Analysis | LV.1 | Analyze and understand business requirements |
| Quality Attributes | LV.3 | Identify and quantify quality attributes |
| Architecture Styles | LV.5 | Master various architecture styles |
| Component Design | LV.7 | Design high cohesion, low coupling components |
| ATAM Evaluation | LV.10 | Use ATAM to evaluate architecture |
| Trade-off Analysis | LV.12 | Optimal decision-making among constraints |
| Risk Management | LV.15 | Identify and manage architecture risks |
| Architecture Documentation | LV.18 | Write clear architecture documentation |

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

## 中文

### 📖 游戏简介

ArchQuest 是一款基于 ABSD（基于架构的软件开发）方法的 RPG 养成游戏，帮助你学习软件架构设计。你是一名刚入职的初级架构师，在 CTO 老王的指导下，通过完成 ABSD 四关挑战，逐步成长为首席架构师。

### 🎯 四关挑战

1. **📋 业务需求分析** - 学习如何分析和理解业务需求
2. **⭐ 质量属性识别** - 识别系统的质量属性需求
3. **🏛️ 架构风格与组件设计** - 选择合适的架构风格并设计组件
4. **🔍 架构评估（ATAM）** - 使用 ATAM 方法评估架构

### 🌟 游戏特色

- **AI 驱动**: 使用本地 Ollama (qwen:7b) 模型生成剧情、出题和评分
- **RPG 养成**: 经验系统、等级系统、技能树
- **沉浸式体验**: CTO 老王 NPC 全程指导
- **实战导向**: 基于真实架构设计场景

## 🛠️ 技术栈

- **后端**: FastAPI
- **前端**: Streamlit
- **数据库**: SQLite + SQLAlchemy
- **AI 模型**: Ollama (qwen:7b)
- **架构风格**: DDD + 分层架构

## 📁 项目结构

```
archquest/
├── backend/
│   ├── main.py              # FastAPI 主入口
│   ├── ollama_api.py        # Ollama API 封装
│   └── engine/
│       ├── game_engine.py   # 游戏引擎
│       ├── evaluator.py     # 评估器
│       └── progression.py   # 进度系统
├── frontend/
│   └── app.py               # Streamlit 前端
├── database/
│   ├── init_db.py           # 数据库初始化
│   └── models.py            # SQLAlchemy 模型
├── data/
│   ├── skill_tree.json      # 技能树配置
│   └── quests/
│       ├── level1_quest.yaml  # 第1关任务
│       ├── level2_quest.yaml  # 第2关任务
│       ├── level3_quest.yaml  # 第3关任务
│       └── level4_quest.yaml  # 第4关任务
├── requirements.txt
└── README.md
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/yourusername/archquest.git
cd archquest

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动 Ollama

确保已安装 Ollama 并下载 qwen:7b 模型：

```bash
# 安装 Ollama (如果未安装)
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh

# 启动 Ollama 服务
ollama serve

# 在另一个终端下载模型
ollama pull qwen:7b
```

### 3. 启动后端服务

```bash
# 在项目根目录
cd archquest
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

后端 API 文档: http://localhost:8000/docs

### 4. 启动前端

```bash
# 在另一个终端
cd archquest
python3 -m streamlit run frontend/app.py --server.port 8501
```

前端界面: http://localhost:8501

## 📡 API 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/create_player` | POST | 创建新玩家 |
| `/get_story` | POST | 获取当前关卡剧情和任务 |
| `/submit_answer` | POST | 提交回答并获取评分 |
| `/get_progress/{user_id}` | GET | 获取玩家进度 |
| `/get_skills/{user_id}` | GET | 获取玩家技能树 |
| `/get_levels` | GET | 获取所有关卡信息 |
| `/health` | GET | 健康检查 |

## 🎮 游戏流程示例

### 1. 创建角色

```
输入名字: 小明
选择头像: 🧑‍💻
点击 "开始冒险"
```

### 2. 进入第一关

```
CTO 老王: "欢迎加入公司！我们正在做一个库存管理系统..."
任务: 分析库存管理系统的业务需求
评分要点: 识别利益相关者、功能性需求、隐含需求
```

### 3. 提交回答

```
你的回答: "库存管理系统的主要利益相关者包括：
1. 仓库管理员 - 需要实时查看库存、入库出库操作
2. 采购部门 - 需要库存预警、采购建议
3. 财务部门 - 需要库存成本核算
..."
```

### 4. 获得评分

```
得分: 85 分
评语: "分析得很全面，特别是对利益相关者的识别..."
获得经验: +120 EXP
升级: LV.1 → LV.2
解锁技能: 需求分析 LV.1
```

### 5. 继续挑战

完成所有四关，成为首席架构师！

## 🌳 技能树

| 技能 | 解锁等级 | 描述 |
|------|----------|------|
| 需求分析 | LV.1 | 分析和理解业务需求 |
| 质量属性 | LV.3 | 识别和量化质量属性 |
| 架构风格 | LV.5 | 掌握各种架构风格 |
| 组件设计 | LV.7 | 设计高内聚低耦合组件 |
| ATAM评估 | LV.10 | 使用ATAM评估架构 |
| 权衡分析 | LV.12 | 多约束间最优决策 |
| 风险管理 | LV.15 | 识别和管理架构风险 |
| 架构文档 | LV.18 | 编写清晰架构文档 |

## 🔧 扩展关卡

### 添加新关卡

1. 在 `data/quests/` 目录创建新的 YAML 文件，如 `level5_quest.yaml`

```yaml
level: 5
name: "微服务架构实战"
description: "设计和实现微服务架构"
stages:
  - stage: 1
    name: "服务拆分"
    description: "学习如何拆分微服务"
    key_points:
      - "领域边界识别"
      - "服务粒度控制"
      - "数据一致性"
    pass_score: 60
```

2. 在 `backend/engine/game_engine.py` 中添加关卡定义：

```python
LEVELS = {
    # ... 现有关卡
    5: {
        "name": "微服务架构实战",
        "description": "设计和实现微服务架构",
        "stages": 3,
        "exp_reward": 300
    }
}
```

3. 在 `data/skill_tree.json` 中添加相关技能

## 🐛 常见问题

### Q: Ollama 连接失败

确保 Ollama 服务正在运行：
```bash
ollama serve
```

### Q: 模型响应慢

qwen:7b 模型需要一定的计算资源，建议：
- 使用 GPU 加速
- 或尝试更小的模型如 qwen:1.8b

### Q: 数据库错误

删除 `database/game.db` 文件，重新启动后端会自动创建新数据库。

## 📝 开发说明

### 目录结构说明

- `backend/`: 后端服务，使用 FastAPI
- `frontend/`: 前端界面，使用 Streamlit
- `database/`: 数据库模型和初始化
- `data/`: 游戏数据配置文件

### 代码风格

- 使用 Python 3.9+
- 遵循 PEP 8 规范
- 使用类型注解

## 📄 License

MIT License

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

**开始你的架构师之旅吧！** 🚀
