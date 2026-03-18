from openai.types.chat.chat_completion_stream_options_param import ChatCompletionStreamOptionsParam
from openai import responses
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
import json

load_dotenv()


def main():
  llm = ChatOpenAI(
	model="gemma3:27b",
	base_url="http://203.71.78.31:8000/v1",
	api_key="sk-12345678",
	temperature=0.0,
)
  message = []
  message.append({"role": "system", "content": "你是一位專業的資料工程師，擅長將產品規格轉換為結構化資料（JSON），並確保資訊完整且語意清晰。"})
  message.append({"role": "user", "content": """ 1. 個人角色設定

你是一位專業的資料工程師，擅長將產品規格轉換為結構化資料（JSON），並確保資訊完整且語意清晰。

2. 情境

你正在處理一段關於高性能筆電的產品說明文字，需要將其轉換為可供系統使用的標準化資料格式。

3. 任務

請將提供的產品規格內容轉換為 JSON 物件，並保留所有關鍵技術資訊（如處理器、記憶體、儲存裝置等）。

4. 格式

輸出為標準 JSON 格式

使用清楚的欄位名稱（例如：CPU、RAM、Storage 等）

結構需具備層次與可讀性

5. 語氣風格

專業、精確、結構化，避免冗詞贅句。

6. 範例
{
  "product_type": "高性能筆電",
  "target_users": ["電競玩家", "內容創作者"],
  "CPU": {
    "cores": 8,
    "max_frequency": "3.5GHz",
    "architecture": "八核心"
  },
  "RAM": {
    "capacity": "16GB"
  },
  "Storage": {
    "type": "NVMe SSD",
    "capacity": "1TB",
    "advantages": [
      "更快的資料傳輸效率",
      "更低的延遲"
    ]
  }
}
文字內容如下:這款針對電競玩家與內容創作者設計的高性能筆電，
    核心運算單元採用八核心架構，其最高運作頻率可達 3.5GHz，
    在效能與功耗之間取得平衡。
    系統記憶體總容量為 16GB，可支援高強度多工處理與大型遊戲執行。
    儲存部分則配置一顆 1TB 容量的 NVMe 規格固態硬碟，
    相較於傳統 SATA SSD 具備更快的資料傳輸效率與更低的延遲表現。"""})

  for chunk in llm.stream(message):
        print(chunk.content, end="", flush=True)

if __name__ == "__main__":
    main()
