# Swift 專案文檔生成器

這是一個專門為 LLM 優化的 Swift 代碼文檔生成工具。它可以自動分析 Swift 源碼，生成結構化且易於理解的文檔，特別適合協助 LLM 進行代碼維護和開發工作。

## 主要特點

1. LLM 優化的文檔格式
   - 自動分類組件類型
   - 結構化信息提取
   - 優化的 Context Windows 佔用
   - 突出重要依賴關係

2. 智能分類系統
   - Views：UI 相關組件
   - ViewModels：視圖邏輯層
   - Models：數據模型
   - Services：服務層組件
   - Others：其他類型

3. 核心信息提取
   - 組件定位和職責
   - 數據流向和依賴
   - API 定義和用途
   - 異常處理機制

## 前置條件

### 環境要求
- Python 3.8 或更高版本
- 本地運行的 Qwen 2.5-32B LLM 服務
- 穩定的網絡連接

### Python 依賴安裝
```bash
pip install requests datetime argparse typing
```

### LLM 服務配置
1. 確保本地 LLM 服務正在運行
2. 修改腳本中的配置（如需要）：
```python
LLM_URL = "http://192.168.6.176:1234/v1"  # 改為你的 LLM 服務地址
MODEL_NAME = "qwen2.5-32b-instruct-mlx"    # 使用的模型名稱
```

### 目錄結構準備
```bash
your-project/
  ├── send_swift_to_llm.py    # 本工具腳本
  ├── AppDocs/                # 將自動創建的文檔目錄
  └── your-swift-project/     # Swift 源碼目錄
```

## 使用方法

### 基本用法

```bash
python send_swift_to_llm.py <Swift專案目錄路徑>
```

### 執行過程

1. 掃描指定目錄中的所有 .swift 文件
2. 使用 LLM 智能判斷每個文件的組件類型
3. 生成優化後的 Markdown 文檔
4. 自動分類並保存到對應目錄
5. 生成專案總覽文件

### 專案總覽使用指南

專案總覽文件（ProjectOverview.md）提供了整個專案的高層視圖，特別適合處理大型專案或需要快速了解專案結構的場景。

#### 總覽文件內容
1. 組件統計
   - 各類型組件的數量分佈
   - 一目了然的統計表格
   
2. 架構特點
   - 資料流設計模式
   - 核心服務職責
   - UI 層次結構

3. 關鍵路徑
   - 主要業務流程
   - 組件調用關係
   - 數據處理流程

4. 擴展建議
   - 可複用組件識別
   - 重構機會點
   - 優化方向建議

#### 最佳實踐
1. 項目初期：
   ```bash
   # 生成初始文檔
   python send_swift_to_llm.py /path/to/swift/project
   
   # 首先閱讀專案總覽
   open AppDocs/ProjectOverview.md
   ```

2. 了解特定領域：
   ```bash
   # 1. 先看總覽中的相關部分
   # 2. 找到關鍵組件的文檔路徑
   # 3. 按需查看詳細文檔
   ```

3. 大型重構前：
   - 研讀總覽中的架構特點
   - 關注標記的重構機會
   - 評估擴展建議的可行性

## 開發最佳實踐

### 1. 使用 .clinerules 規範開發

強烈建議在專案根目錄中創建 .clinerules 文件，這是確保團隊高效協作的關鍵。你可以：

1. 從本文檔底部複製 .clinerules 模板
2. 保存到你的專案根目錄
3. 根據實際需要調整內容

.clinerules 將幫助你：
- 標準化與 LLM 的互動方式
- 提供清晰的文檔使用指南
- 確保團隊遵循一致的開發流程
- 優化代碼覆用和協作效率

### 2. 文檔驅動開發

在有了 .clinerules 的指導後，按照以下順序進行開發：

1. 理解現有組件
   ```bash
   # 按 .clinerules 建議的順序瀏覽文檔：
   AppDocs/ProjectOverview.md  # 1. 先了解整體架構
   AppDocs/Models/            # 2. 了解數據結構
   AppDocs/Services/          # 3. 查看可用服務
   AppDocs/ViewModels/        # 4. 分析業務邏輯
   AppDocs/Views/             # 5. 參考 UI 實現
   ```

2. 開發新功能示例
   ```bash
   # 遵循 .clinerules 的最佳實踐：
   "這是我們的訂單相關實現：
   {Models/OrderEntity.swift.md}
   {Services/OrderService.swift.md}
   
   需求：實現訂單詳情頁面，展示訂單的基本信息和狀態"
   ```

3. 修改現有功能示例
   ```bash
   # 按照 .clinerules 定義的方式：
   "這是當前的訂單列表實現：
   {ViewModels/OrderListViewModel.swift.md}
   {Views/OrderListView.swift.md}
   
   需求：增加按訂單時間排序功能"
   ```

### 3. LLM 互動策略

基於 .clinerules 的規範：

1. 提供完整上下文
   - 引用專案總覽的相關段落
   - 相關組件的文檔內容
   - 組件間的依賴關係
   - 需要重用的功能
   - 新增或修改的需求

