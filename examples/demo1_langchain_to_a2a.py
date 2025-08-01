"""
Demo 1: LangChain → A2A
演示如何將 LangChain 組件轉換為 A2A 服務器
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from utils import ServerManager, print_section, print_success, print_error, wait_for_interrupt
from servers.langchain_server import start_langchain_server
from python_a2a import A2AClient

def main():
    """主函數"""
    print_section("🔄 Demo 1: LangChain → A2A", "=", 60)
    print("演示將 LangChain 組件暴露為 A2A 服務器")
    
    # 驗證配置
    try:
        Config.validate()
    except SystemExit:
        return 1
    
    # 創建服務器管理器
    manager = ServerManager()
    
    try:
        # 啟動 LangChain 服務器
        print_section("啟動 LangChain 服務器")
        port = manager.start_server(
            "LangChain服務器",
            start_langchain_server
        )
        server_url = manager.get_server_url("LangChain服務器")
        print_success(f"LangChain 服務器已啟動: {server_url}")
        
        # 測試 A2A 客戶端連接
        print_section("測試 A2A 客戶端")
        client = A2AClient(server_url)
        
        # 測試問題列表
        test_questions = [
            "什麼是人工智能？",
            "請解釋機器學習的基本概念",
            "Python 程式語言有什麼特點？",
            "什麼是深度學習？"
        ]
        
        # 逐一測試問題
        for i, question in enumerate(test_questions, 1):
            print(f"\n🤔 測試問題 {i}: {question}")
            try:
                # 構造 JSON 格式的輸入
                response = client.ask(f'{{"question": "{question}"}}')
                print_success(f"回應: {response[:200]}...")
            except Exception as e:
                print_error(f"請求失敗: {e}")
        
        # 互動模式
        print_section("互動模式")
        print("💬 進入互動模式，輸入 'quit' 退出")
        
        while True:
            try:
                user_input = input("\n請輸入問題: ").strip()
                if user_input.lower() in ['quit', 'exit', '退出']:
                    break
                
                if user_input:
                    response = client.ask(f'{{"question": "{user_input}"}}')
                    print(f"🤖 回應: {response}")
                else:
                    print("⚠️  請輸入有效問題")
                    
            except KeyboardInterrupt:
                print("\n👋 互動模式結束")
                break
            except Exception as e:
                print_error(f"請求錯誤: {e}")
        
        print_section("Demo 1 完成")
        print_success("成功演示了 LangChain → A2A 的轉換")
        print("✅ LangChain 組件已成功暴露為 A2A 服務器")
        print("✅ A2A 客戶端可以正常與服務器通信")
        print("✅ 支援各種類型的問題和回應")
        
    except Exception as e:
        print_error(f"Demo 執行錯誤: {e}")
        return 1
    
    finally:
        manager.stop_all()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⏹️  Demo 被中斷")
        sys.exit(0)