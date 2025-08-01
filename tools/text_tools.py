"""
文本處理工具
提供各種文本分析和處理功能
"""
from langchain.tools import Tool
import re
from collections import Counter

class TextLengthTool:
    """文本長度計算工具"""
    
    def __init__(self):
        self.name = "text_length"
        self.description = "計算文本的字符長度"
    
    def calculate_length(self, text: str) -> str:
        """計算文本長度"""
        try:
            length = len(text)
            return f"文本長度: {length} 個字符"
        except Exception as e:
            return f"錯誤: {e}"
    
    def get_langchain_tool(self) -> Tool:
        """獲取 LangChain 工具對象"""
        return Tool(
            name=self.name,
            description=self.description,
            func=self.calculate_length
        )

class TextCountTool:
    """文本統計工具"""
    
    def __init__(self):
        self.name = "text_counter"
        self.description = "統計文本中的單詞、行數等資訊"
    
    def count_text(self, text: str) -> str:
        """統計文本"""
        try:
            lines = text.split('\n')
            words = text.split()
            characters = len(text)
            
            # 統計不同類型的字符
            letters = sum(c.isalpha() for c in text)
            digits = sum(c.isdigit() for c in text)
            spaces = sum(c.isspace() for c in text)
            
            result = f"""文本統計結果:
📊 基本統計:
- 總字符數: {characters}
- 單詞數: {len(words)}
- 行數: {len(lines)}

🔤 字符分類:
- 字母: {letters}
- 數字: {digits}
- 空格和換行: {spaces}
- 標點符號: {characters - letters - digits - spaces}"""
            
            return result
        except Exception as e:
            return f"統計錯誤: {e}"
    
    def get_langchain_tool(self) -> Tool:
        """獲取 LangChain 工具對象"""
        return Tool(
            name=self.name,
            description=self.description,
            func=self.count_text
        )

class TextAnalyzerTool:
    """文本分析工具"""
    
    def __init__(self):
        self.name = "text_analyzer"
        self.description = "深度分析文本內容，包括頻率統計、語言特徵等"
    
    def analyze_text(self, text: str) -> str:
        """分析文本"""
        try:
            # 基本統計
            char_count = len(text)
            word_count = len(text.split())
            line_count = len(text.split('\n'))
            
            # 單詞頻率分析
            words = re.findall(r'\b\w+\b', text.lower())
            word_freq = Counter(words)
            most_common = word_freq.most_common(5)
            
            # 字符頻率分析
            char_freq = Counter(text.lower())
            common_chars = [(char, count) for char, count in char_freq.most_common(5) if char.isalpha()]
            
            # 句子分析
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
            
            result = f"""📈 深度文本分析報告:

📊 基本統計:
- 字符數: {char_count}
- 單詞數: {word_count}
- 行數: {line_count}
- 句子數: {len(sentences)}
- 平均句子長度: {avg_sentence_length:.1f} 個單詞

🔤 最常見單詞:"""
            
            for word, count in most_common:
                result += f"\n- '{word}': {count} 次"
            
            result += "\n\n🔠 最常見字母:"
            for char, count in common_chars:
                result += f"\n- '{char}': {count} 次"
            
            # 語言特徵
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
            result += f"\n\n📝 語言特徵:\n- 平均單詞長度: {avg_word_length:.1f} 個字符"
            
            return result
        except Exception as e:
            return f"分析錯誤: {e}"
    
    def get_langchain_tool(self) -> Tool:
        """獲取 LangChain 工具對象"""
        return Tool(
            name=self.name,
            description=self.description,
            func=self.analyze_text
        )

class TextTransformTool:
    """文本轉換工具"""
    
    def __init__(self):
        self.name = "text_transformer"
        self.description = "轉換文本格式，包括大小寫轉換、反轉等"
    
    def transform_text(self, text: str, operation: str = "upper") -> str:
        """轉換文本"""
        try:
            operations = {
                "upper": lambda t: t.upper(),
                "lower": lambda t: t.lower(),
                "title": lambda t: t.title(),
                "reverse": lambda t: t[::-1],
                "capitalize": lambda t: t.capitalize(),
                "swapcase": lambda t: t.swapcase()
            }
            
            if operation not in operations:
                available_ops = ", ".join(operations.keys())
                return f"錯誤: 不支援的操作 '{operation}'。可用操作: {available_ops}"
            
            transformed = operations[operation](text)
            return f"轉換結果 ({operation}):\n{transformed}"
        except Exception as e:
            return f"轉換錯誤: {e}"
    
    def get_langchain_tool(self) -> Tool:
        """獲取 LangChain 工具對象"""
        return Tool(
            name=self.name,
            description=self.description,
            func=lambda text_and_op: self.transform_text(*text_and_op.split('|', 1) if '|' in text_and_op else (text_and_op, "upper"))
        )

class TextValidatorTool:
    """文本驗證工具"""
    
    def __init__(self):
        self.name = "text_validator"
        self.description = "驗證文本格式，如電子郵件、URL、電話號碼等"
    
    def validate_text(self, text: str, validation_type: str = "email") -> str:
        """驗證文本"""
        try:
            patterns = {
                "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                "url": r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$',
                "phone": r'^\+?1?-?\.?\s?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})$',
                "ip": r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
            }
            
            if validation_type not in patterns:
                available_types = ", ".join(patterns.keys())
                return f"錯誤: 不支援的驗證類型 '{validation_type}'。可用類型: {available_types}"
            
            pattern = patterns[validation_type]
            is_valid = bool(re.match(pattern, text.strip()))
            
            return f"驗證結果 ({validation_type}):\n文本: '{text}'\n結果: {'✅ 有效' if is_valid else '❌ 無效'}"
        except Exception as e:
            return f"驗證錯誤: {e}"
    
    def get_langchain_tool(self) -> Tool:
        """獲取 LangChain 工具對象"""
        return Tool(
            name=self.name,
            description=self.description,
            func=lambda text_and_type: self.validate_text(*text_and_type.split('|', 1) if '|' in text_and_type else (text_and_type, "email"))
        )

# 便捷函數
def create_text_length_tool() -> TextLengthTool:
    """創建文本長度工具"""
    return TextLengthTool()

def create_text_count_tool() -> TextCountTool:
    """創建文本統計工具"""
    return TextCountTool()

def create_text_analyzer_tool() -> TextAnalyzerTool:
    """創建文本分析工具"""
    return TextAnalyzerTool()

def create_text_transform_tool() -> TextTransformTool:
    """創建文本轉換工具"""
    return TextTransformTool()

def create_text_validator_tool() -> TextValidatorTool:
    """創建文本驗證工具"""
    return TextValidatorTool()