2. 開發順序建議
   - 先閱讀專案總覽
   - 再提供 Model 文檔
   - 然後是 Service 文檔
   - 接著是 ViewModel 文檔
   - 最後是 View 文檔

3. 代碼一致性維護
   - 遵循現有代碼風格
   - 保持組件實現模式
   - 參考架構設計方式
   - 維護項目結構統一

## 技術細節

- 使用 Qwen 2.5-32B 模型
- 支持流式輸出
- 自動化的組件類型判斷
- 結構化的文檔模板
- 完善的錯誤處理
- 專案總覽生成

## 注意事項

1. 環境準備
   - 確保有穩定的網絡連接訪問 LLM 服務
   - 對於大型項目，首次生成文檔可能需要較長時間
   - 生成的文檔位於 AppDocs 目錄下
   - 已存在的文檔不會被覆蓋

2. 效率優化建議
   - 先閱讀專案總覽文件
   - 優先查找和重用現有組件
   - 善用服務層的通用邏輯
   - 複用已實現的數據模型
   - 參考類似功能的實現方式

3. 問題排查指南
   - 提供完整的錯誤上下文
   - 說明當前的測試覆蓋
   - 討論潛在的性能影響
   - 分享類似問題的解決方案

## .clinerules 模板

以下是一個可以直接複製使用的 .clinerules 文件模板，為使用本文檔生成器的項目提供標準化的開發指導：

```
# Swift 項目 LLM 輔助開發指南

## 文檔使用規範

1. 文檔結構導航
先閱讀 ProjectOverview.md 了解整體架構
按需查看各類型組件文檔
按 Views/ViewModels/Models/Services 分類查找所需組件
注意查看 Others 目錄可能的通用組件

2. 向 LLM 提供上下文
引用總覽中的關鍵架構說明
共享相關組件的 .md 文檔內容
說明組件之間的依賴關係
指出需要重用的現有功能
描述需要新增或修改的部分

## 開發流程指南

1. 需求分析階段
閱讀 ProjectOverview.md 了解整體設計
查閱 Models/ 目錄了解數據結構
瀏覽 Services/ 目錄了解可用服務
查看 Views/ 目錄了解現有UI組件
分析 ViewModels/ 目錄了解業務邏輯

2. 設計規劃階段
# 向 LLM 提供上下文的示例：
"這是專案總覽中的相關說明：
{ProjectOverview.md 相關段落}

這是我們的數據模型：
{Models/OrderEntity.swift.md 內容}

這是現有的訂單服務：
{Services/OrderService.swift.md 內容}

請幫我設計一個新的訂單列表頁面"

3. 實現指導
# 開發新功能時的順序：
1. 先閱讀專案總覽相關部分
2. 共享相關 Model 文檔
3. 提供對應 Service 文檔
4. 分享相關的 ViewModel 文檔
5. 最後是 UI 相關的 View 文檔

## 最佳實踐示例

1. 實現新功能
# 錯誤示範
"幫我實現一個訂單詳情頁面"

# 正確示範
"這是專案總覽中相關的架構說明：
{ProjectOverview.md 訂單相關段落}

這是我們的訂單模型和服務實現：
{Models/OrderEntity.swift.md}
{Services/OrderService.swift.md}

請基於這些實現訂單詳情頁面，需要展示訂單的基本信息和狀態"

2. 修改現有功能
# 錯誤示範
"幫我修改訂單列表的排序邏輯"

# 正確示範
"根據總覽文檔，我們的訂單功能採用以下架構：
{ProjectOverview.md 訂單模塊架構}

這是當前的訂單列表實現：
{ViewModels/OrderListViewModel.swift.md}
{Views/OrderListView.swift.md}

請幫我增加按訂單時間排序的功能"

3. 組件重用
# 錯誤示範
"實現一個通用的列表組件"

# 正確示範
"總覽文檔中提到的可重用組件：
{ProjectOverview.md 可重用組件段落}

這是我們現有的列表組件實現：
{Views/CommonListView.swift.md}

請基於這個組件，實現一個支持下拉刷新的版本"

## 注意事項

1. 文檔完整性
先閱讀專案總覽了解整體架構
提供完整的相關組件文檔
包含所有依賴組件的文檔
說明組件間的交互關係
提供必要的業務上下文

2. 開發效率
參考總覽文檔中的建議
優先查找可重用的組件
善用現有的服務層邏輯
複用已實現的數據模型
參考相似功能的實現方式

3. 代碼一致性
遵循文檔中展示的代碼風格
保持相似功能的實現模式
參考現有組件的架構設計
維護統一的項目結構

## 溝通技巧

1. 提供上下文
引用總覽文檔相關內容
共享完整的相關文檔
解釋業務需求和約束
說明技術限制和要求
描述預期的實現效果

2. 迭代優化
基於文檔討論設計方案
參考相似功能的實現
評估不同方案的優劣
及時調整開發方向

3. 問題解決
參考總覽文檔中的常見問題
提供相關組件的錯誤處理方式
分享類似問題的解決方案
說明現有的測試覆蓋情況
討論潛在的性能影響
