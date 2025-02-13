# PublicCloudDatabase.swift 文檔
生成時間：2025-02-14 02:41:34
源文件：PublicCloudDatabase.swift
組件類型：Service

### 文檔生成

#### 組件定位
- **類型**: Service
- **職責**: 提供與 iCloud Public Cloud Database 交互的服務，包括存儲、刪除和查詢 WebCache 資料。
- **關鍵協議**: 無

#### 數據與依賴
- **必要數據**:
  - `recordType`: 資料類型，值為 "WebCache"
- **服務依賴**:
  - `CKContainer`: iCloud 容器
  - `CKQuery`: 查詢操作
- **模型依賴**:
  - `CacheModel`: 存儲 WebCache 資料的結構

#### 主要API定義
- **公開方法**:
  - `deleteRecord(recordID: CKRecord.ID, completion: @escaping (Error?) -> Void)`: 刪除指定的記錄。
  - `deleteAllRecords(completion: @escaping (Error?) -> Void)`: 刪除所有記錄。
  - `save(url: String, data: String, completionHandler: @escaping () -> Void = {})`: 存儲 WebCache 資料。
  - `fetch(url: String) async throws -> String?`: 异步获取指定 URL 的 WebCache 資料。

- **回調閉包**:
  - `deleteRecord`: 刪除記錄後的回調，傳遞錯誤信息。
  - `deleteAllRecords`: 刪除所有記錄後的回調，傳遞錯誤信息。
  - `save`: 存儲操作完成後的回調。

- **計算屬性**:
  - 無

#### 邏輯流程
- **數據流向**:
  - `save`: 接收 URL 和 Data，查詢是否存在相同 URL 的記錄，若存在則刪除舊記錄並存儲新記錄。
  - `fetch`: 接收 URL，查詢是否存在相同 URL 的記錄並返回 Data。
  - `deleteRecord`: 接收 RecordID，刪除指定的記錄。
  - `deleteAllRecords`: 查詢所有記錄並逐一刪除。

- **異常處理**:
  - `save` 和 `fetch`: 處理查詢和存儲過程中的錯誤，並通過 DiscordHelper 發送錯誤信息。
  - `deleteRecord` 和 `deleteAllRecords`: 處理刪除過程中的錯誤，並通過回調傳遞錯誤信息。

- **回調時機**:
  - `save`: 存儲操作完成後。
  - `deleteRecord` 和 `deleteAllRecords`: 刪除操作完成後。

### 總結
- **重要性**: 提供與 iCloud Public Cloud Database 交互的核心服務，確保數據的存儲、查詢和刪除操作。
- **複用性**: 可以在多個地方重複使用，例如 ViewModel 或其他 Service 中。