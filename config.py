"""
配置文件
包含所有配置選項和環境變數處理
"""
import os
import sys

class Config:
    """應用程式配置類"""
    
    # API 配置
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    
    # 服務器配置
    DEFAULT_HOST = "localhost"
    BASE_PORT = 8000
    PORT_RANGE = 100
    
    # 模型配置
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_TEMPERATURE = 0.7
    
    # 超時配置
    SERVER_START_TIMEOUT = 3
    REQUEST_TIMEOUT = 30
    
    @classmethod
    def validate(cls):
        """驗證配置"""
        if not cls.OPENAI_API_KEY:
            print("❌ 需要設置 OPENAI_API_KEY 環境變數")
            print("請執行: export OPENAI_API_KEY=your_api_key")
            sys.exit(1)
        return True
    
    @classmethod
    def get_server_ports(cls):
        """獲取服務器端口配置"""
        return {
            'langchain_server': cls.BASE_PORT,
            'a2a_agent': cls.BASE_PORT + 1,
            'mcp_server': cls.BASE_PORT + 2,
            'simple_mcp': cls.BASE_PORT + 3
        }