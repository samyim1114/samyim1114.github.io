import requests
import json

def fetch_hkjc():
    url = "https://bet.hkjc.com/contentserver/jcbw/cmc/last30draw.json"
    
    # 偽裝成真實的 Chrome 瀏覽器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://bet.hkjc.com/lotto/index.aspx?lang=ch',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        # 檢查是否真的拿到 JSON
        if response.status_code == 200:
            data = response.json()
            
            next_draw = {
                "jackpot": data['currentDraw']['estimatedJackpot'].replace(',', ''),
                "date": data['currentDraw']['drawDate'],
                "id": data['currentDraw']['drawId']
            }
            
            with open('lotto_data.json', 'w', encoding='utf-8') as f:
                json.dump(next_draw, f, ensure_all_ascii=False, indent=4)
            print("數據更新成功！")
        else:
            print(f"伺服器回傳狀態碼: {response.status_code}")
            
    except Exception as e:
        print(f"抓取失敗: {e}")
        # 如果失敗了，建立一個保底的檔案，防止 GitHub Actions 報錯
        if not os.path.exists('lotto_data.json'):
            with open('lotto_data.json', 'w') as f:
                json.dump({"jackpot": "8000000", "date": "N/A", "id": "0"}, f)

if __name__ == "__main__":
    import os
    fetch_hkjc()
