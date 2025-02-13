# AliSpaceInfo.swift 文檔
生成時間：2025-02-14 03:01:59
源文件：AliSpaceInfo.swift
組件類型：Model

### 組件定位
- **類型**: Model
- **職責**: 存儲和表示阿里雲空間信息，包括個人空間的使用情況
- **關鍵協議**: Codable

### 數據與依賴
- **必要數據**:
  - `personalSpaceInfo`: 包含個人空間的使用和總大小信息
- **模型依賴**:
  - `PersonalSpaceInfo`: 存儲個人空間的具體信息

### 主要API定義
- **公開方法**:
  - `freePercent`: 計算並返回空閒空間百分比
  - `usedPercent`: 計算並返回已使用空間百分比
  - `freeSize`: 計算並返回空閒空間大小

### 邏輯流程
- **數據流向**:
  - `personalSpaceInfo` 提供使用和總大小信息
  - 計算空閒空間百分比、已使用空間百分比和空閒空間大小
- **異常處理**:
  - 無顯式錯誤處理，假設數據有效
- **回調時機**:
  - 無顯式回調，屬性計算在訪問時觸發

### 輸出格式
- **精簡並保持結構化**
  - 突出模型的職責和依賴
- **突出關鍵邏輯**
  - 計算屬性的用途和計算方式
- **標注重要性和複用性**
  - `Codable` 協議標註數據的可編碼和解碼能力
- **使用簡潔的文本描述**
  - 簡明扼要地說明每個屬性和方法的作用

```swift
// AliSpaceInfo.swift
struct AliSpaceInfo: Codable {
    struct PersonalSpaceInfo: Codable {
        let usedSize: Int64
        let totalSize: Int64

        private enum CodingKeys: String, CodingKey {
            case usedSize = "used_size"
            case totalSize = "total_size"
        }
    }

    let personalSpaceInfo: PersonalSpaceInfo

    private enum CodingKeys: String, CodingKey {
        case personalSpaceInfo = "personal_space_info"
    }

    var freePercent: Double { // 空閒空間百分比
        Double(freeSize) / Double(personalSpaceInfo.totalSize)
    }
    
    var usedPercent: Double { // 已使用空間百分比
        Double(personalSpaceInfo.usedSize) / Double(personalSpaceInfo.totalSize)
    }

    var freeSize: Int64 { // 空閒空間大小
        personalSpaceInfo.totalSize - personalSpaceInfo.usedSize
    }
}
```