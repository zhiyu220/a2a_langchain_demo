#!/usr/bin/env python3
"""
Google A2A + LangChain 整合演示主程序
提供統一的入口點執行所有演示
"""
import sys
import os
from pathlib import Path

# 添加項目根目錄到 Python 路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import Config
from utils import print_section, print_success, print_error, print_info

def show_menu():
    """顯示主選單"""
    print_section("🚀 Google A2A + LangChain 整合演示", "=", 70)
    print("""
請選擇要執行的演示:

1️⃣  Demo 1: LangChain → A2A
   將 LangChain 組件暴露為 A2A 服務器

2️⃣  Demo 2: A2A → LangChain  
   將 A2A 代理轉換為 LangChain 組件

3️⃣  Demo 3: LangChain Tools → MCP
   將 LangChain 工具暴露為 MCP 端點

4️⃣  Demo 4: MCP → LangChain
   將 MCP 工具轉換為 LangChain 工具

5️⃣  綜合演示
   執行所有四種整合模式的完整演示

6️⃣  檢查系統環境
   驗證所有依賴和配置

0️⃣  退出程序
""")

def check_dependencies():
    """檢查系統依賴"""
    print_section("🔍 檢查系統環境")
    
    # 檢查 Python 版本
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print_success(f"Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print_error(f"Python 版本過舊: {python_version.major}.{python_version.minor}.{python_version.micro}")
        print("需要 Python 3.8 或更高版本")
        return False
    
    # 檢查必要的套件
    required_packages = [
        'python_a2a',
        'langchain',
        'langchain_openai',
        'openai',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"套件已安裝: {package}")
        except ImportError:
            missing_packages.append(package)
            print_error(f"套件未安裝: {package}")
    
    if missing_packages:
        print_error("缺少必要套件，請執行:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    # 檢查 API Key
    if Config.OPENAI_API_KEY:
        print_success("OpenAI API Key 已設置")
        # 隱藏大部分 key 內容
        masked_key = Config.OPENAI_API_KEY[:8] + "..." + Config.OPENAI_API_KEY[-4:]
        print(f"Key: {masked_key}")
    else:
        print_error("OpenAI API Key 未設置")
        print("請執行: export OPENAI_API_KEY=your_api_key")
        return False
    
    # 檢查端口可用性
    from utils import PortManager
    ports = Config.get_server_ports()
    available_ports = []
    
    for name, port in ports.items():
        if PortManager.is_port_available(port):
            available_ports.append(port)
            print_success(f"端口 {port} ({name}) 可用")
        else:
            print_error(f"端口 {port} ({name}) 被占用")
    
    if len(available_ports) >= 2:
        print_success("足夠的端口可用於演示")
    else:
        print_error("可用端口不足，某些演示可能無法正常運行")
    
    print_section("環境檢查完成")
    return len(missing_packages) == 0 and Config.OPENAI_API_KEY is not None

def run_demo(demo_number):
    """執行指定的演示"""
    demos = {
        1: ("examples.demo1_langchain_to_a2a", "Demo 1: LangChain → A2A"),
        2: ("examples.demo2_a2a_to_langchain", "Demo 2: A2A → LangChain"),
        3: ("examples.demo3_langchain_to_mcp", "Demo 3: LangChain Tools → MCP"),
        4: ("examples.demo4_mcp_to_langchain", "Demo 4: MCP → LangChain"),
        5: ("examples.comprehensive_demo", "綜合演示")
    }
    
    if demo_number not in demos:
        print_error("無效的演示編號")
        return False
    
    module_name, demo_name = demos[demo_number]
    
    try:
        print_section(f"🎯 執行 {demo_name}")
        
        # 動態導入模組
        module = __import__(module_name, fromlist=['main'])
        
        # 執行演示
        if hasattr(module, 'main'):
            result = module.main()
            if result == 0:
                print_success(f"{demo_name} 執行成功")
                return True
            else:
                print_error(f"{demo_name} 執行失敗 (退出碼: {result})")
                return False
        else:
            print_error(f"模組 {module_name} 沒有 main 函數")
            return False
            
    except ImportError as e:
        print_error(f"無法導入演示模組: {e}")
        print("請確保所有演示文件都在正確的位置")
        return False
    except Exception as e:
        print_error(f"演示執行錯誤: {e}")
        return False

def interactive_mode():
    """互動模式主循環"""
    while True:
        try:
            show_menu()
            choice = input("\n請選擇 (0-6): ").strip()
            
            if choice == '0':
                print_info("謝謝使用！")
                break
            elif choice == '6':
                check_dependencies()
                input("\n按 Enter 繼續...")
            elif choice in ['1', '2', '3', '4', '5']:
                demo_num = int(choice)
                print_info(f"準備執行演示 {demo_num}...")
                
                # 執行前檢查
                if not Config.OPENAI_API_KEY:
                    print_error("請先設置 OpenAI API Key")
                    print("export OPENAI_API_KEY=your_api_key")
                    input("按 Enter 繼續...")
                    continue
                
                success = run_demo(demo_num)
                if success:
                    print_success("演示完成！")
                else:
                    print_error("演示執行過程中出現問題")
                
                input("\n按 Enter 返回主選單...")
            else:
                print_error("無效選擇，請輸入 0-6")
                input("按 Enter 繼續...")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序被中斷")
            break
        except EOFError:
            print("\n\n👋 程序結束")
            break
        except Exception as e:
            print_error(f"意外錯誤: {e}")
            input("按 Enter 繼續...")

def main():
    """主函數"""
    # 檢查命令行參數
    if len(sys.argv) > 1:
        try:
            demo_num = int(sys.argv[1])
            if demo_num == 0:
                return 0
            elif demo_num == 6:
                return 0 if check_dependencies() else 1
            elif 1 <= demo_num <= 5:
                Config.validate()
                return 0 if run_demo(demo_num) else 1
            else:
                print_error("演示編號必須在 0-6 之間")
                return 1
        except ValueError:
            print_error("請提供有效的演示編號 (0-6)")
            return 1
        except SystemExit as e:
            return e.code
    else:
        # 互動模式
        try:
            interactive_mode()
            return 0
        except Exception as e:
            print_error(f"程序錯誤: {e}")
            return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n👋 程序被用戶中斷")
        sys.exit(0)