"""
工具函數
包含端口管理、服務器管理等通用功能
"""
import socket
import time
import threading
from typing import Optional, Callable
from config import Config

class PortManager:
    """端口管理器"""
    
    @staticmethod
    def find_available_port(start_port: int = Config.BASE_PORT) -> int:
        """找到可用端口"""
        for port in range(start_port, start_port + Config.PORT_RANGE):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind((Config.DEFAULT_HOST, port))
                sock.close()
                return port
            except OSError:
                continue
        return start_port + 1000
    
    @staticmethod
    def is_port_available(port: int) -> bool:
        """檢查端口是否可用"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((Config.DEFAULT_HOST, port))
            sock.close()
            return True
        except OSError:
            return False

class ServerManager:
    """服務器管理器"""
    
    def __init__(self):
        self.servers = {}
        self.threads = {}
    
    def start_server(self, name: str, server_func: Callable, port: Optional[int] = None) -> int:
        """啟動服務器"""
        if port is None:
            port = PortManager.find_available_port()
        
        def server_target():
            print(f"🚀 啟動 {name} 服務器於端口 {port}")
            try:
                server_func(port)
            except Exception as e:
                print(f"❌ {name} 服務器錯誤: {e}")
        
        thread = threading.Thread(target=server_target, daemon=True)
        thread.start()
        
        # 等待服務器啟動
        time.sleep(Config.SERVER_START_TIMEOUT)
        
        self.servers[name] = port
        self.threads[name] = thread
        
        return port
    
    def get_server_url(self, name: str) -> str:
        """獲取服務器 URL"""
        if name in self.servers:
            return f"http://{Config.DEFAULT_HOST}:{self.servers[name]}"
        raise ValueError(f"服務器 {name} 未啟動")
    
    def stop_all(self):
        """停止所有服務器"""
        print("🔚 正在停止所有服務器...")
        # 由於使用 daemon=True，主程序結束時線程會自動停止

def print_section(title: str, char: str = "-", length: int = 50):
    """打印章節標題"""
    print(f"\n{title}")
    print(char * length)

def print_success(message: str):
    """打印成功消息"""
    print(f"✅ {message}")

def print_error(message: str):
    """打印錯誤消息"""
    print(f"❌ {message}")

def print_info(message: str):
    """打印資訊消息"""
    print(f"ℹ️  {message}")

def wait_for_interrupt(duration: int = 60):
    """等待用戶中斷或超時"""
    print(f"\n🎯 演示將在 {duration} 秒後自動結束，或按 Ctrl+C 立即停止")
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print("\n⏹️  用戶中斷演示")