import requests
import json
import os

def fetch_data():
    # 直接抓馬會最原始的 JSON 介面
    url = "https://bet.hkjc.com/contentserver/jcbw/cmc/last30draw.json"
    
    # 這是極致偽裝：讓馬會以為你是 Windows 上的 Chrome 瀏覽器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://bet.hkjc.com/lotto/index.aspx?lang=ch',
        'Accept-Language': 'zh-HK,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    print(f"正在嘗試連線馬會官方介面...")
    
    result = {
        "jackpot": "8000000", # 預設保底 800 萬
        "date": "2026-04-02",
        "id": "26/000"
    }

    try:
        # 加上 timeout 防止當掉
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            curr = data.get('currentDraw', {})
            result["jackpot"] = curr.get('estimatedJackpot', '8,000,000').replace(',', '')
            result["date"] = curr.get('drawDate', '待更新')
            result["id"] = curr.get('drawId', 'N/A')
            print(" 成功從馬會官網抓取數據！")
        else:
            print(f" 馬會回傳錯誤代碼: {response.status_code}，使用保底數據。")
            
    except Exception as e:
        print(f" 抓取過程發生問題: {e}，執行自我保護機制。")

    # --- 關鍵：無論如何都寫入檔案 ---
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_all_ascii=False, indent=4)
    
    # 打印出來給你看，確保 Actions 日誌裡有東西
    print(f" 最終寫入內容: {result}")

if __name__ == "__main__":
    fetch_data()
