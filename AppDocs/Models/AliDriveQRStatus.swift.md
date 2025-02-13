# AliDriveQRStatus.swift 文檔
生成時間：2025-02-14 03:01:26
源文件：AliDriveQRStatus.swift
組件類型：Model

### 文檔生成

#### 組件定位
- **類型**: Model
- **職責**: 封裝阿里雲驅動器二維碼登錄狀態信息
- **關鍵協議**: Codable

#### 數據與依賴
- **必要數據**:
  - `status`: String (登錄狀態)
  - `authCode`: String? (授權碼，可選)

#### 主要API定義
- **公開方法**:
  - `statusText`: String (根據狀態返回對應的中文描述)

#### 邏輯流程
- **數據流向**:
  - `status` -> 根據狀態值返回對應的中文描述
- **異常處理**:
  - 無顯式錯誤處理，返回原始狀態值
- **回調時機**:
  - 無

### 輸出格式
- **精簡並保持結構化**
  - 組件定位、數據與依賴、主要API定義和邏輯流程均按重要性排序
- **突出關鍵邏輯和依賴**
  - 突出 `status` 和 `authCode` 的數據結構，以及 `statusText` 計算屬性的邏輯
- **標注重要性和複用性**
  - `statusText` 計算屬性在不同狀態下返回不同的中文描述，具有較高的複用性和重要性
- **使用簡潔的文本描述**
  - 簡潔明了地描述各部分功能和邏輯，方便快速理解

```swift
// AliDriveQRStatus.swift
struct AliDriveQRStatus: Codable {
    let status: String
    let authCode: String?
}

extension AliDriveQRStatus {
    var statusText: String {
        if status == "WaitLogin" {
            return "等待二維碼掃描"
        }
        if status == "ScanSuccess" {
            return "掃描完畢"
        }
        if status == "LoginSuccess" {
            return "掃描完畢"
        }
        if status == "QRCodeExpired" {
            return "二維碼已過期"
        }
        return status
    }
}
```