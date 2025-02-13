import os
import sys
import requests
import datetime
import json
import argparse
from typing import Optional, Tuple, Dict, List

# 配置
LLM_URL = "http://192.168.6.176:1234/v1"
MODEL_NAME = "qwen2.5-32b-instruct-mlx"

TYPE_CHECK_PROMPT = """### Swift 代碼類型判斷
請判斷以下 Swift 代碼屬於哪種組件類型。

### 判斷規則
- View: 包含 View 相關的 UI 組件
- ViewModel: 處理視圖邏輯的組件
- Model: 數據模型或實體
- Service: 服務層組件
- Other: 其他類型

### 輸出格式
僅需輸出類型名稱，不需要任何解釋：
View|ViewModel|Model|Service|Other"""

DOC_PROMPT = """### LLM 閱讀優化文檔生成器
你是一個專門為 LLM 閱讀優化的代碼文檔生成器，需要將 Swift 代碼轉換為精簡的結構化文檔。目標是降低其他 LLM 在閱讀代碼時的 Context Windows 負擔。

### 核心信息提取（按重要性排序）
1. 組件定位
    ```swift
    類型：View/ViewModel/Model/Service
    職責：核心功能描述
    關鍵協議：實現的主要協議
    ```

2. 數據與依賴
    ```swift
    必要數據：@State/@Binding/@Published 等
    服務依賴：注入的服務類
    模型依賴：使用的數據模型
    ```

3. 主要API定義
    ```swift
    公開方法：名稱(參數) -> 返回
    回調閉包：類型與觸發時機
    計算屬性：用途說明
    ```

4. 邏輯流程
    ```
    數據流向：輸入數據 -> 處理邏輯 -> 輸出結果
    異常處理：錯誤類型和處理方式
    回調時機：觸發條件和處理流程
    ```

### 輸出格式要求
1. 精簡並保持結構化
2. 突出關鍵邏輯和依賴
3. 標注重要性和複用性
4. 使用簡潔的文本描述"""

OVERVIEW_PROMPT = """### Swift 專案結構總覽生成
請基於以下組件信息，生成一份專案總覽文檔。目標是幫助開發者快速理解專案的整體架構。

### 輸出格式要求
1. 專案統計
   - 各類型組件數量統計
   - 核心組件清單（按重要性排序）
   - 關鍵依賴關係圖

2. 架構特點
   - 資料流設計模式
   - 核心服務職責
   - UI 層次結構

3. 關鍵路徑
   - 主要業務流程
   - 組件調用鏈
   - 數據處理流程

4. 擴展建議
   - 複用機會
   - 重構方向
   - 優化空間

### 注意事項
1. 重點突出核心組件
2. 清晰展示依賴關係
3. 標注重要實現模式
4. 總結代碼風格特點"""

ROOT_OUTPUT_DIR = "AppDocs"
COMPONENT_DIRS = {
    "View": "Views",
    "ViewModel": "ViewModels",
    "Model": "Models",
    "Service": "Services",
    "Other": "Others"  # 默認類別
}

class ComponentInfo:
    def __init__(self, name: str, type: str, path: str):
        self.name = name
        self.type = type
        self.path = path
        self.doc_path = ""
        self.summary = ""

def setup_environment(swift_files_dir: str) -> bool:
    """初始化環境配置"""
    try:
        # 創建主輸出目錄
        os.makedirs(ROOT_OUTPUT_DIR, exist_ok=True)
        
        # 創建各組件類型的子目錄
        for dir_name in COMPONENT_DIRS.values():
            os.makedirs(os.path.join(ROOT_OUTPUT_DIR, dir_name), exist_ok=True)
            
        if not os.path.exists(swift_files_dir):
            print(f"錯誤：源目錄不存在：{swift_files_dir}")
            return False
        return True
    except Exception as e:
        print(f"設置環境時發生錯誤：{e}")
        return False

