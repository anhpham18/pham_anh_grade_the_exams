# pham_anh_grade_the_exams
Exam Grading Program

## Mô tả

Chương trình chấm điểm bài thi từ các file dữ liệu từng lớp học,
Phân tích tính hợp lệ của dữ liệu, và xuất kết quả chấm điểm vô file .txt theo từng lớp.

## Yêu cầu

- Python 3.9+
- numpy
- pandas

## Cách chạy

1. Đặt file `pham_anh_grade_the_exams.py` **cùng thư mục** với các file dữ liệu
   (`class1.txt`, `class2.txt`, ...).

2. Chạy chương trình:

   ```
   python pham_anh_grade_the_exams.py
   ```

3. Nhập tên class khi được yêu cầu (ví dụ: `class1` cho `class1.txt`):

   ```
   Enter a class to grade (i.e. class1 for class1.txt): class1
   ```

4. Chương trình sẽ:
   - Mở và xác thực file dữ liệu
   - In báo cáo phân tích và thống kê ra màn hình
   - Tạo file kết quả `<classname>_grades.txt` cùng thư mục

## Quy tắc chấm điểm

| Kết quả | Điểm |
| ------- | ---- |
| Đúng    | +4   |
| Bỏ qua  | 0    |
| Sai     | -1   |

## Định dạng dữ liệu hợp lệ

Mỗi dòng phải có đúng **26 giá trị** phân tách bằng dấu phẩy và:

- Cột 1: Mã sinh viên — `N` + 8 chữ số (ví dụ: `N00000001`)
- Cột 2–26: Câu trả lời (`A`–`D`), bỏ trống nếu bỏ qua câu hỏi

## Ví dụ output

```
Successfully opened class1.txt

**** ANALYZING ****

No errors found!

**** REPORT ****

Total valid lines of data: 20
Total invalid lines of data: 0

Total student of high scores: 6
Mean (average) score: 75.60
Highest score: 91
Lowest score: 59
Range of scores: 32
Median score: 73

Question that most people skip: 3 - 4 - 0.2 , 5 - 4 - 0.2 , 23 - 4 - 0.2
Question that most people answer incorrectly: 10 - 4 - 0.2 , 14 - 4 - 0.2 , ...
```
