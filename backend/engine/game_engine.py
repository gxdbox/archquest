"""
游戏引擎 - 负责游戏流程控制
"""
import os
import yaml
from typing import Optional, Dict, Any, List

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUESTS_DIR = os.path.join(PROJECT_ROOT, "data", "quests")


class GameEngine:
    """游戏引擎"""
    
    # 关卡信息
    LEVELS = {
        1: {
            "name": "业务需求分析",
            "description": "学习如何分析和理解业务需求",
            "stages": 3,
            "exp_reward": 100
        },
        2: {
            "name": "质量属性识别",
            "description": "识别系统的质量属性需求",
            "stages": 3,
            "exp_reward": 150
        },
        3: {
            "name": "架构风格与组件设计",
            "description": "选择合适的架构风格并设计组件",
            "stages": 3,
            "exp_reward": 200
        },
        4: {
            "name": "架构评估（ATAM）",
            "description": "使用 ATAM 方法评估架构",
            "stages": 3,
            "exp_reward": 250
        }
    }
    
    def __init__(self):
        self.quests_cache: Dict[int, Dict] = {}
    
    def load_quest(self, level: int) -> Dict[str, Any]:
        """
        加载关卡任务配置
        
        Args:
            level: 关卡编号
            
        Returns:
            任务配置字典
        """
        if level in self.quests_cache:
            return self.quests_cache[level]
        
        quest_file = os.path.join(QUESTS_DIR, f"level{level}_quest.yaml")
        
        if not os.path.exists(quest_file):
            # 返回默认任务
            return self._get_default_quest(level)
        
        try:
            with open(quest_file, 'r', encoding='utf-8') as f:
                quest_data = yaml.safe_load(f)
                self.quests_cache[level] = quest_data
                return quest_data
        except Exception as e:
            print(f"加载任务文件失败: {e}")
            return self._get_default_quest(level)
    
    def _get_default_quest(self, level: int) -> Dict[str, Any]:
        """获取默认任务配置"""
        level_info = self.LEVELS.get(level, self.LEVELS[1])
        
        return {
            "level": level,
            "name": level_info["name"],
            "description": level_info["description"],
            "stages": [
                {
                    "stage": 1,
                    "name": "理论学习",
                    "description": f"学习{level_info['name']}的基本概念",
                    "key_points": ["基本概念", "核心原则", "实践方法"]
                },
                {
                    "stage": 2,
                    "name": "案例分析",
                    "description": f"分析{level_info['name']}的实际案例",
                    "key_points": ["案例理解", "问题识别", "解决方案"]
                },
                {
                    "stage": 3,
                    "name": "实战演练",
                    "description": f"完成{level_info['name']}的实战任务",
                    "key_points": ["方案设计", "技术选型", "风险评估"]
                }
            ]
        }
    
    def get_level_info(self, level: int) -> Dict[str, Any]:
        """获取关卡信息"""
        return self.LEVELS.get(level, self.LEVELS[1])
    
    def get_stage_info(self, level: int, stage: int) -> Dict[str, Any]:
        """获取阶段信息"""
        quest = self.load_quest(level)
        stages = quest.get("stages", [])
        
        for s in stages:
            if s.get("stage") == stage:
                return s
        
        # 返回默认阶段
        return {
            "stage": stage,
            "name": f"阶段 {stage}",
            "description": "完成当前阶段的任务",
            "key_points": ["理解", "分析", "设计"]
        }
    
    def get_all_levels(self) -> List[Dict[str, Any]]:
        """获取所有关卡列表"""
        return [
            {"level": k, **v}
            for k, v in self.LEVELS.items()
        ]
    
    def calculate_exp_reward(self, level: int, score: int) -> int:
        """
        计算经验奖励
        
        Args:
            level: 关卡
            score: 得分
            
        Returns:
            经验值
        """
        level_info = self.LEVELS.get(level, self.LEVELS[1])
        base_exp = level_info["exp_reward"]
        
        # 根据得分计算经验倍率
        if score >= 90:
            multiplier = 1.5
        elif score >= 80:
            multiplier = 1.2
        elif score >= 70:
            multiplier = 1.0
        elif score >= 60:
            multiplier = 0.8
        else:
            multiplier = 0.5
        
        return int(base_exp * multiplier)
    
    def get_next_stage(self, level: int, stage: int) -> tuple:
        """
        获取下一个阶段
        
        Args:
            level: 当前关卡
            stage: 当前阶段
            
        Returns:
            (next_level, next_stage, is_game_complete)
        """
        level_info = self.LEVELS.get(level, self.LEVELS[1])
        max_stages = level_info["stages"]
        
        if stage < max_stages:
            # 还有下一阶段
            return level, stage + 1, False
        elif level < 4:
            # 进入下一关
            return level + 1, 1, False
        else:
            # 游戏完成
            return level, stage, True
    
    def get_game_progress_percentage(self, level: int, stage: int) -> float:
        """计算游戏进度百分比"""
        total_stages = sum(l["stages"] for l in self.LEVELS.values())
        completed_stages = 0
        
        for l in range(1, level):
            completed_stages += self.LEVELS[l]["stages"]
        completed_stages += stage - 1
        
        return (completed_stages / total_stages) * 100


# 全局游戏引擎实例
game_engine = GameEngine()


def get_game_engine() -> GameEngine:
    """获取游戏引擎实例"""
    return game_engine
