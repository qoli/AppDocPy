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

OVERVIEW_PROMPT = """### Swift 專案架構分析器
你是一個專業的 iOS 架構分析專家，需要基於提供的組件信息生成一份深入的架構分析報告。

### 分析重點
1. 架構模式識別
   - MVVM 實現特點
   - 依賴注入方式
   - 狀態管理策略
   - 服務層設計模式

2. 核心功能流
   - 用戶交互路徑
   - 數據處理流程
   - 狀態更新機制
   - 異步操作處理

3. 關鍵設計決策
   - 組件解耦策略
   - 數據持久化方案
   - 錯誤處理機制
   - 可擴展性設計

4. 架構評估
   - 代碼組織結構
   - 組件間通信方式
   - 數據流向合理性
   - 測試友好程度

### 輸出格式
## 2. 架構分析
### 2.1 核心架構特點
- 描述項目採用的主要架構模式
- 分析核心服務的職責分配
- 評估數據流設計的合理性

### 2.2 關鍵功能流程
- 列舉主要業務流程
- 分析組件間的調用關係
- 說明數據處理和狀態管理方式

### 2.3 技術特點
- 突出項目的技術亮點
- 分析依賴注入和解耦方式
- 評估異步操作處理方案

### 2.4 優化建議
- 提出可能的重構方向
- 建議代碼復用機會
- 指出潛在的優化空間"""

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
    # 按目錄結構統計組件
    components_by_type: Dict[str, List[ComponentInfo]] = {
        type_name: [] for type_name in COMPONENT_DIRS
    }
    
    for type_name, dir_name in COMPONENT_DIRS.items():
        dir_path = os.path.join(ROOT_OUTPUT_DIR, dir_name)
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                if file.endswith('.swift.md'):
                    # 從實際文件讀取組件信息
                    file_path = os.path.join(dir_path, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    swift_file = file[:-3]  # 移除 .md
                    component = ComponentInfo(swift_file, type_name, "")
                    component.doc_path = file_path
                    component.summary = content[:200]
                    components_by_type[type_name].append(component)

    # 準備概覽數據
    component_data = [
        {
            "type": type_name,
            "count": len(type_components),
            "components": [
                {
                    "name": c.name,
                    "summary": c.summary,
                    "doc_path": c.doc_path
                } for c in type_components
            ]
        }
        for type_name, type_components in components_by_type.items()
        if type_components
    ]

    # 準備深入的架構分析數據
    detailed_analysis = {
        "components": component_data,
        "architecture_patterns": {
            "mvvm_pairs": [
                {
                    "view": comp.name,
                    "viewModel": comp.name.replace("View", "ViewModel"),
                    "summary": comp.summary
                }
                for comp in components
                if comp.type == "View" and any(vm.name == comp.name.replace("View", "ViewModel")
                for vm in components if vm.type == "ViewModel")
            ],
            "service_layer": [
                {
                    "name": comp.name,
                    "summary": comp.summary
                }
                for comp in components
                if comp.type == "Service"
            ],
            "core_models": [
                {
                    "name": comp.name,
                    "summary": comp.summary
                }
                for comp in components
                if comp.type == "Model"
            ]
        },
        "dependencies": {
            "service_dependencies": [
                {
                    "component": comp.name,
                    "type": comp.type,
                    "services": [
                        service.strip()
                        for line in comp.summary.split('\n')
                        for service in line.split()
                        if (("Service" in service or "Manager" in service) and
                            "依賴" in line and
                            not service.startswith('組件類型') and
                            not service.startswith('源文件') and
                            '.swift' in service)
                    ]
                }
                for comp in components
                if comp.summary
            ],
            "model_usage": [
                {
                    "component": comp.name,
                    "type": comp.type,
                    "models": [
                        model.strip()
                        for model in comp.summary.split()
                        if any(m.name.replace(".swift", "") in model
                             for m in components if m.type == "Model")
                    ]
                }
                for comp in components
                if comp.summary
            ]
        },
        "key_patterns": {
            "state_management": [
                comp.name
                for comp in components
                if comp.summary and any(pattern in comp.summary
                    for pattern in ["@State", "@Published", "@StateObject", "@ObservedObject", "@Binding"])
            ],
            "async_operations": [
                comp.name
                for comp in components
                if comp.summary and (
                    any(pattern in comp.summary.lower()
                        for pattern in [
                            "async", "await", "task", "@mainactor", "dispatchqueue",
                            "异步", "並發", "concurrent", "background", "後台",
                            "callback", "completion", "handler"
                        ])
                )
            ],
            "dependency_injection": [
                comp.name
                for comp in components
                if comp.summary and any(pattern in comp.summary
                    for pattern in ["init(", "注入", "依賴", "var service", "let service", "Manager.shared", "Service.shared"])
            ]
        }
    }

    # 生成總覽文檔，使用更詳細的提示
    overview_request = {
        "model": MODEL_NAME,
        "prompt": f"""
{OVERVIEW_PROMPT}

分析以下專案資料並生成深入的架構文檔：

{json.dumps(detailed_analysis, indent=2, ensure_ascii=False)}

請特別注意：
1. View 和 ViewModel 的配對關係
2. 服務層的依賴關係
3. 數據流向和狀態管理
4. 核心業務邏輯的實現方式
""",
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
            # 寫入文檔頭部
            header = f"""# 專案架構總覽
生成時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. 組件分析

### 1.1 組件分佈
| 組件類型 | 數量 | 核心組件 |
|----------|------|----------|
"""
            f.write(header)

            # 識別並添加核心組件
            for type_data in component_data:
                core_components = [
                    comp['name']
                    for comp in type_data['components']
                    if comp['summary'] and (
                        '核心' in comp['summary'] or
                        '主要' in comp['summary'] or
                        'Manager' in comp['name'] or
                        'Service' in comp['name'] or
                        comp['name'] in ['AppEnterView', 'RootView', 'MainView']
                    )
                ][:3]  # 最多顯示3個核心組件
                
                core_str = '、'.join(core_components) if core_components else '無'
                f.write(f"| {type_data['type']} | {type_data['count']} | {core_str} |\n")

            f.write("\n### 1.2 組件關係圖\n```mermaid\ngraph TD\n")
            # 設置圖表樣式
            f.write("""    %% 圖表樣式
            classDef view fill:#ffd7e8,stroke:#ff69b4,stroke-width:2px;
            classDef viewModel fill:#b8d4ff,stroke:#4169e1,stroke-width:2px;
            classDef service fill:#98fb98,stroke:#228b22,stroke-width:2px;
            classDef model fill:#ffe4b5,stroke:#daa520,stroke-width:2px;
            
            %% 設置佈局方向
            graph TB
            
            %% 子圖分組
            subgraph UI Layer
                direction TB
                style UI Layer fill:#fff5f9,stroke:#ff69b4
            end
            
            subgraph Business Layer
                direction TB
                style Business Layer fill:#f5f9ff,stroke:#4169e1
            end
            
            subgraph Data Layer
                direction TB
                style Data Layer fill:#f0fff0,stroke:#228b22
            end
            
            %% 設置組件關係
            linkStyle default stroke:#666,stroke-width:1px;
    
""")
            
            # 生成視圖和視圖模型的關係圖
            f.write("    %% MVVM 關係\n")
            written_nodes = set()  # 追踪已寫入的節點
            
            # 從實際目錄結構獲取組件
            views = []
            viewmodels = []
            services = []
            models = []
            
            for type_name, dir_name in COMPONENT_DIRS.items():
                dir_path = os.path.join(ROOT_OUTPUT_DIR, dir_name)
                if not os.path.exists(dir_path):
                    continue
                    
                for file in os.listdir(dir_path):
                    if file.endswith('.swift.md'):
                        component = {
                            'name': file[:-3],  # 移除 .md
                            'path': os.path.join(dir_path, file)
                        }
                        if type_name == "View":
                            views.append(component)
                        elif type_name == "ViewModel":
                            viewmodels.append(component)
                        elif type_name == "Service":
                            services.append(component)
                        elif type_name == "Model":
                            models.append(component)
            
            # 建立 View-ViewModel 關係
            for view in views:
                view_name = view['name'].replace('.swift', '')
                if 'View' in view_name:
                    vm_name = view_name.replace('View', 'ViewModel')
                    matching_vm = next((vm for vm in viewmodels if vm['name'].startswith(vm_name)), None)
                    
                    if matching_vm:
                        # 寫入 View
                        if view_name not in written_nodes:
                            f.write(f"    {view_name}({view_name})\n")
                            written_nodes.add(view_name)
                            f.write(f"    class {view_name} view\n")
                        
                        # 寫入 ViewModel
                        if vm_name not in written_nodes:
                            f.write(f"    {vm_name}({vm_name})\n")
                            written_nodes.add(vm_name)
                            f.write(f"    class {vm_name} viewModel\n")
                        
                        f.write(f"    {view_name} --> {vm_name}\n")
            
            # 生成核心服務和依賴關係
            f.write("\n    %% 服務層\n")
            service_deps = {}  # 收集所有服務依賴關係
            
            # 寫入服務組件
            for service in services:
                service_name = service['name'].replace('.swift', '')
                if service_name not in written_nodes:
                    f.write(f"    {service_name}[{service_name}]\n")
                    f.write(f"    class {service_name} service\n")
                    written_nodes.add(service_name)
                    
                # 分析服務依賴關係
                if os.path.exists(service['path']):
                    with open(service['path'], 'r', encoding='utf-8') as sf:
                        content = sf.read()
                        for other_service in services:
                            other_name = other_service['name'].replace('.swift', '')
                            if other_name != service_name and other_name in content:
                                if service_name not in service_deps:
                                    service_deps[service_name] = set()
                                service_deps[service_name].add(other_name)
            
            # 找出所有核心服務
            core_services = set()
            for service in detailed_analysis.get('architecture_patterns', {}).get('service_layer', []):
                if 'Manager' in service['name'] or 'Service' in service['name']:
                    service_name = service['name'].replace('.swift', '')
                    core_services.add(service_name)
                    if service_name not in written_nodes:
                        f.write(f"    {service_name}[{service_name}]\n")
                        f.write(f"    class {service_name} service\n")
                        written_nodes.add(service_name)

            # 收集依賴關係
            for dep in detailed_analysis.get('dependencies', {}).get('service_dependencies', []):
                if dep.get('services'):
                    comp_name = dep['component'].replace('.swift', '')
                    if comp_name not in service_deps:
                        service_deps[comp_name] = set()
                    
                    for service in dep['services']:
                        service_name = service.replace('.swift', '')
                        if service_name in core_services and service_name != comp_name:
                            service_deps[comp_name].add(service_name)

            # 寫入依賴關係
            f.write("\n    %% 服務依賴關係\n")
            for service_name, deps in service_deps.items():
                for dep in deps:
                    f.write(f"    {service_name} --> {dep}\n")
            
            # 添加模型層
            f.write("\n    %% 模型層\n")
            model_deps = {}  # 收集模型依賴關係
            
            # 寫入模型組件
            for model in models:
                model_name = model['name'].replace('.swift', '')
                if model_name not in written_nodes:
                    f.write(f"    {model_name}[{model_name}]\n")
                    f.write(f"    class {model_name} model\n")
                    written_nodes.add(model_name)
            
            # 分析模型的使用關係
            for vm in viewmodels:
                if os.path.exists(vm['path']):
                    vm_name = vm['name'].replace('.swift', '')
                    with open(vm['path'], 'r', encoding='utf-8') as vf:
                        content = vf.read()
                        for model in models:
                            model_name = model['name'].replace('.swift', '')
                            if model_name in content:
                                f.write(f"    {vm_name} --> {model_name}\n")
            
            # 分析服務層對模型的使用
            for service in services:
                if os.path.exists(service['path']):
                    service_name = service['name'].replace('.swift', '')
                    with open(service['path'], 'r', encoding='utf-8') as sf:
                        content = sf.read()
                        for model in models:
                            model_name = model['name'].replace('.swift', '')
                            if model_name in content:
                                f.write(f"    {service_name} --> {model_name}\n")

            f.write("```\n\n")
            
            # 準備分析數據統計
            mvvm_pairs_count = len(detailed_analysis.get('architecture_patterns', {}).get('mvvm_pairs', []))
            core_services_count = len(core_services)
            state_management_count = len(detailed_analysis.get('key_patterns', {}).get('state_management', []))
            async_ops_count = len(detailed_analysis.get('key_patterns', {}).get('async_operations', []))
            di_count = len(detailed_analysis.get('key_patterns', {}).get('dependency_injection', []))
            
            # 寫入預設的架構分析
            f.write(f"""## 2. 架構分析

### 2.1 核心架構特點
- **MVVM 架構實現**：完整實現 {mvvm_pairs_count} 對 View-ViewModel 組合
- **服務層設計**：包含 {core_services_count} 個核心服務，採用單例模式管理關鍵業務邏輯
- **狀態管理**：使用 SwiftUI 的 @State/@Published，共 {state_management_count} 處狀態管理點
- **異步處理**：採用 Swift Concurrency，有 {async_ops_count} 個異步操作點
- **依賴注入**：使用建構器注入，{di_count} 處注入點，確保組件解耦

### 2.2 關鍵功能流程
- View 層通過 ViewModel 獲取和更新數據
- 業務邏輯統一由服務層處理
- 資料持久化使用 CoreData 框架
- 採用 Combine 框架處理數據流

### 2.3 技術特點
- SwiftUI 聲明式 UI 開發
- Swift Concurrency 異步處理
- 響應式編程（Combine）
- 依賴注入解耦
- 統一的錯誤處理

### 2.4 優化建議
1. 考慮引入路由層管理導航邏輯
2. 加強模塊間通信的類型安全性
3. 增加單元測試覆蓋率
4. 考慮使用依賴注入容器
""")
            print("生成深入架構分析...")
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

def collect_existing_docs() -> List[ComponentInfo]:
    """收集已存在的文檔信息"""
    components = []
    try:
        # 遍歷所有組件目錄
        for comp_type, dir_name in COMPONENT_DIRS.items():
            doc_dir = os.path.join(ROOT_OUTPUT_DIR, dir_name)
            if not os.path.exists(doc_dir):
                continue
                
            # 讀取該目錄下的所有 .md 文件
            for file in os.listdir(doc_dir):
                if file.endswith('.swift.md'):
                    file_path = os.path.join(doc_dir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # 創建組件信息
                    swift_file = file[:-3]  # 移除 .md
                    component = ComponentInfo(swift_file, comp_type, "")
                    component.doc_path = file_path
                    component.summary = content[:200]  # 使用文件開頭作為摘要
                    components.append(component)
                    
        return components
    except Exception as e:
        print(f"收集現有文檔時發生錯誤：{e}")
        return []

def reorganize_docs() -> None:
    """重新組織文檔文件夾結構"""
    try:
        moves = []  # 記錄需要移動的文件
        
        # 遍歷所有組件目錄
        for _, dir_name in COMPONENT_DIRS.items():
            doc_dir = os.path.join(ROOT_OUTPUT_DIR, dir_name)
            if not os.path.exists(doc_dir):
                continue
                
            # 讀取該目錄下的所有 .md 文件
            for file in os.listdir(doc_dir):
                if not file.endswith('.swift.md'):
                    continue
                    
                file_path = os.path.join(doc_dir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 從詳細文檔中提取實際組件類型
                actual_type = None
                for line in content.split('\n'):
                    if "- **類型**:" in line:
                        type_part = line.split("- **類型**:", 1)[1].strip()
                        # 提取類型值（去除可能的額外描述）
                        type_value = type_part.split()[0].strip()
                        
                        # 映射常見的類型表述到標準類型
                        type_mapping = {
                            # View 相关
                            "View": "View",
                            "視圖": "View",
                            "UIComponent": "View",
                            
                            # ViewModel 相关
                            "ViewModel": "ViewModel",
                            "視圖模型": "ViewModel",
                            
                            # Model 相关
                            "Model": "Model",
                            "模型": "Model",
                            "Entity": "Model",
                            "實體": "Model",
                            
                            # Service 相关
                            "Service": "Service",
                            "服務": "Service",
                            "Helper": "Service",
                            "Helper Class": "Service",
                            "Manager": "Service",
                            "Utility": "Service",
                            "工具類": "Service",
                            "Configuration": "Service",
                        }
                        
                        actual_type = type_mapping.get(type_value, "Other")
                        if actual_type in COMPONENT_DIRS:
                            target_dir = os.path.join(ROOT_OUTPUT_DIR, COMPONENT_DIRS[actual_type])
                            if os.path.abspath(doc_dir) != os.path.abspath(target_dir):
                                moves.append((file_path, os.path.join(target_dir, file)))
                                
                                # 更新文件內容中的組件類型標記
                                new_content = []
                                header_updated = False
                                for content_line in content.split('\n'):
                                    if content_line.startswith('組件類型：') and not header_updated:
                                        new_content.append(f'組件類型：{actual_type}')
                                        header_updated = True
                                    else:
                                        new_content.append(content_line)
                                        
                                if header_updated:
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                        f.write('\n'.join(new_content))
                        break
                        
        # 執行文件移動
        if moves:
            print("\n開始重新組織文檔...")
            for src, dst in moves:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                print(f"移動: {os.path.basename(src)} -> {os.path.relpath(dst, ROOT_OUTPUT_DIR)}")
                os.rename(src, dst)
            print("文檔重組完成！")
        else:
            print("沒有需要重組的文檔")
            
    except Exception as e:
        print(f"重組文檔時發生錯誤：{e}")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='Swift 代碼文檔生成工具')
    parser.add_argument('swift_dir', nargs='?', help='Swift 源代碼目錄路徑')
    parser.add_argument('--rebuild-overview', action='store_true',
                      help='只重新生成專案總覽文檔')
    parser.add_argument('--reorganize', action='store_true',
                      help='重新組織文檔文件夾結構')

    args = parser.parse_args()

    # 處理重組文檔請求
    if args.reorganize:
        if not os.path.exists(ROOT_OUTPUT_DIR):
            print(f"錯誤：文檔目錄不存在：{ROOT_OUTPUT_DIR}")
            return
            
        reorganize_docs()
        
        # 重組後重建總覽
        print("\n更新專案總覽...")
        components = collect_existing_docs()
        if components:
            generate_project_overview(components, ROOT_OUTPUT_DIR)
        return
        
    # 處理重建總覽請求
    if args.rebuild_overview:
        print("重新生成專案總覽文檔...")
        if not os.path.exists(ROOT_OUTPUT_DIR):
            print(f"錯誤：文檔目錄不存在：{ROOT_OUTPUT_DIR}")
            return
            
        components = collect_existing_docs()
        if not components:
            print("錯誤：未找到任何現有文檔")
            return
            
        generate_project_overview(components, ROOT_OUTPUT_DIR)
        print("專案總覽文檔重建完成！")
        return

    if not args.swift_dir:
        parser.print_help()
        return

    if not setup_environment(args.swift_dir):
        return

    swift_files = collect_swift_files(args.swift_dir)
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