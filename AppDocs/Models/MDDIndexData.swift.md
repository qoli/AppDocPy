# MDDIndexData.swift 文檔
生成時間：2025-02-14 02:50:13
源文件：MDDIndexData.swift
組件類型：Model

### 組件定位
- **類型**: Model
- **職責**: 封裝和解析 MDDIndexData 相關的數據結構
- **關鍵協議**: Codable

### 數據與依賴
- **必要數據**:
  - `data`: `[MDDDatum]?`
  - `msg`: `String?`
  - `msgType`: `Int?`
  - `signType`: `String?`
  - `status`: `Bool?`
  - `time`: `Int?`

- **模型依賴**:
  - `MDDDatum`
  - `MDDModuleDatum`
  - `MDDVODList`
  - `MDDPSVODModuleEntryList`
  - `MDDScrollList`

### 主要API定義
- **公開方法**:
  - `init(from decoder: Decoder)` (Codable 協議)
  - `encode(to encoder: Encoder)` (Codable 協議)

### 邏輯流程
- **數據流向**:
  - `jsonData` -> 解析成 `MDDIndexData`
- **異常處理**:
  - 使用 `try?` 捕獲解析錯誤
- **回調時機**:
  - 無

### 輸出格式
```swift
// MARK: - MDDIndexData
struct MDDIndexData: Codable {
    let data: [MDDDatum]?
    let msg: String?
    let msgType: Int?
    let signType: String?
    let status: Bool?
    let time: Int?
}

// MARK: - MDDDatum
struct MDDDatum: Codable {
    let autoMountLive, isSlide, limitNum, liveOrderStrategy: Int?
    let moduleData: [MDDModuleDatum]?
    let moduleType, showMore, showTitle: Int?
    let title, uuid: String?
    let psVODModuleEntryList: [MDDPSVODModuleEntryList]?
    let scrollList: [MDDScrollList]?

    enum CodingKeys: String, CodingKey {
        case autoMountLive, isSlide, limitNum, liveOrderStrategy, moduleData, moduleType, showMore, showTitle, title, uuid
        case psVODModuleEntryList = "psVodModuleEntryList"
        case scrollList
    }
}

// MARK: - MDDModuleDatum
struct MDDModuleDatum: Codable {
    let bannerColor, bannerURL, bigTitle, moduleUUID, name, redirectValue, smallTitle, sourceURL, tagIcon: String?
    let mediaType, redirectType, uuid, displayType, seq, themeType, vodThemeUUID, position: Int?
    let vodList: [MDDVODList]?

    enum CodingKeys: String, CodingKey {
        case bannerColor
        case bannerURL = "bannerUrl"
        case bigTitle, mediaType
        case moduleUUID = "moduleUuid"
        case name, redirectType, redirectValue, smallTitle
        case sourceURL = "sourceUrl"
        case tagIcon, uuid, displayType, seq, themeType, vodList
        case vodThemeUUID = "vodThemeUuid"
        case position
    }
}

// MARK: - MDDVODList
struct MDDVODList: Codable {
    let banner, cornerImage, coverImage, vodListDescription, introVideoURL: String?
    let isFreeLimit: Int?
    let isSub: Bool?
    let isVipSaction: Int?
    let name, scheduleText: String?
    let seq, subDate, totalNum, updateNum: Int?
    let vodThemeUUID, vodUUID, collectionTime: String?

    enum CodingKeys: String, CodingKey {
        case banner, cornerImage, coverImage
        case vodListDescription = "description"
        case introVideoURL = "introVideoUrl"
        case isFreeLimit, isSub, isVipSaction, name, scheduleText, seq, subDate, totalNum, updateNum
        case vodThemeUUID = "vodThemeUuid"
        case vodUUID = "vodUuid"
        case collectionTime
    }
}

// MARK: - MDDPSVODModuleEntryList
struct MDDPSVODModuleEntryList: Codable {
    let commentNum, contentType, defPlayNum, duration, hideName, isHot, isRecommend, isSelect, isTimeLimit, isVip, liveNum: Int?
    let moduleUUID, name, subTitle, uuid, vodServiceName, vodServiceUUID: String?
    let playNum, realTimePlayNum, topNewNum, totalNum, updateNum, vodPlayNum, vodType: Int?
    let cornerImage, coverImage: String?

    enum CodingKeys: String, CodingKey {
        case commentNum, contentType, cornerImage, coverImage, defPlayNum, duration, hideName, isHot, isRecommend, isSelect, isTimeLimit, isVip, liveNum
        case moduleUUID = "moduleUuid"
        case name, playNum, realTimePlayNum, subTitle, topNewNum, totalNum, updateNum, uuid, vodPlayNum, vodType
        case vodUUID = "vodUuid"
        case vodServiceName
        case vodServiceUUID = "vodServiceUuid"
    }
}

// MARK: - MDDScrollList
struct MDDScrollList: Codable {
    let moduleUUID, redirectValue, title: String?
    let redirectType: Int?

    enum CodingKeys: String, CodingKey {
        case moduleUUID = "moduleUuid"
        case redirectType, redirectValue, title
    }
}
```