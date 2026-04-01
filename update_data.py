import requests
import json
import os

def fetch_gov_data():
    # 香港政府資料一線通的六合彩 API (這是最穩定的來源)
    url = "https://resource.data.one.gov.hk/td/lottery-result/last_30_draw.json"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            
            # 政府資料的結構稍微不同，我們提取第一筆 (最新一期)
            # 註：政府資料通常在開獎後稍有延遲，但對於預測下期頭獎非常穩定
            latest = data[0] 
            
            # 建立你的網頁需要的格式
            # 注意：政府 API 有時不提供「預計頭獎」，若無則預設 800 萬
            next_draw = {
                "jackpot": "8000000", # 預設值
                "date": latest.get('draw_date', '待更新'),
                "id": str(int(latest.get('draw_number', '0')) + 1) # 預測下一期 ID
            }
            
            # 如果你想嘗試從馬會補抓金額，可以在這裡做，但建議先保證檔案不空白
            with open('lotto_data.json', 'w', encoding='utf-8') as f:
                json.dump(next_draw, f, ensure_all_ascii=False, indent=4)
            
            print("政府數據抓取成功！")
        else:
            print(f"伺服器錯誤: {response.status_code}")
    except Exception as e:
        print(f"發生錯誤: {e}")
        # 萬一連政府 API 都掛了，寫入一個保底數據，確保 lotto_data.json 不是空的
        if not os.path.exists('lotto_data.json'):
            with open('lotto_data.json', 'w') as f:
                json.dump({"jackpot": "8000000", "date": "請參考官網", "id": "0"}, f)

if __name__ == "__main__":
    fetch_gov_data()
