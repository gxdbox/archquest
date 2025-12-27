"""
进度系统 - 负责经验、等级、技能树管理
"""
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILL_TREE_PATH = os.path.join(PROJECT_ROOT, "data", "skill_tree.json")


class ProgressionSystem:
    """进度系统"""
    
    # 等级经验表
    LEVEL_EXP = {
        1: 0,
        2: 100,
        3: 250,
        4: 450,
        5: 700,
        6: 1000,
        7: 1350,
        8: 1750,
        9: 2200,
        10: 2700,
        11: 3250,
        12: 3850,
        13: 4500,
        14: 5200,
        15: 5950,
        16: 6750,
        17: 7600,
        18: 8500,
        19: 9450,
        20: 10450
    }
    
    # 称号系统
    TITLES = {
        1: "初级架构师",
        5: "助理架构师",
        10: "中级架构师",
        15: "高级架构师",
        20: "首席架构师"
    }
    
    def __init__(self):
        self.skill_tree = self._load_skill_tree()
    
    def _load_skill_tree(self) -> Dict[str, Any]:
        """加载技能树配置"""
        if os.path.exists(SKILL_TREE_PATH):
            try:
                with open(SKILL_TREE_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载技能树失败: {e}")
        
        return self._get_default_skill_tree()
    
    def _get_default_skill_tree(self) -> Dict[str, Any]:
        """获取默认技能树"""
        return {
            "skills": [
                {"id": "req_analysis", "name": "需求分析", "unlock_level": 1, "max_level": 5},
                {"id": "quality_attr", "name": "质量属性", "unlock_level": 3, "max_level": 5},
                {"id": "arch_style", "name": "架构风格", "unlock_level": 5, "max_level": 5},
                {"id": "component_design", "name": "组件设计", "unlock_level": 7, "max_level": 5},
                {"id": "atam", "name": "ATAM评估", "unlock_level": 10, "max_level": 5},
                {"id": "trade_off", "name": "权衡分析", "unlock_level": 12, "max_level": 5},
                {"id": "risk_mgmt", "name": "风险管理", "unlock_level": 15, "max_level": 5},
                {"id": "arch_doc", "name": "架构文档", "unlock_level": 18, "max_level": 5}
            ]
        }
    
    def calculate_level(self, experience: int) -> int:
        """
        根据经验计算等级
        
        Args:
            experience: 总经验值
            
        Returns:
            等级
        """
        level = 1
        for lv, exp in self.LEVEL_EXP.items():
            if experience >= exp:
                level = lv
            else:
                break
        return min(level, 20)
    
    def get_exp_for_next_level(self, current_level: int) -> int:
        """获取升到下一级所需经验"""
        if current_level >= 20:
            return 0
        return self.LEVEL_EXP.get(current_level + 1, 0)
    
    def get_current_level_exp(self, current_level: int) -> int:
        """获取当前等级所需经验"""
        return self.LEVEL_EXP.get(current_level, 0)
    
    def get_exp_progress(self, experience: int, current_level: int) -> Dict[str, Any]:
        """
        获取经验进度
        
        Args:
            experience: 当前经验
            current_level: 当前等级
            
        Returns:
            {current_exp, next_level_exp, progress_percent}
        """
        current_level_exp = self.get_current_level_exp(current_level)
        next_level_exp = self.get_exp_for_next_level(current_level)
        
        if current_level >= 20:
            return {
                "current_exp": experience,
                "next_level_exp": experience,
                "progress_percent": 100.0,
                "exp_needed": 0
            }
        
        exp_in_level = experience - current_level_exp
        exp_for_level = next_level_exp - current_level_exp
        progress = (exp_in_level / exp_for_level) * 100 if exp_for_level > 0 else 100
        
        return {
            "current_exp": experience,
            "next_level_exp": next_level_exp,
            "progress_percent": min(progress, 100),
            "exp_needed": max(0, next_level_exp - experience)
        }
    
    def get_title(self, level: int) -> str:
        """获取称号"""
        title = "初级架构师"
        for lv, t in self.TITLES.items():
            if level >= lv:
                title = t
        return title
    
    def get_unlockable_skills(self, level: int) -> List[Dict[str, Any]]:
        """
        获取可解锁的技能
        
        Args:
            level: 当前等级
            
        Returns:
            可解锁技能列表
        """
        skills = self.skill_tree.get("skills", [])
        return [s for s in skills if s.get("unlock_level", 1) <= level]
    
    def get_all_skills(self) -> List[Dict[str, Any]]:
        """获取所有技能"""
        return self.skill_tree.get("skills", [])
    
    def check_level_up(self, old_exp: int, new_exp: int) -> Optional[Dict[str, Any]]:
        """
        检查是否升级
        
        Args:
            old_exp: 旧经验
            new_exp: 新经验
            
        Returns:
            升级信息或 None
        """
        old_level = self.calculate_level(old_exp)
        new_level = self.calculate_level(new_exp)
        
        if new_level > old_level:
            # 检查新解锁的技能
            old_skills = set(s["id"] for s in self.get_unlockable_skills(old_level))
            new_skills = set(s["id"] for s in self.get_unlockable_skills(new_level))
            unlocked_skill_ids = new_skills - old_skills
            
            unlocked_skills = [
                s for s in self.skill_tree.get("skills", [])
                if s["id"] in unlocked_skill_ids
            ]
            
            return {
                "old_level": old_level,
                "new_level": new_level,
                "old_title": self.get_title(old_level),
                "new_title": self.get_title(new_level),
                "unlocked_skills": unlocked_skills,
                "title_changed": self.get_title(old_level) != self.get_title(new_level)
            }
        
        return None
    
    def add_experience(self, current_exp: int, exp_gained: int) -> Dict[str, Any]:
        """
        添加经验
        
        Args:
            current_exp: 当前经验
            exp_gained: 获得的经验
            
        Returns:
            {new_exp, level_up_info}
        """
        new_exp = current_exp + exp_gained
        level_up_info = self.check_level_up(current_exp, new_exp)
        
        return {
            "old_exp": current_exp,
            "new_exp": new_exp,
            "exp_gained": exp_gained,
            "level_up_info": level_up_info
        }


# 全局进度系统实例
progression_system = ProgressionSystem()


def get_progression_system() -> ProgressionSystem:
    """获取进度系统实例"""
    return progression_system
