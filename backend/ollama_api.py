"""
Ollama 本地模型 API 封装
使用 qwen:7b 模型
"""
import requests
import json
from typing import Optional

# Ollama API 配置
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen:7b"


class OllamaClient:
    """Ollama 本地模型客户端"""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url
        self.model = model
        self.generate_url = f"{base_url}/api/generate"
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """
        调用 Ollama 生成文本
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大生成 token 数
            
        Returns:
            生成的文本
        """
        # 构建完整提示
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = requests.post(
                self.generate_url,
                json=payload,
                timeout=120,
                proxies={"http": None, "https": None}
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.ConnectionError:
            return "[错误] 无法连接到 Ollama 服务，请确保 Ollama 正在运行 (ollama serve)"
        except requests.exceptions.Timeout:
            return "[错误] Ollama 响应超时，请稍后重试"
        except Exception as e:
            return f"[错误] Ollama 调用失败: {str(e)}"
    
    def generate_story(self, level: int, stage: int, context: str = "") -> str:
        """
        生成游戏剧情
        
        Args:
            level: 当前关卡
            stage: 当前阶段
            context: 上下文信息
        """
        level_names = {
            1: "业务需求分析",
            2: "质量属性识别",
            3: "架构风格与组件设计",
            4: "架构评估（ATAM）"
        }
        
        system_prompt = """你是一位资深的 CTO，名叫"老王"，在一家科技公司担任技术总监。
你正在指导一位新入职的架构师学习 ABSD（基于架构的软件开发）方法。
你的风格是：专业但友善，喜欢用实际案例来讲解，偶尔会开个玩笑。
请用中文回复，保持对话自然流畅。"""
        
        level_name = level_names.get(level, "未知关卡")
        
        prompt = f"""当前场景：第 {level} 关 - {level_name}，阶段 {stage}
{context}

请生成一段简短的剧情对话（100-200字），引导玩家进入当前关卡的学习。
包含：
1. 场景描述
2. CTO 老王的开场白
3. 给玩家的任务提示

直接输出剧情内容，不要有多余的解释。"""
        
        return self.generate(prompt, system_prompt, temperature=0.8)
    
    def generate_quest(self, level: int, quest_info: dict) -> str:
        """
        生成任务描述
        
        Args:
            level: 当前关卡
            quest_info: 任务信息
        """
        system_prompt = """你是 CTO 老王，正在给架构师出题考核。
请根据任务信息，生成一个具体的架构设计问题。
问题要贴近实际工作场景，有一定难度但不要太复杂。"""
        
        prompt = f"""任务信息：
关卡：{level}
任务名称：{quest_info.get('name', '未知任务')}
任务描述：{quest_info.get('description', '')}
考核要点：{quest_info.get('key_points', [])}

请生成一个具体的问题场景，让玩家回答。问题要具体、可回答。
直接输出问题，不要有多余的解释。"""
        
        return self.generate(prompt, system_prompt, temperature=0.7)
    
    def evaluate_answer(self, question: str, answer: str, key_points: list) -> dict:
        """
        评估玩家回答
        
        Args:
            question: 问题
            answer: 玩家回答
            key_points: 评分要点
            
        Returns:
            评估结果 {score, comment, pass_flag}
        """
        system_prompt = """你是 CTO 老王，正在评估架构师的回答。
请根据评分要点，给出客观公正的评价。
评分标准：
- 90-100分：优秀，完全理解并有创新
- 70-89分：良好，基本掌握核心要点
- 60-69分：及格，有一定理解但不够深入
- 60分以下：不及格，需要继续学习

请严格按照 JSON 格式输出，不要有其他内容。"""
        
        prompt = f"""问题：{question}

玩家回答：{answer}

评分要点：{key_points}

请评估这个回答，输出 JSON 格式：
{{"score": 分数(0-100), "comment": "评语(50-100字)", "pass_flag": true/false(60分以上为true)}}

只输出 JSON，不要有其他内容。"""
        
        response = self.generate(prompt, system_prompt, temperature=0.3)
        
        # 解析 JSON
        try:
            # 尝试提取 JSON
            import re
            json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    "score": int(result.get("score", 0)),
                    "comment": result.get("comment", "评估完成"),
                    "pass_flag": result.get("pass_flag", False)
                }
        except (json.JSONDecodeError, ValueError):
            pass
        
        # 解析失败，返回默认值
        return {
            "score": 60,
            "comment": response[:200] if response else "评估完成，请继续努力！",
            "pass_flag": True
        }
    
    def generate_advice(self, score: int, level: int, answer: str) -> str:
        """
        生成改进建议
        
        Args:
            score: 得分
            level: 当前关卡
            answer: 玩家回答
        """
        system_prompt = """你是 CTO 老王，正在给架构师提供改进建议。
请根据得分和回答，给出具体的学习建议。
建议要具体、可操作，不要太长。"""
        
        prompt = f"""玩家在第 {level} 关获得了 {score} 分。
玩家的回答：{answer[:500]}

请给出 2-3 条具体的改进建议，帮助玩家提升架构能力。
直接输出建议，不要有多余的解释。"""
        
        return self.generate(prompt, system_prompt, temperature=0.7)
    
    def check_level_pass(self, total_score: int, level: int) -> dict:
        """
        判断是否通关
        
        Args:
            total_score: 总分
            level: 当前关卡
            
        Returns:
            {passed: bool, message: str}
        """
        pass_threshold = 60
        passed = total_score >= pass_threshold
        
        if passed:
            system_prompt = "你是 CTO 老王，玩家通过了考核，请给予鼓励。"
            prompt = f"玩家在第 {level} 关获得了 {total_score} 分，成功通关！请给一段简短的祝贺语（50字以内）。"
        else:
            system_prompt = "你是 CTO 老王，玩家未通过考核，请给予鼓励和建议。"
            prompt = f"玩家在第 {level} 关获得了 {total_score} 分，未能通关。请给一段简短的鼓励语（50字以内）。"
        
        message = self.generate(prompt, system_prompt, temperature=0.8)
        
        return {
            "passed": passed,
            "message": message,
            "score": total_score
        }


# 全局客户端实例
ollama_client = OllamaClient()


def get_ollama_client() -> OllamaClient:
    """获取 Ollama 客户端实例"""
    return ollama_client
