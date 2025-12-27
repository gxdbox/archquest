"""
FastAPI 主入口
Architecture RPG 后端服务
"""
import os
import sys
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.init_db import get_db, init_database, get_db_session
from database.models import User, Progress, Skill, GameLog
from backend.ollama_api import get_ollama_client
from backend.engine.game_engine import get_game_engine
from backend.engine.evaluator import get_evaluator
from backend.engine.progression import get_progression_system

# 初始化数据库
init_database()

# 创建 FastAPI 应用
app = FastAPI(
    title="🎮 Architecture RPG",
    description="RPG 架构师养成游戏后端 API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Pydantic 模型 ====================

class CreatePlayerRequest(BaseModel):
    username: str
    avatar: Optional[str] = "🧑‍💻"


class CreatePlayerResponse(BaseModel):
    id: int
    username: str
    avatar: str
    title: str
    message: str


class GetStoryRequest(BaseModel):
    user_id: int
    level: Optional[int] = None
    stage: Optional[int] = None


class StoryResponse(BaseModel):
    story: str
    level: int
    stage: int
    level_name: str
    stage_name: str
    quest: str
    key_points: List[str]


class SubmitAnswerRequest(BaseModel):
    user_id: int
    answer: str


class SubmitAnswerResponse(BaseModel):
    score: int
    comment: str
    pass_flag: bool
    advice: str
    exp_gained: int
    level_up_info: Optional[dict] = None
    next_stage: Optional[dict] = None
    game_complete: bool = False


class ProgressResponse(BaseModel):
    user_id: int
    username: str
    avatar: str
    title: str
    current_level: int
    current_stage: int
    experience: int
    player_level: int
    total_score: int
    quests_completed: int
    exp_progress: dict
    unlocked_skills: List[dict]
    game_progress_percent: float


class SkillResponse(BaseModel):
    skills: List[dict]


# ==================== API 路由 ====================

@app.get("/")
async def root():
    """API 根路径"""
    return {
        "name": "🎮 Architecture RPG API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/create_player",
            "/get_story",
            "/submit_answer",
            "/get_progress",
            "/get_skills",
            "/get_levels"
        ]
    }


