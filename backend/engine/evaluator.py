"""
评估器 - 负责评估玩家回答
"""
import sys
import os
from typing import Dict, Any, List

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.ollama_api import get_ollama_client


class Evaluator:
    """玩家回答评估器"""
    
    def __init__(self):
        self.ollama = get_ollama_client()
    
    def evaluate(self, question: str, answer: str, key_points: List[str]) -> Dict[str, Any]:
        """
        评估玩家回答
        
        Args:
            question: 问题
            answer: 玩家回答
            key_points: 评分要点
            
        Returns:
            评估结果 {score, comment, pass_flag}
        """
        if not answer or len(answer.strip()) < 10:
            return {
                "score": 0,
                "comment": "回答太短了，请认真思考后再回答。",
                "pass_flag": False
            }
        
        # 调用 Ollama 评估
        result = self.ollama.evaluate_answer(question, answer, key_points)
        
        return result
    
    def get_advice(self, score: int, level: int, answer: str) -> str:
        """
        获取改进建议
        
        Args:
            score: 得分
            level: 当前关卡
            answer: 玩家回答
            
        Returns:
            改进建议
        """
        return self.ollama.generate_advice(score, level, answer)
    
    def check_pass(self, total_score: int, level: int) -> Dict[str, Any]:
        """
        检查是否通关
        
        Args:
            total_score: 总分
            level: 当前关卡
            
        Returns:
            {passed, message, score}
        """
        return self.ollama.check_level_pass(total_score, level)
    
    def calculate_stage_score(self, scores: List[int]) -> int:
        """
        计算阶段总分
        
        Args:
            scores: 各题得分列表
            
        Returns:
            平均分
        """
        if not scores:
            return 0
        return int(sum(scores) / len(scores))


# 全局评估器实例
evaluator = Evaluator()


def get_evaluator() -> Evaluator:
    """获取评估器实例"""
    return evaluator
