"""
LangChain 服務器
將 LangChain 組件暴露為 A2A 服務器
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from python_a2a import run_server
from python_a2a.langchain import to_a2a_server
from config import Config

class LangChainServer:
    """LangChain 服務器類"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.server = None
        self._setup_chain()
    
    def _setup_chain(self):
        """設置 LangChain 鏈"""
        # 創建 LLM
        llm = ChatOpenAI(
            api_key=self.api_key,
            model=Config.DEFAULT_MODEL,
            temperature=Config.DEFAULT_TEMPERATURE
        )
        
        # 創建提示模板
        prompt = PromptTemplate.from_template(
            "你是一個友善且知識豐富的助手。"
            "請用繁體中文回答以下問題，答案要準確且有幫助。\n\n"
            "問題: {question}\n"
            "回答:"
        )
        
        # 創建處理鏈
        self.chain = prompt | llm | StrOutputParser()
        
        # 轉換為 A2A 服務器
        self.server = to_a2a_server(self.chain)
    
    def start(self, port: int):
        """啟動服務器"""
        if self.server:
            run_server(self.server, host=Config.DEFAULT_HOST, port=port)
        else:
            raise RuntimeError("服務器未初始化")

def create_langchain_server(api_key: str) -> LangChainServer:
    """創建 LangChain 服務器實例"""
    return LangChainServer(api_key)

def start_langchain_server(port: int):
    """啟動 LangChain 服務器的便捷函數"""
    Config.validate()
    server = create_langchain_server(Config.OPENAI_API_KEY)
    server.start(port)