"""
MCP 服務器
創建和管理 MCP (Model Context Protocol) 服務器
"""
from python_a2a.mcp import FastMCP, text_response
from python_a2a.langchain import to_mcp_server
from tools.calculator import CalculatorTool
from tools.text_tools import TextLengthTool, TextCountTool
from config import Config

class SimpleMCPServer:
    """簡單的 MCP 服務器"""
    
    def __init__(self):
        self.server = FastMCP(
            name="基本工具集",
            description="提供基本實用工具的 MCP 服務器"
        )
        self._register_tools()
    
    def _register_tools(self):
        """註冊工具"""
        
        @self.server.tool(
            name="text_length",
            description="計算文本的字符長度"
        )
        def text_length(text: str):
            """計算文本長度工具"""
            try:
                length = len(text)
                return text_response(f"文本 '{text[:50]}...' 的長度是 {length} 個字符")
            except Exception as e:
                return text_response(f"錯誤: {e}")
        
        @self.server.tool(
            name="word_count",
            description="計算文本的單詞數量"
        )
        def word_count(text: str):
            """計算單詞數量工具"""
            try:
                words = text.split()
                word_count = len(words)
                return text_response(f"文本包含 {word_count} 個單詞")
            except Exception as e:
                return text_response(f"錯誤: {e}")
        
        @self.server.tool(
            name="text_reverser",
            description="反轉文本內容"
        )
        def text_reverser(text: str):
            """文本反轉工具"""
            try:
                reversed_text = text[::-1]
                return text_response(f"反轉後的文本: {reversed_text}")
            except Exception as e:
                return text_response(f"錯誤: {e}")
        
        @self.server.tool(
            name="text_upper",
            description="將文本轉換為大寫"
        )
        def text_upper(text: str):
            """文本轉大寫工具"""
            try:
                upper_text = text.upper()
                return text_response(f"大寫文本: {upper_text}")
            except Exception as e:
                return text_response(f"錯誤: {e}")
    
    def start(self, port: int):
        """啟動 MCP 服務器"""
        self.server.run(host=Config.DEFAULT_HOST, port=port)

class LangChainMCPServer:
    """基於 LangChain 工具的 MCP 服務器"""
    
    def __init__(self):
        self.tools = []
        self._setup_tools()
        self.server = to_mcp_server(self.tools)
    
    def _setup_tools(self):
        """設置 LangChain 工具"""
        # 添加計算器工具
        calculator = CalculatorTool()
        self.tools.append(calculator.get_langchain_tool())
        
        # 添加文本工具
        text_length_tool = TextLengthTool()
        self.tools.append(text_length_tool.get_langchain_tool())
        
        text_count_tool = TextCountTool()
        self.tools.append(text_count_tool.get_langchain_tool())
    
    def start(self, port: int):
        """啟動服務器"""
        self.server.run(host=Config.DEFAULT_HOST, port=port)

class AdvancedMCPServer:
    """進階 MCP 服務器"""
    
    def __init__(self):
        self.server = FastMCP(
            name="進階工具集",
            description="提供進階分析和處理工具"
        )
        self._register_advanced_tools()
    
    def _register_advanced_tools(self):
        """註冊進階工具"""
        
        @self.server.tool(
            name="text_analyzer",
            description="分析文本的詳細統計資訊"
        )
        def text_analyzer(text: str):
            """文本分析工具"""
            try:
                char_count = len(text)
                word_count = len(text.split())
                line_count = len(text.split('\n'))
                
                # 字符統計
                letters = sum(c.isalpha() for c in text)
                digits = sum(c.isdigit() for c in text)
                spaces = sum(c.isspace() for c in text)
                
                analysis = f"""文本分析結果:
📊 基本統計:
   - 總字符數: {char_count}
   - 單詞數: {word_count}
   - 行數: {line_count}

🔤 字符分類:
   - 字母: {letters}
   - 數字: {digits}
   - 空格: {spaces}
   - 其他: {char_count - letters - digits - spaces}"""
                
                return text_response(analysis)
            except Exception as e:
                return text_response(f"分析錯誤: {e}")
        
        @self.server.tool(
            name="math_evaluator",
            description="安全地計算數學表達式"
        )
        def math_evaluator(expression: str):
            """數學表達式求值工具"""
            try:
                # 安全檢查
                allowed_chars = set('0123456789+-*/(). ')
                if not all(c in allowed_chars for c in expression):
                    return text_response("錯誤: 表達式包含不允許的字符")
                
                # 避免過於複雜的表達式
                if len(expression) > 100:
                    return text_response("錯誤: 表達式過長")
                
                result = eval(expression)
                return text_response(f"計算結果: {expression} = {result}")
            except ZeroDivisionError:
                return text_response("錯誤: 除零錯誤")
            except Exception as e:
                return text_response(f"計算錯誤: {e}")
    
    def start(self, port: int):
        """啟動進階 MCP 服務器"""
        self.server.run(host=Config.DEFAULT_HOST, port=port)

def create_simple_mcp_server() -> SimpleMCPServer:
    """創建簡單 MCP 服務器"""
    return SimpleMCPServer()

def create_langchain_mcp_server() -> LangChainMCPServer:
    """創建基於 LangChain 的 MCP 服務器"""
    return LangChainMCPServer()

def create_advanced_mcp_server() -> AdvancedMCPServer:
    """創建進階 MCP 服務器"""
    return AdvancedMCPServer()

def start_simple_mcp_server(port: int):
    """啟動簡單 MCP 服務器的便捷函數"""
    server = create_simple_mcp_server()
    server.start(port)

def start_langchain_mcp_server(port: int):
    """啟動 LangChain MCP 服務器的便捷函數"""
    server = create_langchain_mcp_server()
    server.start(port)

def start_advanced_mcp_server(port: int):
    """啟動進階 MCP 服務器的便捷函數"""
    server = create_advanced_mcp_server()
    server.start(port)