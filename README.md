# Google A2A + LangChain 整合演示

這個項目演示了 Google A2A (Agent-to-Agent) 協議與 LangChain 框架的四種基本整合模式，展示如何構建模組化、可互操作的 AI 系統。

## 🚀 快速開始

### 環境需求

- Python 3.8+
- OpenAI API Key

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 設置 API Key

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

### 運行演示

```bash
# 互動模式 - 推薦新手使用
python main.py

# 直接運行特定演示
python main.py 1  # Demo 1: LangChain → A2A
python main.py 2  # Demo 2: A2A → LangChain
python main.py 3  # Demo 3: LangChain Tools → MCP
python main.py 4  # Demo 4: MCP → LangChain
python main.py 5  # 綜合演示

# 檢查環境
python main.py 6
```

## 📁 項目結構

```
a2a_langchain_demo/
├── README.md              # 項目說明
├── requirements.txt       # 依賴列表
├── config.py             # 配置管理
├── utils.py              # 工具函數
├── main.py               # 主程序入口
├── servers/              # 服務器實現
│   ├── langchain_server.py   # LangChain 服務器
│   ├── a2a_agent.py         # A2A 代理服務器
│   └── mcp_server.py        # MCP 服務器
├── tools/                # 工具實現
│   ├── calculator.py        # 計算器工具
│   └── text_tools.py        # 文本處理工具
├── clients/              # 客戶端（待實現）
└── examples/             # 演示程序
    ├── demo1_langchain_to_a2a.py     # Demo 1
    ├── demo2_a2a_to_langchain.py     # Demo 2
    ├── demo3_langchain_to_mcp.py     # Demo 3
    ├── demo4_mcp_to_langchain.py     # Demo 4
    └── comprehensive_demo.py         # 綜合演示
```

## 🔄 四種整合模式

### 1. LangChain → A2A
將 LangChain 組件（如 LLM、Chain、Agent）暴露為 A2A 服務器，使其他 A2A 代理能夠與之通信。

**核心概念:**
- 使用 `to_a2a_server()` 轉換 LangChain 組件
- 通過標準化的 A2A 協議提供服務
- 支援任何 A2A 客戶端訪問

**使用場景:**
- 將現有 LangChain 應用暴露給其他 AI 系統
- 構建可被多個代理訪問的共享服務
- 實現跨框架的 AI 服務整合

### 2. A2A → LangChain
將 A2A 代理轉換為 LangChain 組件，在 LangChain 工作流中使用專門的 A2A 代理。

**核心概念:**
- 使用 `to_langchain_agent()` 轉換 A2A 代理
- 在 LangChain Chain 中無縫使用
- 支援複雜的工作流整合

**使用場景:**
- 在 LangChain 應用中使用專門的外部代理
- 構建多專家系統
- 實現智能路由和任務分配

### 3. LangChain Tools → MCP
將 LangChain 工具暴露為 MCP (Model Context Protocol) 端點，提供標準化的工具調用接口。

**核心概念:**
- 使用 `to_mcp_server()` 轉換工具集合
- 通過 REST API 提供工具服務
- 支援標準化的工具發現和調用

**使用場景:**
- 將內部工具暴露給外部系統
- 構建工具市場或服務註冊中心
- 實現工具的標準化管理

### 4. MCP → LangChain
將 MCP 工具轉換為 LangChain 工具，在 LangChain 代理中使用外部工具服務。

**核心概念:**
- 使用 `to_langchain_tool()` 轉換 MCP 工具
- 支援動態工具發現和使用
- 無縫整合到 LangChain 工具生態

**使用場景:**
- 使用外部提供的專門工具
- 構建工具豐富的 AI 應用
- 實現工具的熱插拔和擴展

## 🛠️ 核心組件

### 服務器組件

#### LangChain 服務器 (`servers/langchain_server.py`)
- 提供基於 OpenAI 的對話服務
- 支援自定義提示模板
- 可配置模型參數

