# RecordEntity.swift 文檔
生成時間：2025-02-14 02:38:55
源文件：RecordEntity.swift
組件類型：Model

### RecordEntity 文檔

#### 組件定位
- **類型**: Model
- **職責**: 處理錄製數據，包括時間、播放狀態和存儲操作
- **關鍵協議**: 無

#### 數據與依賴
- **必要數據**:
  - `cmTimeValue`: 錄製時間值
  - `cmTimeScale`: 時間比例尺
  - `durationTime`: 總播放時間
  - `videoTitle`: 媒體標題
  - `key`: 錄製唯一標識
  - `universalItemData`: 媒體數據
  - `mediaName`: 頻道名稱
  - `imageCoverURLString`: 封面圖 URL 字符串
  - `imageBackgroundURLString`: 背景圖 URL 字符串
- **服務依賴**:
  - `MainStatus.shared`: 狀態管理器
  - `HistoryItem.shared`: 歷史記錄管理器
  - `PlayerHelper.shared`: 播放助手
- **模型依賴**:
  - `TMDBHelper.shared`: TMDB 元數據助手
  - `PersistenceController.shared`: 持久化控制器

#### 主要API定義
- **公開方法**:
  - `getCMTime() -> CMTime`: 返回 CMTime
  - `getDurationPlayingText() -> String`: 返回播放時間文本
  - `getDurationTotalText() -> String`: 返回總時間文本
  - `recordPlay()`: 處理播放操作
  - `play(specialPlayURLString: String? = nil) async`: 播放歷史記錄
  - `toString() -> String?`: 返回字符串表示
  - `getBackground() -> URL?`: 返回背景圖 URL
  - `saveRecord(cms: CMTimeScale, cmv: CMTimeValue, lastVideoScreenshot: Data?, lastFaceScreenshot: Data?)`: 存儲錄製數據
- **計算屬性**:
  - `recentTitle: String`: 返回最近標題
  - `coverImage: String`: 返回封面圖 URL

#### 邏輯流程
- **數據流向**:
  - `cmTimeValue` 和 `cmTimeScale` 轉換為 CMTime
  - 總播放時間轉換為文本格式
  - 封面圖和背景圖 URL 處理
- **異常處理**:
  - 總播放時間為 NaN 或無窮時返回 "0"
- **回調時機**:
  - `recordPlay()` 根據數據存在情況觸發不同操作
  - `play(specialPlayURLString: String? = nil) async` 根據特殊播放 URL 字符串觸發播放操作
  - `saveRecord(cms: CMTimeScale, cmv: CMTimeValue, lastVideoScreenshot: Data?, lastFaceScreenshot: Data?)` 存儲錄製數據並保存上下文

### 重要性和複用性
- `getCMTime()` 和 `recordPlay()` 是核心方法，頻繁使用。
- `saveRecord(cms: CMTimeScale, cmv: CMTimeValue, lastVideoScreenshot: Data?, lastFaceScreenshot: Data?)` 用於存儲錄製數據，確保數據持久化。