@app.post("/create_player", response_model=CreatePlayerResponse)
async def create_player(request: CreatePlayerRequest):
    """
    创建新玩家
    """
    db = get_db_session()
    try:
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == request.username).first()
        if existing_user:
            # 返回已存在的用户
            return CreatePlayerResponse(
                id=existing_user.id,
                username=existing_user.username,
                avatar=existing_user.avatar,
                title=existing_user.title,
                message="欢迎回来，架构师！"
            )
        
        # 创建新用户
        user = User(
            username=request.username,
            avatar=request.avatar,
            title="初级架构师"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # 创建进度记录
        progress = Progress(
            user_id=user.id,
            current_level=1,
            current_stage=1,
            experience=0,
            player_level=1,
            total_score=0,
            quests_completed=0,
            game_state={}
        )
        db.add(progress)
        
        # 初始化技能
        progression = get_progression_system()
        initial_skills = progression.get_unlockable_skills(1)
        for skill_info in initial_skills:
            skill = Skill(
                user_id=user.id,
                skill_name=skill_info["name"],
                skill_level=1,
                unlocked=True,
                unlocked_at=datetime.utcnow()
            )
            db.add(skill)
        
        db.commit()
        
        return CreatePlayerResponse(
            id=user.id,
            username=user.username,
            avatar=user.avatar,
            title=user.title,
            message="欢迎加入，新晋架构师！你的冒险即将开始..."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建玩家失败: {str(e)}")
    finally:
        db.close()


@app.post("/get_story", response_model=StoryResponse)
async def get_story(request: GetStoryRequest):
    """
    获取当前关卡剧情和任务
    """
    db = get_db_session()
    try:
        # 获取用户进度
        progress = db.query(Progress).filter(Progress.user_id == request.user_id).first()
        if not progress:
            raise HTTPException(status_code=404, detail="玩家不存在")
        
        # 确定关卡和阶段
        level = request.level if request.level else progress.current_level
        stage = request.stage if request.stage else progress.current_stage
        
        # 获取游戏引擎
        engine = get_game_engine()
        ollama = get_ollama_client()
        
        # 获取关卡和阶段信息
        level_info = engine.get_level_info(level)
        stage_info = engine.get_stage_info(level, stage)
        
        # 生成剧情
        context = f"玩家当前等级: {progress.player_level}, 已完成任务: {progress.quests_completed}"
        story = ollama.generate_story(level, stage, context)
        
        # 生成任务
        quest = ollama.generate_quest(level, stage_info)
        
        # 更新游戏状态
        game_state = progress.game_state or {}
        game_state["current_quest"] = quest
        game_state["current_key_points"] = stage_info.get("key_points", [])
        progress.game_state = game_state
        progress.current_level = level
        progress.current_stage = stage
        db.commit()
        
        return StoryResponse(
            story=story,
            level=level,
            stage=stage,
            level_name=level_info["name"],
            stage_name=stage_info.get("name", f"阶段 {stage}"),
            quest=quest,
            key_points=stage_info.get("key_points", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取剧情失败: {str(e)}")
    finally:
        db.close()


@app.post("/submit_answer", response_model=SubmitAnswerResponse)
async def submit_answer(request: SubmitAnswerRequest):
    """
    提交玩家回答并评分
    """
    db = get_db_session()
    try:
        # 获取用户和进度
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="玩家不存在")
        
        progress = db.query(Progress).filter(Progress.user_id == request.user_id).first()
        if not progress:
            raise HTTPException(status_code=404, detail="玩家进度不存在")
        
        # 获取当前任务信息
        game_state = progress.game_state or {}
        current_quest = game_state.get("current_quest", "")
        key_points = game_state.get("current_key_points", [])
        
        # 评估回答
        evaluator = get_evaluator()
        eval_result = evaluator.evaluate(current_quest, request.answer, key_points)
        
        score = eval_result["score"]
        comment = eval_result["comment"]
        pass_flag = eval_result["pass_flag"]
        
        # 获取建议
        advice = evaluator.get_advice(score, progress.current_level, request.answer)
        
        # 计算经验
        engine = get_game_engine()
        progression = get_progression_system()
        
        exp_gained = engine.calculate_exp_reward(progress.current_level, score)
        old_exp = progress.experience
        
        # 更新进度
        progress.experience += exp_gained
        progress.total_score += score
        progress.quests_completed += 1
        
        # 检查升级
        exp_result = progression.add_experience(old_exp, exp_gained)
        level_up_info = exp_result.get("level_up_info")
        
        if level_up_info:
            progress.player_level = level_up_info["new_level"]
            user.title = level_up_info["new_title"]
            
            # 解锁新技能
            for skill_info in level_up_info.get("unlocked_skills", []):
                existing_skill = db.query(Skill).filter(
                    Skill.user_id == user.id,
                    Skill.skill_name == skill_info["name"]
                ).first()
                
                if not existing_skill:
                    skill = Skill(
                        user_id=user.id,
                        skill_name=skill_info["name"],
                        skill_level=1,
                        unlocked=True,
                        unlocked_at=datetime.utcnow()
                    )
                    db.add(skill)
        
        # 记录游戏日志
        log = GameLog(
            user_id=user.id,
            level=progress.current_level,
            stage=progress.current_stage,
            player_answer=request.answer[:1000],
            ai_response=comment,
            score=score,
            passed=pass_flag
        )
        db.add(log)
        
        # 计算下一阶段
        next_stage = None
        game_complete = False
        
        if pass_flag:
            next_level, next_stage_num, game_complete = engine.get_next_stage(
                progress.current_level, progress.current_stage
            )
            
            if not game_complete:
                progress.current_level = next_level
                progress.current_stage = next_stage_num
                next_stage = {
                    "level": next_level,
                    "stage": next_stage_num,
                    "level_name": engine.get_level_info(next_level)["name"]
                }
        
        db.commit()
        
        return SubmitAnswerResponse(
            score=score,
            comment=comment,
            pass_flag=pass_flag,
            advice=advice,
            exp_gained=exp_gained,
            level_up_info=level_up_info,
            next_stage=next_stage,
            game_complete=game_complete
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"提交回答失败: {str(e)}")
    finally:
        db.close()


@app.get("/get_progress/{user_id}", response_model=ProgressResponse)
async def get_progress(user_id: int):
    """
    获取玩家进度
    """
    db = get_db_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="玩家不存在")
        
        progress = db.query(Progress).filter(Progress.user_id == user_id).first()
        if not progress:
            raise HTTPException(status_code=404, detail="玩家进度不存在")
        
        # 获取技能
        skills = db.query(Skill).filter(Skill.user_id == user_id, Skill.unlocked == True).all()
        unlocked_skills = [
            {"name": s.skill_name, "level": s.skill_level}
            for s in skills
        ]
        
        # 计算经验进度
        progression = get_progression_system()
        exp_progress = progression.get_exp_progress(progress.experience, progress.player_level)
        
        # 计算游戏进度
        engine = get_game_engine()
        game_progress = engine.get_game_progress_percentage(
            progress.current_level, progress.current_stage
        )
        
        return ProgressResponse(
            user_id=user.id,
            username=user.username,
            avatar=user.avatar,
            title=user.title,
            current_level=progress.current_level,
            current_stage=progress.current_stage,
            experience=progress.experience,
            player_level=progress.player_level,
            total_score=progress.total_score,
            quests_completed=progress.quests_completed,
            exp_progress=exp_progress,
            unlocked_skills=unlocked_skills,
            game_progress_percent=game_progress
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取进度失败: {str(e)}")
    finally:
        db.close()


@app.get("/get_skills/{user_id}", response_model=SkillResponse)
async def get_skills(user_id: int):
    """
    获取玩家技能树
    """
    db = get_db_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="玩家不存在")
        
        progress = db.query(Progress).filter(Progress.user_id == user_id).first()
        player_level = progress.player_level if progress else 1
        
        # 获取所有技能定义
        progression = get_progression_system()
        all_skills = progression.get_all_skills()
        
        # 获取玩家已解锁的技能
        user_skills = db.query(Skill).filter(Skill.user_id == user_id).all()
        user_skill_map = {s.skill_name: s for s in user_skills}
        
        skills = []
        for skill_def in all_skills:
            user_skill = user_skill_map.get(skill_def["name"])
            skills.append({
                "id": skill_def["id"],
                "name": skill_def["name"],
                "unlock_level": skill_def["unlock_level"],
                "max_level": skill_def["max_level"],
                "unlocked": user_skill.unlocked if user_skill else False,
                "current_level": user_skill.skill_level if user_skill else 0,
                "can_unlock": player_level >= skill_def["unlock_level"]
            })
        
        return SkillResponse(skills=skills)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取技能失败: {str(e)}")
    finally:
        db.close()


@app.get("/get_levels")
async def get_levels():
    """
    获取所有关卡信息
    """
    engine = get_game_engine()
    return {"levels": engine.get_all_levels()}


@app.get("/health")
async def health_check():
    """健康检查"""
    ollama = get_ollama_client()
    
    # 测试 Ollama 连接
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        ollama_status = "connected" if response.status_code == 200 else "error"
    except:
        ollama_status = "disconnected"
    
    return {
        "status": "healthy",
        "ollama": ollama_status,
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
