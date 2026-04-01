import requests
import json
import os

def fetch_hkjc():
    url = "https://bet.hkjc.com/contentserver/jcbw/cmc/last30draw.json"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # 提取下一期資訊
        next_draw = {
            "jackpot": data['currentDraw']['estimatedJackpot'].replace(',', ''),
            "date": data['currentDraw']['drawDate'],
            "id": data['currentDraw']['drawId']
        }
        
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(next_draw, f, ensure_all_ascii=False, indent=4)
        print("數據更新成功！")
    except Exception as e:
        print(f"抓取失敗: {e}")

if __name__ == "__main__":
    fetch_hkjc()