def collect_swift_files(swift_files_dir: str) -> list[Tuple[str, str]]:
    """收集所有 Swift 文件"""
    swift_files = []
    try:
        for root, _, files in os.walk(swift_files_dir):
            for file in files:
                if file.endswith(".swift"):
                    file_path = os.path.join(root, file)
                    swift_files.append((file, file_path))
        return swift_files
    except Exception as e:
        print(f"收集文件時發生錯誤：{e}")
        return []

def get_component_type(swift_code: str) -> str:
    """使用 LLM 判斷組件類型"""
    request_data = {
        "model": MODEL_NAME,
        "prompt": f"{TYPE_CHECK_PROMPT}\n\n{swift_code}",
        "stream": False,
        "temperature": 0.2,
        "top_p": 0.8,
        "max_tokens": 10,
        "stop": ["\n"]
    }

    try:
        response = requests.post(
            f"{LLM_URL}/completions",
            headers={"Content-Type": "application/json"},
            json=request_data,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'choices' in data and len(data['choices']) > 0:
            component_type = data['choices'][0]['text'].strip()
            if component_type in COMPONENT_DIRS:
                return component_type
                
        return "Other"
        
    except Exception as e:
        print(f"組件類型判斷失敗：{e}")
        return "Other"

def generate_documentation(swift_code: str, output_file_path: str, component_type: str, file: str) -> str:
    """生成文檔，返回文檔摘要"""
    request_data = {
        "model": MODEL_NAME,
        "prompt": f"{DOC_PROMPT}\n\n{swift_code}",
        "stream": True,
        "temperature": 0.2,
        "top_p": 0.8,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.8,
        "max_tokens": 4000,
        "stop": ["<|endoftext|>"]
    }

    summary = ""
    try:
        response = requests.post(
            f"{LLM_URL}/completions",
            headers={"Content-Type": "application/json"},
            json=request_data,
            stream=True,
            timeout=180
        )
        response.raise_for_status()

        print(f"開始生成文檔...\n")
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            # 寫入頭部信息
            header = f"""# {file} 文檔
生成時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
源文件：{os.path.basename(file)}
組件類型：{component_type}

"""
            f.write(header)
            print(header)
            
            # 處理流式響應
            for line in response.iter_lines():
                if not line:
                    continue

                try:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = json.loads(line[5:])
                        if 'choices' in data:
                            choice = data['choices'][0]
                            
                            # 檢查是否生成結束
                            if choice.get('finish_reason') == 'stop':
                                break
                                
                            # 獲取生成的文本
                            text = choice.get('text', '')
                            if text:
                                print(text, end='', flush=True)
                                f.write(text)
                                f.flush()
                                # 收集前 200 字符作為摘要
                                if len(summary) < 200:
                                    summary += text

                except json.JSONDecodeError:
                    print(f"\n警告：JSON 解析錯誤：{line}")
                except Exception as e:
                    print(f"\n警告：處理響應時發生錯誤：{e}")
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 錯誤：{e}\n")
    except Exception as e:
        print(f"文檔生成失敗：{e}\n")
    
    return summary[:200] + "..." if len(summary) > 200 else summary

def generate_project_overview(components: List[ComponentInfo], output_dir: str) -> None:
    """生成專案總覽文檔"""
    # 按類型分類組件
    components_by_type: Dict[str, List[ComponentInfo]] = {
        type_name: [] for type_name in COMPONENT_DIRS
    }
    for component in components:
        components_by_type[component.type].append(component)

    # 準備概覽數據
    component_data = []
    for type_name, type_components in components_by_type.items():
        if type_components:
            component_data.append({
                "type": type_name,
                "count": len(type_components),
                "components": [
                    {
                        "name": c.name,
                        "summary": c.summary,
                        "doc_path": c.doc_path
                    } for c in type_components
                ]
            })

    # 生成總覽文檔
    overview_request = {
        "model": MODEL_NAME,
        "prompt": f"{OVERVIEW_PROMPT}\n\n{json.dumps(component_data, indent=2)}",
        "stream": True,
        "temperature": 0.3,
        "top_p": 0.8,
        "max_tokens": 4000,
    }

    try:
        response = requests.post(
            f"{LLM_URL}/completions",
            headers={"Content-Type": "application/json"},
            json=overview_request,
            stream=True,
            timeout=180
        )
        response.raise_for_status()

        overview_path = os.path.join(output_dir, "ProjectOverview.md")
        print(f"\n生成專案總覽文檔...\n")

        with open(overview_path, 'w', encoding='utf-8') as f:
            # 寫入頭部信息
            header = f"""# 專案總覽文檔
生成時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 組件統計
"""
            f.write(header)

            # 添加組件統計表格
            stats_table = "| 組件類型 | 數量 |\n|----------|------|\n"
            for type_data in component_data:
                stats_table += f"| {type_data['type']} | {type_data['count']} |\n"
            f.write(stats_table + "\n")

            # 寫入 LLM 生成的總覽內容
            print("生成架構分析...")
            for line in response.iter_lines():
                if not line:
                    continue

                try:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = json.loads(line[5:])
                        if 'choices' in data:
                            choice = data['choices'][0]
                            if choice.get('finish_reason') == 'stop':
                                break
                            text = choice.get('text', '')
                            if text:
                                print(text, end='', flush=True)
                                f.write(text)
                                f.flush()
                except Exception as e:
                    print(f"\n警告：處理響應時發生錯誤：{e}")

        print(f"\n總覽文檔已生成：{overview_path}\n")

    except Exception as e:
        print(f"生成總覽文檔失敗：{e}")

def process_file(file: str, file_path: str, index: int, total: int) -> Optional[ComponentInfo]:
    """處理單個文件，返回組件信息"""
    print(f"\n{'='*60}")
    print(f"處理文件 [{index}/{total}]: {file}")
    print(f"{'='*60}\n")
    
    try:
        # 讀取源文件內容
        with open(file_path, 'r', encoding='utf-8') as f:
            swift_code = f.read()
            
        # 步驟 1: 使用 LLM 判斷組件類型
        print("判斷組件類型...")
        component_type = get_component_type(swift_code)
        print(f"識別為: {component_type}")
        
        # 構建輸出路徑
        component_dir = COMPONENT_DIRS[component_type]
        output_file_path = os.path.join(ROOT_OUTPUT_DIR, component_dir, f"{file}.md")

        component = ComponentInfo(file, component_type, file_path)
        component.doc_path = output_file_path
        
        if os.path.exists(output_file_path):
            print(f"文件已存在，跳過處理\n")
            return component
            
        # 步驟 2: 生成文檔
        summary = generate_documentation(swift_code, output_file_path, component_type, file)
        component.summary = summary
        
        print(f"\n\n{'='*60}")
        print(f"文檔已保存至：{output_file_path}")
        print(f"{'='*60}\n")
        
        return component
        
    except Exception as e:
        print(f"處理文件時發生錯誤：{e}\n")
        return None

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='Swift 代碼文檔生成工具')
    parser.add_argument('swift_dir', help='Swift 源代碼目錄路徑')

    args = parser.parse_args()
    swift_files_dir = args.swift_dir

    if not setup_environment(swift_files_dir):
        return

    swift_files = collect_swift_files(swift_files_dir)
    if not swift_files:
        print("未找到任何 Swift 文件")
        return

    total_files = len(swift_files)
    print(f"\n開始處理 {total_files} 個 Swift 文件...")
    
    # 收集所有組件信息
    components: List[ComponentInfo] = []
    for index, (file, file_path) in enumerate(swift_files, 1):
        component = process_file(file, file_path, index, total_files)
        if component:
            components.append(component)
    
    # 生成專案總覽
    print("\n生成專案總覽...")
    generate_project_overview(components, ROOT_OUTPUT_DIR)
    
    print("處理完成！")

if __name__ == "__main__":
    main()