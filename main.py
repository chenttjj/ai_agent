import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def load_system_prompt():
    """
    從專案根目錄讀取 SOUL.md 與 USER.md 並組合成 system prompt。
    """
    # 取得當前檔案所在的目錄（確保從腳本位置讀取）
    base_dir = os.path.dirname(os.path.abspath(__file__))
    soul_path = os.path.join(base_dir, "SOUL.md")
    user_md_path = os.path.join(base_dir, "USER.md")
    
    try:
        soul_content = ""
        if os.path.exists(soul_path):
            with open(soul_path, "r", encoding="utf-8") as f:
                soul_content = f.read()
        
        user_content = ""
        if os.path.exists(user_md_path):
            with open(user_md_path, "r", encoding="utf-8") as f:
                user_content = f.read()
                
        # 組合成 system prompt
        prompts = []
        if soul_content:
            prompts.append(soul_content)
        if user_content:
            prompts.append(user_content)
            
        if not prompts:
            return "你是一位專業的 AI 助理。"
            
        return "\n\n---\n\n".join(prompts)
        
    except Exception as e:
        print(f"Error loading prompt files: {e}")
        return "你是一位專業的 AI 助理。"

def main():
    # 初始化 LLM (根據原本設定)
    llm = ChatOpenAI(
        model="gemma3:27b",
        base_url="http://203.71.78.31:8000/v1",
        api_key="sk-12345678", # 注意：實際使用應放於 .env
        temperature=0.0,
    )
    
    # 1. 讀入並組合成 system prompt
    system_prompt = load_system_prompt()
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "用第一人稱自我介紹,並說明你會如何協助我"}
    ]
    
    # 執行串流回應
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)

if __name__ == "__main__":
    main()
