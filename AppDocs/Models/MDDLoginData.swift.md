# MDDLoginData.swift 文檔
生成時間：2025-02-14 02:53:10
源文件：MDDLoginData.swift
組件類型：Model

### MDDLoginData 文檔

#### 組件定位
- **類型**: Model
- **職責**: 封裝登錄數據，包含用戶信息和狀態
- **關鍵協議**: Codable

#### 數據與依賴
- **必要數據**:
  - `status`: 登錄狀態
  - `msgType`: 消息類型
  - `msg`: 消息內容
  - `data`: 具體用戶數據
  - `signType`: 簽名類型
  - `time`: 時間戳

- **模型依賴**:
  - `MDDLoginDataData`: 具體用戶數據
  - `MDDLoginDataLVInfo`: 等級信息
  - `MDDLoginDataNextLVInfo`: 下一等級信息

#### 主要API定義
- **公開方法**:
  - 無公開方法，主要通過 Codable 協議進行編碼和解碼

- **計算屬性**:
  - 無計算屬性，主要通過 Codable 協議進行數據轉換

#### 邏輯流程
- **數據流向**:
  - `jsonData` -> 解碼成 `MDDLoginData` -> 提取用戶信息和狀態

- **異常處理**:
  - 無顯式錯誤處理，通過 Codable 協議進行數據轉換時會拋出解碼異常

- **回調時機**:
  - 無回調，主要通過 Codable 協議進行數據轉換

### MDDLoginDataData 文檔

#### 組件定位
- **類型**: Model
- **職責**: 封裝具體用戶數據，包含詳細信息和狀態
- **關鍵協議**: Codable

#### 數據與依賴
- **必要數據**:
  - `uuid`: 唯一標識符
  - `seq`: 序號
  - `createTime`: 創建時間
  - `isOncePaid`, `isPay`, `isVODVip`: 支付狀態
  - `vipEffectiveDate`: VIP有效期
  - `serverTimestamp`, `experience`, `score`, `commentQty`: 服務器時間戳和用戶數據
  - `articleCollectionQty`, `starCollectionQty`, `dramaCollectionQty`, `vodCollectionQty`: 收藏數量
  - `postCollectionQty`, `vipLevel`, `postQty`, `postCommentQty`: 帖子相關數據
  - `num`, `password`: 認證信息
  - `settingPush`, `settingWifiImg`, `status`, `sexEnum`: 設置和狀態
  - `birthday`, `realName`, `nickName`, `oldNickName`: 個人信息
  - `appToken`, `appExpiresTime`: 應用令牌和過期時間
  - `memberLVUUID`, `memberGroupUUID`, `os`, `version`: 成員等級和應用信息
  - `channel`, `imRegFlag`, `regDeviceNum`, `loginDeviceNum`, `reservedField1`: 通道和設備信息
  - `whiteListEnable`: 白名單啟用狀態
  - `lvInfo`, `nextLVInfo`: 等級信息
  - `newMsg`, `newCommentMsg`, `newSysMsg`, `followQty`: 新消息和關注數量
  - `isNew`, `fansQty`, `allowModifyPost`: 新用戶和粉絲數量
  - `simpleDesc`: 簡介

- **模型依賴**:
  - `MDDLoginDataLVInfo`: 等級信息
  - `MDDLoginDataNextLVInfo`: 下一等級信息

#### 主要API定義
- **公開方法**:
  - 無公開方法，主要通過 Codable 協議進行編碼和解碼

- **計算屬性**:
  - 無計算屬性，主要通過 Codable 協議進行數據轉換

#### 邏輯流程
- **數據流向**:
  - `jsonData` -> 解碼成 `MDDLoginDataData` -> 提取具體用戶數據

- **異常處理**:
  - 無顯式錯誤處理，通過 Codable 協議進行數據轉換時會拋出解碼異常

- **回調時機**:
  - 無回調，主要通過 Codable 協議進行數據轉換

### MDDLoginDataLVInfo 文檔

#### 組件定位
- **類型**: Model
- **職責**: 封裝用戶等級信息，包含名稱和圖標
- **關鍵協議**: Codable

#### 數據與依賴
- **必要數據**:
  - `uuid`: 唯一標識符
  - `seq`: 序號
  - `createTime`, `name`: 等級名稱和創建時間
  - `icon`: 圖標
  - `privilege`, `activity`, `rule`: 權限和規則
  - `experience`: 經驗值

#### 主要API定義
- **公開方法**:
  - 無公開方法，主要通過 Codable 協議進行編碼和解碼

- **計算屬性**:
  - 無計算屬性，主要通過 Codable 協議進行數據轉換

#### 邏輯流程
- **數據流向**:
  - `jsonData` -> 解碼成 `MDDLoginDataLVInfo` -> 提取等級信息

- **異常處理**:
  - 無顯式錯誤處理，通過 Codable 協議進行數據轉換時會拋出解碼異常

- **回調時機**:
  - 無回調，主要通過 Codable 協議進行數據轉換

### MDDLoginDataNextLVInfo 文檔

#### 組件定位
- **類型**: Model
- **職責**: 封裝下一等級信息，包含名稱和描述
- **關鍵協議**: Codable

#### 數據與依賴
- **必要數據**:
  - `uuid`: 唯一標識符
  - `seq`: 序號
  - `createTime`, `name`, `descript`: 等級名稱和描述
  - `experience`: 經驗值

#### 主要API定義
- **公開方法**:
  - 無公開方法，主要通過 Codable 協議進行編碼和解碼

- **計算屬性**:
  - 無計算屬性，主要通過 Codable 協議進行數據轉換

#### 邏輯流程
- **數據流向**:
  - `jsonData` -> 解碼成 `MDDLoginDataNextLVInfo` -> 提取下一等級信息

- **異常處理**:
  - 無顯式錯誤處理，通過 Codable 協議進行數據轉換時會拋出解碼異常

- **回調時機**:
  - 無回調，主要通過 Codable 協議進行數據轉換

---

以上文檔精簡並保持結構化，突出關鍵邏輯和依賴，使用簡潔的文本描述。