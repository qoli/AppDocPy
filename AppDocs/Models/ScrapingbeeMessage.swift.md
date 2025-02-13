# ScrapingbeeMessage.swift 文檔
生成時間：2025-02-14 02:43:25
源文件：ScrapingbeeMessage.swift
組件類型：Model

### 文檔生成

#### 組件定位
- **類型**: Model
- **職責**: 封裝 Scrapingbee API 返回的消息數據
- **關鍵協議**: Codable

#### 數據與依賴
- **必要數據**:
  - `message`: String

#### 主要API定義
- **公開方法**: 無
- **計算屬性**: 無

#### 邏輯流程
- **數據流向**:
  - 輸入: Scrapingbee API 返回的 JSON
  - 處理邏輯: 解碼 JSON 為 `ScrapingbeeMessage` 對象
  - 輸出: 包含 `message` 屬性的 `ScrapingbeeMessage` 對象

- **異常處理**: 無
- **回調時機**: 無

### 輸出格式要求
1. **精簡並保持結構化**
2. **突出關鍵邏輯和依賴**
3. **標注重要性和複用性**
4. **使用簡潔的文本描述**