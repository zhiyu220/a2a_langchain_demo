"""
A2A 代理服務器
創建專門的 A2A 代理
"""
from python_a2a import OpenAIA2AServer, AgentCard, AgentSkill, run_server
from config import Config

class MathExpertAgent:
    """數學專家代理"""
    
    def __init__(self, api_key: str, port: int):
        self.api_key = api_key
        self.port = port
        self._setup_agent()
    
    def _setup_agent(self):
        """設置代理"""
        # 創建代理卡片
        self.agent_card = AgentCard(
            name="數學專家",
            description="專門解決數學問題的智能代理，能夠解答各種數學相關疑問",
            url=f"http://{Config.DEFAULT_HOST}:{self.port}",
            version="1.0.0",
            skills=[
                AgentSkill(
                    name="基礎數學",
                    description="處理基礎數學計算和概念解釋",
                    examples=["2+2等於多少？", "什麼是質數？"]
                ),
                AgentSkill(
                    name="高等數學",
                    description="解答微積分、線性代數等高等數學問題",
                    examples=["解釋微分的概念", "什麼是線性變換？"]
                ),
                AgentSkill(
                    name="應用數學",
                    description="解決實際問題中的數學應用",
                    examples=["計算圓的面積", "統計學在生活中的應用"]
                )
            ]
        )
        
        # 創建 OpenAI 驅動的 A2A 服務器
        self.server = OpenAIA2AServer(
            api_key=self.api_key,
            model=Config.DEFAULT_MODEL,
            temperature=0.1,  # 數學問題需要更精確的答案
            system_prompt=(
                "你是一位專業的數學專家。你的職責是："
                "1. 提供準確的數學計算和解答"
                "2. 用清晰易懂的語言解釋數學概念"
                "3. 在適當時候提供計算步驟"
                "4. 使用繁體中文回答"
                "5. 如果問題不是數學相關，請禮貌地說明你專精於數學領域"
            )
        )
    
    def start(self, port: int):
        """啟動代理服務器"""
        run_server(self.server, host=Config.DEFAULT_HOST, port=port)

class GeographyExpertAgent:
    """地理專家代理"""
    
    def __init__(self, api_key: str, port: int):
        self.api_key = api_key
        self.port = port
        self._setup_agent()
    
    def _setup_agent(self):
        """設置地理專家代理"""
        self.agent_card = AgentCard(
            name="地理專家",
            description="專門提供地理和旅遊資訊的智能代理",
            url=f"http://{Config.DEFAULT_HOST}:{self.port}",
            version="1.0.0",
            skills=[
                AgentSkill(
                    name="地理知識",
                    description="回答關於國家、首都、地形等地理問題",
                    examples=["法國的首都是什麼？", "喜馬拉雅山在哪裡？"]
                ),
                AgentSkill(
                    name="旅遊資訊",
                    description="提供旅遊目的地和景點資訊",
                    examples=["巴黎有什麼著名景點？", "日本最佳旅遊季節是什麼時候？"]
                )
            ]
        )
        
        self.server = OpenAIA2AServer(
            api_key=self.api_key,
            model=Config.DEFAULT_MODEL,
            temperature=0.3,
            system_prompt=(
                "你是一位地理和旅遊專家。你的專長包括："
                "1. 提供準確的地理資訊"
                "2. 推薦旅遊景點和路線"
                "3. 解答文化和歷史相關問題"
                "4. 使用繁體中文回答"
                "5. 提供實用的旅遊建議"
            )
        )
    
    def start(self, port: int):
        """啟動代理服務器"""
        run_server(self.server, host=Config.DEFAULT_HOST, port=port)

def create_math_agent(api_key: str, port: int) -> MathExpertAgent:
    """創建數學專家代理"""
    return MathExpertAgent(api_key, port)

def create_geography_agent(api_key: str, port: int) -> GeographyExpertAgent:
    """創建地理專家代理"""
    return GeographyExpertAgent(api_key, port)

def start_math_agent(port: int):
    """啟動數學專家代理的便捷函數"""
    Config.validate()
    agent = create_math_agent(Config.OPENAI_API_KEY, port)
    agent.start(port)

def start_geography_agent(port: int):
    """啟動地理專家代理的便捷函數"""
    Config.validate()
    agent = create_geography_agent(Config.OPENAI_API_KEY, port)
    agent.start(port)