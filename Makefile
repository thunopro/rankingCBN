# Biến định nghĩa các lệnh chạy
PYTHON = python
SRC_DIR = src/cogs
DATA_DIR = data

# Lệnh mặc định khi gõ 'make'
all: update_problems update_submissions

# 1. Lấy danh sách bài tập của contest (Chỉ chạy 1 lần khi đổi contest)
update_problems:
	@echo "--- Đang lấy cấu trúc bài tập từ Codeforces ---"
	$(PYTHON) $(SRC_DIR)/get_problem.py

# 2. Lấy toàn bộ bài nộp của nhóm và gộp vào file JSON tổng
update_submissions:
	@echo "--- Đang tải và gộp dữ liệu bài nộp của cả nhóm ---"
	$(PYTHON) $(SRC_DIR)/get_submission_handle.py

# 3. Lệnh xóa dữ liệu cũ để làm mới hoàn toàn
clean:
	@echo "--- Đang dọn dẹp dữ liệu cũ ---"
	rm -rf $(DATA_DIR)/*.json
	@echo "Đã xóa sạch các file JSON trong folder data."

# 4. Lệnh chạy nhanh: Dọn dẹp -> Lấy bài tập -> Lấy bài nộp
refresh: clean all