"""
Demo 2: A2A → LangChain
演示如何將 A2A 代理轉換為 LangChain 組件
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from utils import ServerManager, print_section, print_success, print_error
from servers.a2a_agent import start_math_agent, start_geography_agent
from python_a2a.langchain import to_langchain_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def test_math_agent_integration():
    """測試數學代理整合"""
    manager = ServerManager()
    
    try:
        # 啟動數學專家代理
        print_section("啟動數學專家 A2A 代理")
        port = manager.start_server("數學專家", start_math_agent)
        server_url = manager.get_server_url("數學專家")
        print_success(f"數學專家代理已啟動: {server_url}")
        
        # 轉換為 LangChain 代理
        print_section("轉換為 LangChain 代理")
        langchain_agent = to_langchain_agent(server_url)
        print_success("A2A 代理已成功轉換為 LangChain 組件")
        
        # 測試數學問題
        print_section("測試數學問題")
        math_questions = [
            "什麼是畢達哥拉斯定理？",
            "請解釋微積分的基本概念",
            "如何計算圓的面積？",
            "什麼是質數？請給出前10個質數"
        ]
        
        for question in math_questions:
            print(f"\n📐 數學問題: {question}")
            try:
                result = langchain_agent.invoke(question)
                response = result.get('output', str(result))
                print_success(f"回應: {response[:300]}...")
            except Exception as e:
                print_error(f"問題處理失敗: {e}")
        
        return langchain_agent, manager
        
    except Exception as e:
        print_error(f"數學代理測試失敗: {e}")
        manager.stop_all()
        raise

def test_geography_agent_integration():
    """測試地理代理整合"""
    manager = ServerManager()
    
    try:
        # 啟動地理專家代理
        print_section("啟動地理專家 A2A 代理")
        port = manager.start_server("地理專家", start_geography_agent)
        server_url = manager.get_server_url("地理專家")
        print_success(f"地理專家代理已啟動: {server_url}")
        
        # 轉換為 LangChain 代理
        langchain_agent = to_langchain_agent(server_url)
        print_success("地理代理已轉換為 LangChain 組件")
        
        # 測試地理問題
        geography_questions = [
            "法國的首都是什麼？",
            "世界上最高的山峰在哪裡？",
            "介紹一下日本的地理特色",
            "推薦義大利的旅遊景點"
        ]
        
        for question in geography_questions:
            print(f"\n🌍 地理問題: {question}")
            try:
                result = langchain_agent.invoke(question)
                response = result.get('output', str(result))
                print_success(f"回應: {response[:300]}...")
            except Exception as e:
                print_error(f"問題處理失敗: {e}")
        
        return langchain_agent, manager
        
    except Exception as e:
        print_error(f"地理代理測試失敗: {e}")
        manager.stop_all()
        raise

def test_langchain_workflow_integration():
    """測試在 LangChain 工作流中使用 A2A 代理"""
    print_section("LangChain 工作流整合測試")
    
    # 啟動兩個專家代理
    math_agent, math_manager = test_math_agent_integration()
    geo_agent, geo_manager = test_geography_agent_integration()
    
    try:
        # 創建主 LLM 用於協調
        llm = ChatOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model=Config.DEFAULT_MODEL,
            temperature=0.3
        )
        
        # 創建協調提示
        coordinator_prompt = ChatPromptTemplate.from_template(
            """你是一個智能協調器。根據用戶的問題，決定是否需要專家幫助。

用戶問題: {question}

如果是數學相關問題，回應 "MATH: " + 問題
如果是地理相關問題，回應 "GEO: " + 問題  
如果是一般問題，直接回答

問題類型判斷:"""
        )
        
        # 創建協調鏈
        coordinator = coordinator_prompt | llm | StrOutputParser()
        
        # 測試複合問題
        complex_questions = [
            "請計算地球的周長（假設地球是完美球體，半徑為 6371 公里）",
            "如果我要從台北飛到紐約，大約需要飛行多少公里？請計算距離",
            "法國巴黎的經緯度是多少？",
            "計算一個邊長為 5 公尺的正方形面積"
        ]
        
        print_section("複合問題處理測試")
        for question in complex_questions:
            print(f"\n🔀 複合問題: {question}")
            try:
                # 協調器決策
                decision = coordinator.invoke({"question": question})
                print(f"📋 協調器決策: {decision[:100]}...")
                
                # 根據決策路由到專家
                if decision.startswith("MATH:"):
                    expert_question = decision[5:].strip()
                    result = math_agent.invoke(expert_question)
                    expert_type = "數學專家"
                elif decision.startswith("GEO:"):
                    expert_question = decision[4:].strip()
                    result = geo_agent.invoke(expert_question)
                    expert_type = "地理專家"
                else:
                    result = {"output": decision}
                    expert_type = "協調器"
                
                response = result.get('output', str(result))
                print_success(f"{expert_type}回應: {response[:400]}...")
                
            except Exception as e:
                print_error(f"複合問題處理失敗: {e}")
        
        print_section("Demo 2 完成")
        print_success("成功演示了 A2A → LangChain 的轉換和工作流整合")
        print("✅ A2A 代理已成功轉換為 LangChain 組件")
        print("✅ 可以在 LangChain 工作流中無縫使用")
        print("✅ 支援專家代理的智能路由")
        
    except Exception as e:
        print_error(f"工作流整合測試失敗: {e}")
    finally:
        math_manager.stop_all()
        geo_manager.stop_all()

def main():
    """主函數"""
    print_section("🔄 Demo 2: A2A → LangChain", "=", 60)
    print("演示將 A2A 代理轉換為 LangChain 組件並在工作流中使用")
    
    # 驗證配置
    try:
        Config.validate()
    except SystemExit:
        return 1
    
    try:
        # 執行整合測試
        test_langchain_workflow_integration()
        
    except Exception as e:
        print_error(f"Demo 執行錯誤: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⏹️  Demo 被中斷")
        sys.exit(0)