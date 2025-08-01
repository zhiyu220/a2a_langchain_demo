"""
計算器工具
提供安全的數學計算功能
"""
from langchain.tools import Tool
from typing import Any

class CalculatorTool:
    """安全的計算器工具"""
    
    def __init__(self):
        self.name = "calculator"
        self.description = "安全地計算數學表達式，支援基本算術運算"
    
    def calculate(self, expression: str) -> str:
        """執行計算"""
        try:
            # 安全檢查：只允許數字和基本運算符
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                return "錯誤: 表達式包含不允許的字符。只允許數字、+、-、*、/、()、和空格。"
            
            # 長度檢查
            if len(expression) > 200:
                return "錯誤: 表達式過長（最多200個字符）"
            
            # 括號匹配檢查
            if expression.count('(') != expression.count(')'):
                return "錯誤: 括號不匹配"
            
            # 執行計算
            result = eval(expression)
            
            # 處理特殊結果
            if isinstance(result, complex):
                return f"計算結果: {expression} = {result.real} + {result.imag}i"
            elif isinstance(result, float):
                # 保留合理的小數位數
                if result.is_integer():
                    return f"計算結果: {expression} = {int(result)}"
                else:
                    return f"計算結果: {expression} = {result:.6f}".rstrip('0').rstrip('.')
            else:
                return f"計算結果: {expression} = {result}"
                
        except ZeroDivisionError:
            return "錯誤: 除零錯誤"
        except OverflowError:
            return "錯誤: 數值過大"
        except ValueError as e:
            return f"錯誤: 數值錯誤 - {e}"
        except SyntaxError:
            return "錯誤: 表達式語法錯誤"
        except Exception as e:
            return f"計算錯誤: {str(e)}"
    
    def get_langchain_tool(self) -> Tool:
        """獲取 LangChain 工具對象"""
        return Tool(
            name=self.name,
            description=self.description,
            func=self.calculate
        )

class ScientificCalculator:
    """科學計算器工具"""
    
    def __init__(self):
        self.name = "scientific_calculator"
        self.description = "科學計算器，支援三角函數、對數、指數等高級數學函數"
    
    def calculate(self, expression: str) -> str:
        """執行科學計算"""
        import math
        
        try:
            # 創建安全的計算環境
            safe_dict = {
                # 基本運算
                '__builtins__': {},
                # 數學常數
                'pi': math.pi,
                'e': math.e,
                # 基本函數
                'abs': abs,
                'round': round,
                'min': min,
                'max': max,
                # 三角函數
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                # 指數和對數
                'exp': math.exp,
                'log': math.log,
                'log10': math.log10,
                'sqrt': math.sqrt,
                'pow': pow,
                # 其他函數
                'ceil': math.ceil,
                'floor': math.floor,
                'degrees': math.degrees,
                'radians': math.radians,
            }
            
            # 長度檢查
            if len(expression) > 300:
                return "錯誤: 表達式過長"
            
            # 執行計算
            result = eval(expression, safe_dict)
            
            # 格式化結果
            if isinstance(result, float):
                if result.is_integer():
                    return f"科學計算結果: {expression} = {int(result)}"
                else:
                    return f"科學計算結果: {expression} = {result:.8f}".rstrip('0').rstrip('.')
            else:
                return f"科學計算結果: {expression} = {result}"
                
        except ZeroDivisionError:
            return "錯誤: 除零錯誤"
        except ValueError as e:
            return f"錯誤: 數值錯誤 - {e}"
        except OverflowError:
            return "錯誤: 數值過大"
        except Exception as e:
            return f"科學計算錯誤: {str(e)}"
    
    def get_langchain_tool(self) -> Tool:
        """獲取 LangChain 工具對象"""
        return Tool(
            name=self.name,
            description=self.description,
            func=self.calculate
        )

# 便捷函數
def create_calculator() -> CalculatorTool:
    """創建基本計算器"""
    return CalculatorTool()

def create_scientific_calculator() -> ScientificCalculator:
    """創建科學計算器"""
    return ScientificCalculator()