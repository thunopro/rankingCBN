import requests
import json
import os
import time
from datetime import datetime, timedelta

def get_recent_submissions():
    # Đường dẫn file (tính từ gốc thư mục dự án để chạy được trên GitHub Actions)
    handles_path = 'data/handles.json'
    output_path = 'data/recent_activity.json'
    
    if not os.path.exists(handles_path):
        print(f"❌ Không tìm thấy file {handles_path}")
        return

    with open(handles_path, 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    all_data = []
    # Mốc thời gian 10 ngày trước (tính bằng giây)
    ten_days_ago = (datetime.now() - timedelta(days=10)).timestamp()

    for user in users:
        handle = user['handle']
        name = user['name']
        print(f"🔄 Đang lấy dữ liệu cho: {handle} ({name})...")
        
        # Lấy 100 submission gần nhất của mỗi user
        url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=100"
        
        try:
            res = requests.get(url, timeout=10).json()
            if res['status'] == 'OK':
                for sub in res['result']:
                    creation_time = sub['creationTimeSeconds']
                    
                    # Chỉ lấy các bài nộp trong vòng 10 ngày trở lại đây
                    if creation_time >= ten_days_ago:
                        all_data.append({
                            "handle": handle,
                            "name": name,
                            "verdict": sub.get('verdict'),
                            "creationTimeSeconds": creation_time,
                            "problem": f"{sub['problem'].get('contestId')}{sub['problem'].get('index')}"
                        })
            
            # Nghỉ 1 giây giữa các user để tránh bị Codeforces chặn API
            time.sleep(1) 
        except Exception as e:
            print(f"⚠️ Lỗi khi lấy dữ liệu {handle}: {e}")

    # Đảm bảo thư mục data tồn tại
    os.makedirs('data', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã xong! Lưu {len(all_data)} submissions vào {output_path}")

if __name__ == "__main__":
    get_recent_submissions()