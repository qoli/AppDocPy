# Persistence.swift 文檔
生成時間：2025-02-14 02:40:17
源文件：Persistence.swift
組件類型：Model

### 文檔生成

#### 組件定位
- **類型**: Service
- **職責**: 提供 CoreData 和 CloudKit 的數據持久化和同步功能。
- **關鍵協議**: 無

#### 數據與依賴
- **必要數據**:
  - `PersistenceController.error`: 存儲初始化過程中的錯誤信息。
- **服務依賴**:
  - `CloudKit`: 提供 iCloud 資源管理。
- **模型依賴**:
  - `NSPersistentCloudKitContainer`: 提供 CoreData 和 CloudKit 的集成。

#### 主要API定義
- **公開方法**:
  - `saveContext(completionHandler:)`: 儲存 CoreData 上下文的更改。
  - `getRecordType() -> [String]`: 獲取所有記錄類型。
  - `getDatabaseSize() -> Int64?`: 獲取數據庫大小。
  - `calculateBinaryDataSize() -> Int64`: 計算二進制數據大小。
  - `fetchTotalRecordCountForAllEntities(context:completion:)`: 獲取所有實體的總記錄數。
  - `fetchTotalRecordCount(for:completion:)`: 獲取指定記錄類型的總記錄數。
- **回調閉包**:
  - `saveContext(completionHandler:)`: 儲存成功後的回調。
- **計算屬性**:
  - `PersistenceController.viewContext`: 提供主線程的 CoreData 上下文。
  - `PersistenceController.backgroundContext`: 提供背景線程的 CoreData 上下文。

#### 邏輯流程
- **數據流向**:
  - 初始化 `NSPersistentCloudKitContainer`，配置持久化存儲描述。
  - 檢查 iCloud 帳戶狀態並初始化 CloudKit schema。
  - 提供儲存 CoreData 上下文更改的方法，檢查插入對象的合法性並儲存。
  - 獲取數據庫大小和二進制數據大小的方法。
- **異常處理**:
  - 在初始化過程中捕獲並存儲錯誤信息。
  - 儲存 CoreData 上下文時，處理插入對象的合法性檢查和儲存異常。
- **回調時機**:
  - `saveContext(completionHandler:)`: 儲存成功後觸發回調。
  - `fetchTotalRecordCountForAllEntities(context:completion:)`: 獲取所有實體的總記錄數後觸發回調。
  - `fetchTotalRecordCount(for:completion:)`: 獲取指定記錄類型的總記錄數後觸發回調。

### 重要性和複用性
- **重要性**:
  - `PersistenceController` 是應用的核心服務，負責數據的持久化和同步。
- **複用性**:
  - `PersistenceController` 提供的公開方法和計算屬性可以在多個地方重複使用，確保數據的一致性和可靠性。