#### A2A 代理服務器 (`servers/a2a_agent.py`)
- **數學專家代理**: 專門處理數學相關問題
- **地理專家代理**: 提供地理和旅遊資訊
- 支援代理卡片和技能描述

#### MCP 服務器 (`servers/mcp_server.py`)
- **簡單工具集**: 基本文本處理工具
- **LangChain 工具集**: 基於 LangChain 工具的 MCP 服務
- **進階工具集**: 複雜分析和處理工具

### 工具組件

#### 計算器工具 (`tools/calculator.py`)
- **基本計算器**: 安全的數學表達式求值
- **科學計算器**: 支援三角函數、對數等高級函數
- 完整的錯誤處理和安全檢查

#### 文本工具 (`tools/text_tools.py`)
- **文本長度工具**: 計算字符數
- **文本統計工具**: 單詞、行數等統計
- **文本分析工具**: 深度分析包含頻率統計
- **文本轉換工具**: 大小寫轉換、反轉等
- **文本驗證工具**: 驗證電子郵件、URL 等格式

## 🎯 演示內容

### Demo 1: LangChain → A2A
- 創建友善的 AI 助手
- 轉換為 A2A 服務器
- A2A 客戶端測試
- 互動問答模式

### Demo 2: A2A → LangChain
- 創建專門的數學和地理代理
- 轉換為 LangChain 組件
- 工作流整合測試
- 智能路由演示

### Demo 3: LangChain Tools → MCP
- 工具集合轉換
- MCP 端點測試
- REST API 調用演示

### Demo 4: MCP → LangChain
- MCP 工具發現
- 轉換為 LangChain 工具
- 代理中的工具使用

### 綜合演示
- 所有模式的組合使用
- 複雜任務的協作處理
- 端到端工作流演示

## ⚙️ 配置選項

### 環境變數
- `OPENAI_API_KEY`: OpenAI API 密鑰（必需）

### 配置文件 (`config.py`)
```python
class Config:
    # API 配置
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    
    # 服務器配置
    DEFAULT_HOST = "localhost"
    BASE_PORT = 8000
    
    # 模型配置
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_TEMPERATURE = 0.7
```

## 🔧 故障排除

### 常見問題

#### 1. 端口被占用
```bash
# 檢查端口使用情況
netstat -an | grep :8000

# 或使用系統檢查
python main.py 6
```

#### 2. API Key 問題
```bash
# 檢查是否正確設置
echo $OPENAI_API_KEY

# 重新設置
export OPENAI_API_KEY=your_key_here
```

#### 3. 依賴問題
```bash
# 重新安裝所有依賴
pip install -r requirements.txt --upgrade

# 檢查特定套件
python -c "import python_a2a; print('OK')"
```

#### 4. 服務器啟動失敗
- 檢查端口是否被占用
- 確認 API Key 有效
- 查看錯誤日誌詳細資訊

### 性能優化

#### 1. 服務器配置
- 調整 `SERVER_START_TIMEOUT` 適應不同網路環境
- 修改 `REQUEST_TIMEOUT` 處理長時間運行的任務

#### 2. 模型配置
- 使用更快的模型如 `gpt-3.5-turbo` 提升回應速度
- 調整 `temperature` 平衡創意和一致性

## 📚 進階用法

### 自定義代理
```python
from servers.a2a_agent import create_custom_agent

agent = create_custom_agent(
    name="自定義專家",
    speciality="特定領域",
    system_prompt="你的專門提示..."
)
```

### 自定義工具
```python
from langchain.tools import Tool

def my_custom_function(input_text):
    # 你的業務邏輯
    return f"處理結果: {input_text}"

custom_tool = Tool(
    name="my_tool",
    description="我的自定義工具",
    func=my_custom_function
)
```

### 批次處理
```python
# 批次問題處理
questions = ["問題1", "問題2", "問題3"]
results = []

for question in questions:
    result = agent.invoke(question)
    results.append(result)
```
