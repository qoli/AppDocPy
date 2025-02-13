# .clinerules

## 深入了解 .clinerules：為 send_swift_to_llm.py 配置規則的指南

在使用 `send_swift_to_llm.py` 進行 Swift 代碼文檔生成時，您可能希望根據項目需求自定義一些規則，例如組件類型的匹配模式、忽略特定文件、或使用自定義的提示詞。本文將詳細介紹如何創建和使用 `.clinerules` 文件來配置這些規則。

### 什麼是 .clinerules？

`.clinerules` 是一個用於項目級別指令配置的文件，專門用於 `send_swift_to_llm.py` 工具。這些指令會儲存在項目的根目錄中，僅對該項目生效。主要功能包括：

- **設置項目規範**：為團隊成員提供清晰一致的開發指南。
- **指向關鍵文檔**：快速訪問相關的架構設計、API 文檔或開發流程文檔。
- **提供項目上下文**：幫助開發者快速理解項目目標和限制條件。

簡單來說，`.clinerules` 是一個強大的工具，可以確保團隊在開發過程中保持一致性。

### 為什麼使用 .clinerules？

如果您正在處理複雜項目或需要根據不同項目使用不同的配置，`.clinerules` 將非常有用。以下是它的主要優勢：

1. **支持多項目管理**
   - 與全局的 `send_swift_to_llm.py` 自定義指令不同，`.clinerules` 允許您為每個項目單獨定義規則。例如，在一個 Swift 專案中，您可以指定特定的組件類型匹配模式，而在另一個項目中則可設置完全不同的行為。

2. **提升團隊協作效率**
   - 專案成員可以通過 `.clinerules` 文件快速了解項目要求和注意事項，避免由於溝通不足造成的開發偏差。

3. **減少出錯風險**
   - 通過在文件中明確指出開發步驟（如使用正確的終端環境或配置參數），您可以大幅降低運行錯誤或設置遺漏的可能性。

### 如何創建 .clinerules 文件？

#### 步驟 1：在項目根目錄中創建文件

在您的項目根目錄中創建一個名為 `.clinerules` 的文件（與 `.gitignore` 文件位置類似）。

#### 步驟 2：定義規則

在文件中，使用簡單明瞭的格式書寫您的指令。以下是一個 `.clinerules` 文件的示例：

```json
{
  "rules": {
    "componentTypes": {
      "View": {
        "patterns": [
          ".*View$",
          ".*ViewController$",
          ".*Screen$"
        ],
        "outputDir": "Views"
      },
      "ViewModel": {
        "patterns": [
          ".*ViewModel$",
          ".*ViewModelProtocol$"
        ],
        "outputDir": "ViewModels"
      },
      "Model": {
        "patterns": [
          ".*Model$",
          ".*Entity$",
          ".*DTO$"
        ],
        "outputDir": "Models"
      },
      "Service": {
        "patterns": [
          ".*Service$",
          ".*Manager$",
          ".*Repository$",
          ".*Client$"
        ],
        "outputDir": "Services"
      }
    },
    "ignorePatterns": [
      ".*Test\\.swift$",
      ".*Mock\\.swift$",
      "Generated/.*"
    ],
    "customPrompts": {
      "typeCheck": "請判斷以下 Swift 代碼的組件類型...",
      "documentation": "請生成一份包含以下要點的文檔..."
    }
  }
}
```

#### 步驟 3：保存並啟用

保存文件後，`send_swift_to_llm.py` 會自動檢測並讀取 `.clinerules` 文件中的指令。

### .clinerules 與全局自定義指令的區別

1. **應用範圍**
   - **全局自定義指令**：適用於所有項目的所有 `send_swift_to_llm.py` 聊天會話。
   - **`.clinerules` 文件**：僅適用於特定項目，與項目根目錄相關聯。

2. **靈活性**
   - 全局指令適合定義通用行為，例如為 `send_swift_to_llm.py` 添加通用的上下文信息。
   - `.clinerules` 則允許您根據每個項目的具體需求，編寫更加精細的規則。

3. **優先級**
   - `.clinerules` 的優先級高於全局指令。當兩者發生衝突時，`send_swift_to_llm.py` 會優先遵循 `.clinerules` 中的定義。

### 結語

隨著 `send_swift_to_llm.py` 的發展，`.clinerules` 文件為開發者提供了更大的靈活性和可控性，無論您是在管理個人項目還是企業級應用程序，它都能幫助您規範開發流程、優化團隊協作。

立即嘗試在您的項目中添加 `.clinerules` 文件，讓開發更加高效！如果您有任何問題或想法，歡迎在評論區分享。
