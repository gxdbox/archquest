"""
Architecture RPG - Streamlit 前端
🎮 RPG 架构师养成游戏
"""
import streamlit as st
import requests
import json
from typing import Optional, Dict, Any

# API 配置
API_BASE_URL = "http://localhost:8000"

# 页面配置
st.set_page_config(
    page_title="🎮 Architecture RPG",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS
st.markdown("""
<style>
    /* 主题颜色 */
    :root {
        --primary-color: #4CAF50;
        --secondary-color: #2196F3;
        --accent-color: #FF9800;
        --bg-dark: #1a1a2e;
        --bg-light: #16213e;
    }
    
    /* 对话框样式 */
    .dialog-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #4CAF50;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .npc-dialog {
        background: linear-gradient(135deg, #2d2d44 0%, #1a1a2e 100%);
        border-left: 4px solid #FF9800;
        padding: 15px 20px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    
    .player-dialog {
        background: linear-gradient(135deg, #1e3a5f 0%, #16213e 100%);
        border-left: 4px solid #2196F3;
        padding: 15px 20px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    
    /* 状态栏 */
    .status-bar {
        background: linear-gradient(90deg, #4CAF50 0%, #2196F3 100%);
        border-radius: 10px;
        padding: 10px 20px;
        color: white;
        font-weight: bold;
    }
    
    /* 技能卡片 */
    .skill-card {
        background: #2d2d44;
        border: 1px solid #4CAF50;
        border-radius: 10px;
        padding: 15px;
        margin: 5px;
        text-align: center;
    }
    
    .skill-locked {
        opacity: 0.5;
        border-color: #666;
    }
    
    /* 进度条 */
    .progress-container {
        background: #333;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%);
        height: 100%;
        transition: width 0.5s ease;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
    }
    
    /* 标题样式 */
    h1 {
        color: #4CAF50;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2, h3 {
        color: #2196F3;
    }
    
    /* 评分显示 */
    .score-display {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
    }
    
    .score-excellent { color: #4CAF50; }
    .score-good { color: #8BC34A; }
    .score-pass { color: #FF9800; }
    .score-fail { color: #f44336; }
</style>
""", unsafe_allow_html=True)


# ==================== API 调用函数 ====================

def api_call(endpoint: str, method: str = "GET", data: dict = None) -> Optional[Dict]:
    """调用后端 API"""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        proxies = {"http": None, "https": None}
        if method == "GET":
            response = requests.get(url, timeout=30, proxies=proxies)
        else:
            response = requests.post(url, json=data, timeout=120, proxies=proxies)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API 错误: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ 无法连接到后端服务，请确保 FastAPI 服务正在运行")
        return None
    except Exception as e:
        st.error(f"请求失败: {str(e)}")
        return None


def create_player(username: str, avatar: str = "🧑‍💻") -> Optional[Dict]:
    """创建玩家"""
    return api_call("create_player", "POST", {"username": username, "avatar": avatar})


def get_all_users() -> Optional[Dict]:
    """获取所有用户列表"""
    return api_call("get_users", "GET")


def get_story(user_id: int, level: int = None, stage: int = None) -> Optional[Dict]:
    """获取剧情"""
    data = {"user_id": user_id}
    if level:
        data["level"] = level
    if stage:
        data["stage"] = stage
    return api_call("get_story", "POST", data)


def submit_answer(user_id: int, answer: str) -> Optional[Dict]:
    """提交回答"""
    return api_call("submit_answer", "POST", {"user_id": user_id, "answer": answer})


def get_progress(user_id: int) -> Optional[Dict]:
    """获取进度"""
    return api_call(f"get_progress/{user_id}", "GET")


def get_skills(user_id: int) -> Optional[Dict]:
    """获取技能"""
    return api_call(f"get_skills/{user_id}", "GET")


def check_health() -> bool:
    """检查后端健康状态"""
    result = api_call("health", "GET")
    return result is not None


# ==================== UI 组件 ====================

def render_header():
    """渲染页面头部"""
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1>🎮 Architecture RPG</h1>
            <p style="color: #888; font-size: 18px;">RPG 架构师养成 - 成为首席架构师的冒险之旅</p>
        </div>
        """, unsafe_allow_html=True)


def render_player_status(progress: Dict):
    """渲染玩家状态栏"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background: #2d2d44; border-radius: 10px;">
            <div style="font-size: 40px;">{progress.get('avatar', '🧑‍💻')}</div>
            <div style="font-weight: bold; color: #4CAF50;">{progress.get('username', '玩家')}</div>
            <div style="color: #FF9800;">{progress.get('title', '初级架构师')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        exp_progress = progress.get('exp_progress', {})
        progress_percent = exp_progress.get('progress_percent', 0)
        st.markdown(f"""
        <div style="padding: 10px; background: #2d2d44; border-radius: 10px;">
            <div style="color: #888;">等级 LV.{progress.get('player_level', 1)}</div>
            <div style="background: #333; border-radius: 5px; height: 20px; margin: 5px 0;">
                <div style="background: linear-gradient(90deg, #4CAF50, #8BC34A); width: {progress_percent}%; height: 100%; border-radius: 5px;"></div>
            </div>
            <div style="color: #888; font-size: 12px;">EXP: {progress.get('experience', 0)} / {exp_progress.get('next_level_exp', 100)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        game_progress = progress.get('game_progress_percent', 0)
        st.markdown(f"""
        <div style="padding: 10px; background: #2d2d44; border-radius: 10px;">
            <div style="color: #888;">游戏进度</div>
            <div style="font-size: 24px; font-weight: bold; color: #2196F3;">{game_progress:.1f}%</div>
            <div style="color: #888; font-size: 12px;">第 {progress.get('current_level', 1)} 关 - 阶段 {progress.get('current_stage', 1)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="padding: 10px; background: #2d2d44; border-radius: 10px;">
            <div style="color: #888;">统计</div>
            <div style="color: #4CAF50;">✅ 完成任务: {progress.get('quests_completed', 0)}</div>
            <div style="color: #FF9800;">⭐ 总分: {progress.get('total_score', 0)}</div>
        </div>
        """, unsafe_allow_html=True)


def render_npc_dialog(text: str, npc_name: str = "CTO 老王"):
    """渲染 NPC 对话框"""
    st.markdown(f"""
    <div class="npc-dialog">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 30px; margin-right: 10px;">👨‍💼</span>
            <span style="font-weight: bold; color: #FF9800;">{npc_name}</span>
        </div>
        <div style="color: #ddd; line-height: 1.8;">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_quest_box(quest: str, key_points: list):
    """渲染任务框"""
    points_html = "".join([f"<li>{p}</li>" for p in key_points])
    st.markdown(f"""
    <div class="dialog-box">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <span style="font-size: 24px; margin-right: 10px;">📋</span>
            <span style="font-weight: bold; color: #4CAF50; font-size: 18px;">当前任务</span>
        </div>
        <div style="color: #ddd; line-height: 1.8; margin-bottom: 15px;">{quest}</div>
        <div style="border-top: 1px solid #444; padding-top: 10px;">
            <div style="color: #888; margin-bottom: 5px;">💡 评分要点：</div>
            <ul style="color: #aaa; margin: 0; padding-left: 20px;">{points_html}</ul>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_score_result(result: Dict):
    """渲染评分结果"""
    score = result.get('score', 0)
    
    if score >= 90:
        score_class = "score-excellent"
        emoji = "🌟"
        grade = "优秀"
    elif score >= 70:
        score_class = "score-good"
        emoji = "👍"
        grade = "良好"
    elif score >= 60:
        score_class = "score-pass"
        emoji = "✅"
        grade = "及格"
    else:
        score_class = "score-fail"
        emoji = "💪"
        grade = "继续努力"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: #2d2d44; border-radius: 15px; margin: 20px 0;">
        <div style="font-size: 60px;">{emoji}</div>
        <div class="score-display {score_class}">{score} 分</div>
        <div style="font-size: 24px; color: #888;">{grade}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 评语
    st.markdown(f"""
    <div class="npc-dialog">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 30px; margin-right: 10px;">👨‍💼</span>
            <span style="font-weight: bold; color: #FF9800;">CTO 老王的评价</span>
        </div>
        <div style="color: #ddd; line-height: 1.8;">{result.get('comment', '')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 建议
    if result.get('advice'):
        st.markdown(f"""
        <div style="background: #1e3a5f; border-left: 4px solid #2196F3; padding: 15px 20px; margin: 10px 0; border-radius: 0 10px 10px 0;">
            <div style="font-weight: bold; color: #2196F3; margin-bottom: 10px;">💡 改进建议</div>
            <div style="color: #ddd; line-height: 1.8;">{result.get('advice', '')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 经验获得
    exp_gained = result.get('exp_gained', 0)
    st.success(f"🎉 获得经验值: +{exp_gained} EXP")
    
    # 升级信息
    level_up = result.get('level_up_info')
    if level_up:
        st.balloons()
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #4CAF50, #8BC34A); border-radius: 15px; margin: 20px 0;">
            <div style="font-size: 40px;">🎊</div>
            <div style="font-size: 24px; font-weight: bold; color: white;">升级了！</div>
            <div style="color: white;">LV.{level_up.get('old_level')} → LV.{level_up.get('new_level')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if level_up.get('title_changed'):
            st.info(f"🏆 获得新称号: {level_up.get('new_title')}")
        
        for skill in level_up.get('unlocked_skills', []):
            st.success(f"🔓 解锁新技能: {skill.get('name')}")


def render_skill_tree(skills: list, player_level: int):
    """渲染技能树"""
    st.markdown("### 🌳 技能树")
    
    cols = st.columns(4)
    for i, skill in enumerate(skills):
        with cols[i % 4]:
            unlocked = skill.get('unlocked', False)
            can_unlock = skill.get('can_unlock', False)
            
            if unlocked:
                border_color = "#4CAF50"
                opacity = 1
                status = f"LV.{skill.get('current_level', 1)}"
            elif can_unlock:
                border_color = "#FF9800"
                opacity = 0.7
                status = "可解锁"
            else:
                border_color = "#666"
                opacity = 0.4
                status = f"需要 LV.{skill.get('unlock_level', 1)}"
            
            st.markdown(f"""
            <div style="background: #2d2d44; border: 2px solid {border_color}; border-radius: 10px; 
                        padding: 15px; margin: 5px 0; text-align: center; opacity: {opacity};">
                <div style="font-size: 24px;">{'⭐' if unlocked else '🔒'}</div>
                <div style="font-weight: bold; color: #ddd; margin: 5px 0;">{skill.get('name', '')}</div>
                <div style="font-size: 12px; color: #888;">{status}</div>
            </div>
            """, unsafe_allow_html=True)


# ==================== 页面状态管理 ====================

def init_session_state():
    """初始化会话状态"""
    # 尝试从 query params 恢复用户 ID（用于页面刷新后保持登录）
    try:
        # Streamlit 1.28+ 使用 st.query_params，旧版本使用 st.experimental_get_query_params
        if hasattr(st, 'query_params'):
            query_params = st.query_params
        else:
            query_params = st.experimental_get_query_params()
        
        if 'user_id' not in st.session_state:
            # 尝试从 URL 参数恢复
            if 'user_id' in query_params:
                try:
                    user_id_param = query_params['user_id']
                    if isinstance(user_id_param, list):
                        user_id_param = user_id_param[0]
                    st.session_state.user_id = int(user_id_param)
                except:
                    st.session_state.user_id = None
            else:
                st.session_state.user_id = None
        
        # 如果有 user_id，更新 URL 参数
        if st.session_state.user_id:
            if hasattr(st, 'query_params'):
                st.query_params['user_id'] = str(st.session_state.user_id)
            else:
                st.experimental_set_query_params(user_id=str(st.session_state.user_id))
    except:
        # 如果 query params 不可用，只使用 session_state
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
    
    if 'current_story' not in st.session_state:
        st.session_state.current_story = None
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None
    if 'game_phase' not in st.session_state:
        st.session_state.game_phase = 'login' if not st.session_state.user_id else 'story'


# ==================== 主页面 ====================

def main():
    """主函数"""
    init_session_state()
    render_header()
    
    # 侧边栏
    with st.sidebar:
        st.markdown("### 🎮 游戏菜单")
        
        # 检查后端状态
        if st.button("🔄 检查连接"):
            if check_health():
                st.success("✅ 后端服务正常")
            else:
                st.error("❌ 后端服务未连接")
        
        st.markdown("---")
        
        # 如果已登录，显示快捷操作
        if st.session_state.user_id:
            if st.button("📊 查看进度"):
                st.session_state.game_phase = 'progress'
            if st.button("🌳 技能树"):
                st.session_state.game_phase = 'skills'
            if st.button("🎯 继续冒险"):
                st.session_state.game_phase = 'story'
                st.session_state.current_story = None
            
            st.markdown("---")
            if st.button("🚪 退出登录"):
                st.session_state.user_id = None
                st.session_state.game_phase = 'login'
                # 清除 URL 参数
                try:
                    if hasattr(st, 'query_params') and 'user_id' in st.query_params:
                        del st.query_params['user_id']
                    else:
                        st.experimental_set_query_params()
                except:
                    pass
                st.rerun()
        
        st.markdown("---")
        st.markdown("""
        ### 📖 游戏说明
        
        **ABSD 四关挑战：**
        1. 🔍 业务需求分析
        2. ⭐ 质量属性识别
        3. 🏛️ 架构风格设计
        4. 📋 ATAM 评估
        
        **玩法：**
        - 与 CTO 老王对话
        - 完成架构任务
        - 获得经验升级
        - 解锁技能树
        """)
    
    # 主内容区
    if st.session_state.game_phase == 'login':
        render_login_page()
    elif st.session_state.game_phase == 'story':
        render_story_page()
    elif st.session_state.game_phase == 'answer':
        render_answer_page()
    elif st.session_state.game_phase == 'result':
        render_result_page()
    elif st.session_state.game_phase == 'progress':
        render_progress_page()
    elif st.session_state.game_phase == 'skills':
        render_skills_page()
    elif st.session_state.game_phase == 'complete':
        render_complete_page()


def render_login_page():
    """渲染登录页面"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 30px; background: #2d2d44; border-radius: 15px;">
            <div style="font-size: 60px;">🧑‍💻</div>
            <h2 style="color: #4CAF50;">开始你的架构师之旅</h2>
            <p style="color: #888;">选择已有角色或创建新角色</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # 选择登录方式
        login_mode = st.radio(
            "选择方式",
            ["选择已有角色", "创建新角色"],
            horizontal=True
        )
        
        st.markdown("")
        
        if login_mode == "选择已有角色":
            # 获取用户列表
            users_data = get_all_users()
            if users_data and users_data.get('users'):
                users = users_data['users']
                
                if users:
                    st.markdown("### 📋 选择你的角色")
                    
                    for user in users:
                        with st.container():
                            col_a, col_b, col_c = st.columns([1, 4, 2])
                            
                            with col_a:
                                st.markdown(f"<div style='font-size: 40px; text-align: center;'>{user['avatar']}</div>", unsafe_allow_html=True)
                            
                            with col_b:
                                st.markdown(f"**{user['username']}**")
                                st.caption(f"{user['title']} | LV.{user['player_level']} | 总分: {user['total_score']}")
                                st.caption(f"完成任务: {user['quests_completed']} | 创建于: {user['created_at']}")
                            
                            with col_c:
                                if st.button("选择", key=f"select_{user['id']}", use_container_width=True):
                                    st.session_state.user_id = user['id']
                                    st.session_state.game_phase = 'story'
                                    try:
                                        if hasattr(st, 'query_params'):
                                            st.query_params['user_id'] = str(user['id'])
                                        else:
                                            st.experimental_set_query_params(user_id=str(user['id']))
                                    except:
                                        pass
                                    st.success(f"欢迎回来，{user['username']}！")
                                    st.rerun()
                            
                            st.markdown("---")
                else:
                    st.info("还没有角色，请创建一个新角色")
            else:
                st.info("还没有角色，请创建一个新角色")
        
        else:  # 创建新角色
            st.markdown("### ✨ 创建新角色")
            
            # 头像选择
            avatars = ["🧑‍💻", "👨‍💻", "👩‍💻", "🧙‍♂️", "🦸‍♂️", "🦸‍♀️", "🥷", "🧑‍🎓"]
            selected_avatar = st.selectbox("选择头像", avatars, index=0)
            
            # 用户名输入
            username = st.text_input("输入你的名字", placeholder="请输入玩家名称...")
            
            if st.button("🚀 开始冒险", use_container_width=True):
                if username:
                    with st.spinner("正在创建角色..."):
                        result = create_player(username, selected_avatar)
                        if result:
                            st.session_state.user_id = result['id']
                            st.session_state.game_phase = 'story'
                            try:
                                if hasattr(st, 'query_params'):
                                    st.query_params['user_id'] = str(result['id'])
                                else:
                                    st.experimental_set_query_params(user_id=str(result['id']))
                            except:
                                pass
                            st.success(result.get('message', '欢迎！'))
                            st.rerun()
                else:
                    st.warning("请输入你的名字")


def render_story_page():
    """渲染剧情页面"""
    if not st.session_state.user_id:
        st.session_state.game_phase = 'login'
        st.rerun()
        return
    
    # 获取玩家进度
    progress = get_progress(st.session_state.user_id)
    if not progress:
        st.error("获取进度失败")
        return
    
    render_player_status(progress)
    st.markdown("---")
    
    # 获取剧情
    if not st.session_state.current_story:
        with st.spinner("CTO 老王正在思考..."):
            story = get_story(st.session_state.user_id)
            if story:
                st.session_state.current_story = story
            else:
                st.error("获取剧情失败")
                return
    
    story = st.session_state.current_story
    
    # 显示关卡信息
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; background: linear-gradient(90deg, #4CAF50, #2196F3); 
                border-radius: 10px; margin-bottom: 20px;">
        <span style="font-size: 20px; font-weight: bold; color: white;">
            第 {story.get('level', 1)} 关：{story.get('level_name', '')} - {story.get('stage_name', '')}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示剧情
    render_npc_dialog(story.get('story', ''))
    
    st.markdown("")
    
    # 显示任务
    render_quest_box(story.get('quest', ''), story.get('key_points', []))
    
    st.markdown("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✍️ 开始回答", use_container_width=True):
            st.session_state.game_phase = 'answer'
            st.rerun()


def render_answer_page():
    """渲染回答页面"""
    if not st.session_state.user_id or not st.session_state.current_story:
        st.session_state.game_phase = 'story'
        st.rerun()
        return
    
    story = st.session_state.current_story
    
    # 显示任务
    st.markdown(f"### 📋 第 {story.get('level', 1)} 关 - {story.get('stage_name', '')}")
    
    render_quest_box(story.get('quest', ''), story.get('key_points', []))
    
    st.markdown("---")
    
    # 回答输入
    st.markdown("### ✍️ 你的回答")
    answer = st.text_area(
        "请详细回答上述问题",
        height=300,
        placeholder="在这里输入你的回答...\n\n提示：\n- 尽量覆盖所有评分要点\n- 结合实际场景说明\n- 给出具体的方案或建议"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ 返回", use_container_width=True):
            st.session_state.game_phase = 'story'
            st.rerun()
    
    with col3:
        if st.button("📤 提交回答", use_container_width=True, type="primary"):
            if answer and len(answer.strip()) >= 20:
                with st.spinner("CTO 老王正在评估你的回答..."):
                    result = submit_answer(st.session_state.user_id, answer)
                    if result:
                        st.session_state.last_result = result
                        st.session_state.game_phase = 'result'
                        st.rerun()
            else:
                st.warning("回答太短了，请认真思考后再提交（至少 20 个字）")


def render_result_page():
    """渲染结果页面"""
    if not st.session_state.last_result:
        st.session_state.game_phase = 'story'
        st.rerun()
        return
    
    result = st.session_state.last_result
    
    st.markdown("### 📊 评估结果")
    
    render_score_result(result)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # 判断下一步
    if result.get('game_complete'):
        with col2:
            if st.button("🎉 查看通关成就", use_container_width=True):
                st.session_state.game_phase = 'complete'
                st.session_state.current_story = None
                st.session_state.last_result = None
                st.rerun()
    elif result.get('pass_flag'):
        next_stage = result.get('next_stage', {})
        with col2:
            if st.button(f"➡️ 进入下一关", use_container_width=True, type="primary"):
                st.session_state.game_phase = 'story'
                st.session_state.current_story = None
                st.session_state.last_result = None
                st.rerun()
    else:
        with col1:
            if st.button("🔄 重新挑战", use_container_width=True):
                st.session_state.game_phase = 'story'
                st.session_state.last_result = None
                st.rerun()
        
        with col3:
            if st.button("📊 查看进度", use_container_width=True):
                st.session_state.game_phase = 'progress'
                st.rerun()


def render_progress_page():
    """渲染进度页面"""
    if not st.session_state.user_id:
        st.session_state.game_phase = 'login'
        st.rerun()
        return
    
    progress = get_progress(st.session_state.user_id)
    if not progress:
        st.error("获取进度失败")
        return
    
    render_player_status(progress)
    
    st.markdown("---")
    st.markdown("### 📈 详细进度")
    
    # 关卡进度
    levels = [
        {"name": "业务需求分析", "icon": "📋"},
        {"name": "质量属性识别", "icon": "⭐"},
        {"name": "架构风格设计", "icon": "🏛️"},
        {"name": "ATAM 评估", "icon": "🔍"}
    ]
    
    current_level = progress.get('current_level', 1)
    current_stage = progress.get('current_stage', 1)
    
    cols = st.columns(4)
    for i, level in enumerate(levels):
        level_num = i + 1
        with cols[i]:
            if level_num < current_level:
                status = "✅ 已完成"
                color = "#4CAF50"
            elif level_num == current_level:
                status = f"🎯 进行中 ({current_stage}/3)"
                color = "#FF9800"
            else:
                status = "🔒 未解锁"
                color = "#666"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: #2d2d44; 
                        border: 2px solid {color}; border-radius: 10px;">
                <div style="font-size: 40px;">{level['icon']}</div>
                <div style="font-weight: bold; color: #ddd; margin: 10px 0;">第 {level_num} 关</div>
                <div style="color: #888; font-size: 14px;">{level['name']}</div>
                <div style="color: {color}; margin-top: 10px;">{status}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 技能预览
    skills_data = get_skills(st.session_state.user_id)
    if skills_data:
        render_skill_tree(skills_data.get('skills', []), progress.get('player_level', 1))
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 继续冒险", use_container_width=True, type="primary"):
            st.session_state.game_phase = 'story'
            st.session_state.current_story = None
            st.rerun()


def render_skills_page():
    """渲染技能页面"""
    if not st.session_state.user_id:
        st.session_state.game_phase = 'login'
        st.rerun()
        return
    
    progress = get_progress(st.session_state.user_id)
    skills_data = get_skills(st.session_state.user_id)
    
    if not progress or not skills_data:
        st.error("获取数据失败")
        return
    
    render_player_status(progress)
    
    st.markdown("---")
    st.markdown("### 🌳 技能树")
    
    skills = skills_data.get('skills', [])
    player_level = progress.get('player_level', 1)
    
    # 按类别分组显示
    categories = {"基础": [], "进阶": [], "高级": [], "专家": []}
    
    for skill in skills:
        unlock_level = skill.get('unlock_level', 1)
        if unlock_level <= 4:
            categories["基础"].append(skill)
        elif unlock_level <= 9:
            categories["进阶"].append(skill)
        elif unlock_level <= 14:
            categories["高级"].append(skill)
        else:
            categories["专家"].append(skill)
    
    for cat_name, cat_skills in categories.items():
        if cat_skills:
            st.markdown(f"#### {cat_name}技能")
            cols = st.columns(len(cat_skills))
            for i, skill in enumerate(cat_skills):
                with cols[i]:
                    unlocked = skill.get('unlocked', False)
                    can_unlock = skill.get('can_unlock', False)
                    
                    if unlocked:
                        bg_color = "linear-gradient(135deg, #4CAF50, #45a049)"
                        status_text = f"已解锁 LV.{skill.get('current_level', 1)}/{skill.get('max_level', 5)}"
                    elif can_unlock:
                        bg_color = "linear-gradient(135deg, #FF9800, #F57C00)"
                        status_text = "可解锁"
                    else:
                        bg_color = "#444"
                        status_text = f"需要 LV.{skill.get('unlock_level', 1)}"
                    
                    st.markdown(f"""
                    <div style="background: {bg_color}; border-radius: 15px; padding: 20px; 
                                text-align: center; margin: 5px 0;">
                        <div style="font-size: 30px;">{'⭐' if unlocked else '🔒'}</div>
                        <div style="font-weight: bold; color: white; margin: 10px 0;">{skill.get('name', '')}</div>
                        <div style="font-size: 12px; color: rgba(255,255,255,0.8);">{status_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 继续冒险", use_container_width=True, type="primary"):
            st.session_state.game_phase = 'story'
            st.session_state.current_story = None
            st.rerun()


def render_complete_page():
    """渲染通关页面"""
    progress = get_progress(st.session_state.user_id) if st.session_state.user_id else None
    
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <div style="font-size: 100px;">🎊</div>
        <h1 style="color: #4CAF50;">恭喜通关！</h1>
        <p style="font-size: 20px; color: #888;">你已经完成了 ABSD 四关的全部挑战！</p>
    </div>
    """, unsafe_allow_html=True)
    
    if progress:
        st.markdown(f"""
        <div style="text-align: center; padding: 30px; background: #2d2d44; border-radius: 15px; margin: 20px auto; max-width: 500px;">
            <div style="font-size: 60px;">{progress.get('avatar', '🧑‍💻')}</div>
            <h2 style="color: #FF9800;">{progress.get('title', '首席架构师')}</h2>
            <div style="color: #ddd;">{progress.get('username', '玩家')}</div>
            <div style="margin-top: 20px;">
                <div style="color: #4CAF50;">🏆 等级: LV.{progress.get('player_level', 1)}</div>
                <div style="color: #2196F3;">⭐ 总分: {progress.get('total_score', 0)}</div>
                <div style="color: #FF9800;">✅ 完成任务: {progress.get('quests_completed', 0)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="color: #888; font-size: 16px;">
            从一个初级架构师，你已经成长为能够独立完成架构设计的专业人士。<br>
            但记住，这只是开始。真正的架构能力需要在实践中不断磨练。<br>
            <strong style="color: #4CAF50;">继续加油！</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📊 查看成就", use_container_width=True):
            st.session_state.game_phase = 'progress'
            st.rerun()


if __name__ == "__main__":
    main()
