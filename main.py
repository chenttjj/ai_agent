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
        {"role": "system", "content": """ 你是一位 人才資料分析師。以下為【學生自我介紹】，請 只依原文 用繁體中文條列萃取：① 興趣與關注主題 ② 技能／經驗／學習線索 ③ 價值觀與理想工作條件 ④ 疑慮或卡關。勿臆測文中沒有的事實，勿在此步推薦職業或打分。
（下接 §2 整段）"""},
        {"role": "user", "content": """
        我是一名高二學生，目前對未來的方向有點迷惘。
我從小就很喜歡玩電腦和研究科技產品，像是組裝電腦、研究手機規格，甚至會看一些 AI 或科技相關的 YouTube 頻道。我對新技術很好奇，例如最近我在研究生成式 AI 和自動化工具。
在學校裡，我的數學和資訊課成績通常不錯，也學過一點 Python，曾經寫過一個小程式幫家裡整理帳目。不過我不太確定自己是不是適合當工程師，因為有時候寫程式卡住會讓我很挫折。
除了科技，我其實也很喜歡觀察人和社會。例如我很喜歡看一些心理學或行為經濟學的內容，也會思考為什麼有些 APP 或網站會讓人一直想使用。
我平常也會幫社團做海報或設計簡單的圖，像是活動宣傳圖或簡單的 logo。我覺得設計和創意的過程很有趣。
個性方面，我是一個比較內向的人，比較喜歡自己研究東西，而不是一直跟很多人社交。但如果是討論一個有趣的問題，我其實可以聊很久。
不過我常常覺得自己沒有什麼特別厲害的專長，因為很多事情我都只學到一點點。
如果說我希望未來的工作，我大概會希望：

可以持續學習新技術
有機會創造新的東西
不要只是一直做重複的事情
最好可以做出對很多人有幫助的產品
        """}
    ]
    
    # 執行串流回應
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)

if __name__ == "__main__":
    main()
