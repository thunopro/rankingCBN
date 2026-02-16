import requests, json, os, time
from dotenv import load_dotenv

load_dotenv()
def get_recent_submissions():
    with open('data/handles.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    all_data = []
    for user in users:
        handle = user['handle']
        print(f"🔄 Đang lấy dữ liệu 10 ngày cho: {handle}...")
        url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=200"
        try:
            res = requests.get(url).json()
            if res['status'] == 'OK':
                for sub in res['result']:
                    # Chỉ lưu các thông tin cần thiết để file nhẹ hơn
                    all_data.append({
                        "handle": handle,
                        "name": user['name'],
                        "verdict": sub.get('verdict'),
                        "creationTimeSeconds": sub['creationTimeSeconds'],
                        "problem": f"{sub['problem'].get('contestId')}{sub['problem'].get('index')}"
                    })
            time.sleep(1) # Tránh bị chặn
        except: pass

    os.makedirs('data', exist_ok=True)
    with open('data/recent_activity.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4)
    print("✅ Đã xong! File: data/recent_activity.json")

if __name__ == "__main__":
    get_recent_submissions()