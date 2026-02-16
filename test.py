import json

def generate_dynamic_table(handle, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            submissions = json.load(f)
        
        # 1. Đảo ngược để tính từ cũ đến mới
        submissions.reverse()
        
        results = {}
        all_problem_indices = set() # Dùng set để lấy danh sách bài tập duy nhất

        for sub in submissions:
            p_idx = sub['problem']
            all_problem_indices.add(p_idx)
            
            if p_idx not in results:
                results[p_idx] = {'ac': False, 'fails': 0}
            
            if results[p_idx]['ac']: continue # Đã AC thì bỏ qua các dòng sau
                
            if sub['verdict'] == 'OK':
                results[p_idx]['ac'] = True
            else:
                results[p_idx]['fails'] += 1

        # 2. Sắp xếp danh sách bài tập theo thứ tự (A, B, C, D...) để làm cột
        sorted_problems = sorted(list(all_problem_indices))

        # 3. Tạo Header động
        header = f"{'Who':<10} |"
        divider = "-" * 11 + "|"
        for p in sorted_problems:
            header += f" {p:^4} |"
            divider += "-----|"

        # 4. Tạo dòng dữ liệu cho User
        row = f"{handle:<10} |"
        for p in sorted_problems:
            data = results[p]
            if data['ac']:
                # AC lần đầu là '+', nộp sai n lần rồi AC là '+n'
                cell = "+" if data['fails'] == 0 else f"+{data['fails']}"
            else:
                # Chưa AC và nộp sai n lần là '-n'
                cell = f"-{data['fails']}" if data['fails'] > 0 else ""
            row += f" {cell:^4} |"

        return f"```\n{header}\n{divider}\n{row}\n```"

    except Exception as e:
        return f"Lỗi: {e}"

# Chạy với file viobow_2194.json của bạn
print(generate_dynamic_table("viobow", "data/viobow_2194.json"))