import numpy as np
import pandas as pd

# =========== Task 1: Prompt user for a filename and open it; retry on failure. ===========

while True:
    filename_input = input('Enter a class to grade (i.e. class1 for class1.txt): ')
    filename = filename_input.strip() + '.txt'
    try:
        file = open(filename,'r')
        print(f'Successfully opened {filename}')
        break
    except FileNotFoundError:
        print('File cannot be found.')


# =========== Task 2: Check if data is in correct format ===========
lines = file.readlines()
valid_records = []
invalid_count = 0
errors_found = False

print('\n**** ANALYZING ****\n')

for line in lines:
    line = line.strip()
    
    if not line:
        continue
    
    fields = line.split(',')
    # Check if there are exactly 26 fields (1 student ID + 25 answers)
    if len(fields) != 26:
        invalid_count += 1
        errors_found = True
        print(f'Invalid line of data: does not contain exactly 26 values:{line}')
        continue
    
    # Validate student ID format
    student_id = fields[0]

    if student_id[0] != 'N' or len(student_id) != 9 or not student_id[1:].isdigit():
        invalid_count += 1
        errors_found = True
        print('abc')
        print(
            f'Invalid line of data: student ID does not start with "N" followed by 8 digits:{line}'
            )
        continue

    # If we reach this point, the line is valid
    answers = fields[1:]
    valid_records.append([student_id, answers])

# If no errors were found, print a message indicating that
if not errors_found:
    print('No errors found!')

# Print the report of valid and invalid lines

print('\n**** REPORT ****\n')
print(f'Total valid lines of data: {len(valid_records)}')
print(f'Total invalid lines of data: {invalid_count}\n')


# =========== Task 3 with NUMPY: Grade the exams and output results to a file. ===========

# Define constants for grading
ANSWER_KEY = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(",")
NUM_QUESTIONS = 25
SCORE_CORRECT = 4
SCORE_WRONG = -1
SCORE_SKIP = 0
HIGH_SCORE_THRESHOLD = 80

# Initialize lists and arrays for grading results
scores = []
grade_results = []

# Initialize arrays to count skips and wrong answers for each question.
# Must be arrays to be able to use numpy for counting and calculating vectors.
skip_counts = np.zeros(NUM_QUESTIONS, dtype=int)
wrong_counts = np.zeros(NUM_QUESTIONS, dtype=int)

for student_id, answers in valid_records:
    score = 0
    skipped = []
    wrong = []

    for i in range(NUM_QUESTIONS):
        if answers[i] == ANSWER_KEY[i]:
            score += SCORE_CORRECT 
        elif answers[i] == '':
            score += SCORE_SKIP 
            skip_counts[i] += 1 
            skipped.append(i+1) 
        elif answers[i] != ANSWER_KEY[i]: 
            score += SCORE_WRONG 
            wrong_counts[i] += 1 
            wrong.append(i+1) 

    scores.append(score) 
    grade_results.append((student_id, score)) 

scores_arr = np.array(scores)
n = len(scores_arr) 

# 3.1 số lượng học sinh có điểm cao hơn ngưỡng điểm cao (theo đề bài là 80)
high_score_count = int(np.sum(scores_arr > HIGH_SCORE_THRESHOLD))
print(f'Number of students scoring higher than {HIGH_SCORE_THRESHOLD}: {high_score_count}\n')

# 3.2 tính điểm trung bình của tất cả học sinh và làm tròn đến 3 chữ số thập phân
mean_score = round(float(np.mean(scores_arr)), 3)
print(f'Mean score: {mean_score}\n')

# 3.3 điểm cao nhất của tất cả học sinh và chuyển sang kiểu int
highest = int(np.max(scores_arr))
print(f'Hightest score: {highest}\n')

# 3.4 điểm thấp nhất của tất cả học sinh và chuyển sang kiểu int
lowest = int(np.min(scores_arr))
print(f'Lowest score: {lowest}\n')

# 3.5 Miền giá trị của điểm = điểm cao nhất - điểm thấp nhất
score_range = highest - lowest
print(f'Score range: {score_range}\n')

# 3.6 tính điểm trung vị
sorted_scores = np.sort(scores_arr) # sắp xếp điểm của tất cả học sinh theo thứ tự tăng dần
if n % 2 == 1: # nếu số lượng học sinh là số lẻ 
    median = float(sorted_scores[n // 2]) # 3.6.1 thì điểm trung vị là điểm của học sinh ở vị trí giữa
else: # nếu số lượng học sinh là số chẵn
    mid1 = sorted_scores[n // 2 - 1] # điểm của học sinh ở vị trí giữa thứ nhất
    mid2 = sorted_scores[n // 2] # điểm của học sinh ở vị trí giữa thứ hai
    median = round((int(mid1) + int(mid2)) / 2, 3) # 3.6.2 điểm trung vị = (điểm của học sinh ở vị trí giữa thứ nhất + điểm của học sinh ở vị trí giữa thứ hai) / 2


# 3.7 Câu bị bỏ nhiều nhất
max_skip = int(np.max(skip_counts))   # số lớn nhất trong skip_counts là số lượng câu bi bỏ nhiều nhất, sl học sinh bỏ câu này
skip_ratio = round(max_skip / n, 3)   # tỉ lệ số câu bị bỏ nhiều nhất trên tổng số học sinh, được tính bằng số lượng câu bị bỏ nhiều nhất chia cho tổng số học sinh và làm tròn đến 3 chữ số thập phân

skip_parts = []

for i in range(NUM_QUESTIONS):
    if skip_counts[i] == max_skip: # nếu số lượng câu bị bỏ của câu hỏi này bằng số lượng câu bị bỏ nhiều nhất
        skip_parts.append(f'thứ tự: {i+1} - số lượng hs: {max_skip} - tỉ lệ: {skip_ratio*100}%') # thì thêm thông tin của câu hỏi này vào danh sách các câu bị bỏ nhiều nhất (thứ tự câu hỏi bắt đầu từ 1)

print('Question that most people skip:')
for part in skip_parts:
    print(part)



# 3.8 Câu bị sai nhiều nhất
max_wrong = int(np.max(wrong_counts))
wrong_ratio = round(max_wrong / n, 3)

wrong_parts = [] 
for i, count in enumerate(wrong_counts, start=1):
    if count == max_wrong:
        wrong_parts.append(f'thứ tự: {i} - số lượng hs: {max_wrong} - tỉ lệ: {wrong_ratio*100}%')
print(f"\nQuestion that most people answer incorrectly:\n{'\n'.join(wrong_parts)}")





# =========== Task 3 with PANDAS: Grade the exams and output results to a file. ===========

# Chuyển [list] valid_records về dạng DataFrame để xử lý bằng Pandas
df = pd.DataFrame(valid_records, columns=['student_id', 'answers'])

# Chuyển [list] answers về dạng DataFrame để xử lý bằng Pandas
answers_df = pd.DataFrame(df['answers'].tolist(), columns=[f'Q{i}' for i in range(1, 26)])

# Tính điểm từng câu cho từng học sinh
score_df = pd.DataFrame() # tạo DataFrame để lưu điểm từng câu của từng học sinh
for i in range(NUM_QUESTIONS): # duyệt qua từng câu hỏi (từ 0 đến 24)
    col = f'Q{i+1}' # tên cột tương ứng với câu hỏi (bắt đầu từ Q1 đến Q25)
    scores_col = [] # tạo biến danh sách điểm của câu hỏi này cho tất cả học sinh
    for ans in answers_df[col]: # duyệt qua từng câu trả lời của học sinh trong cột câu hỏi này
        if ans == ANSWER_KEY[i]: # nếu câu trả lời của học sinh này đúng với đáp án của câu hỏi này
            scores_col.append(SCORE_CORRECT) # thì thêm điểm SCORE_CORRECT (theo đề bài là 4) vào danh sách điểm của câu hỏi này
        elif ans == '': # nếu câu trả lời của học sinh này bị bỏ qua
            scores_col.append(SCORE_SKIP) # thì thêm điểm SCORE_SKIP (theo đề bài là 0) vào danh sách điểm của câu hỏi này
        else: #
            scores_col.append(SCORE_WRONG) # nếu câu trả lời của học sinh này sai thì thêm điểm SCORE_WRONG (theo đề bài là -1) vào danh sách điểm của câu hỏi này
    score_df[col] = scores_col # thêm cột điểm của câu hỏi này vào DataFrame điểm từng câu của từng học sinh

n = len(df)

# Tính tổng điểm từng học sinh
total_scores = [] # tạo biến danh sách điểm tổng của từng học sinh
for i in range(len(score_df)): # duyệt qua từng học sinh (từ 0 đến n-1) để tính tổng điểm của học sinh này
    total = 0 # tạo biến điểm tổng ban đầu của học sinh này = 0
    for col in score_df.columns: # duyệt qua từng cột điểm của từng câu để cộng vào điểm tổng của học sinh này
        total += score_df[col].iloc[i] # cộng điểm của câu hỏi này vào điểm tổng của học sinh này
    total_scores.append(total) # thêm điểm tổng của học sinh này vào danh sách điểm tổng của tất cả học sinh

df['score'] = total_scores # thêm cột điểm tổng của từng học sinh vào DataFrame chính


# 3.1 Số học sinh đạt điểm cao (>80)

# 3.2 Điểm trung bình
mean_score = round(float(df['score'].mean()), 3) 
print(f'\n\nTASK 3 WITH PANDAS:\n\nMean (average) score (PANDAS): {mean_score:.3f}')

# 3.3 Điểm cao nhất
highest = int(df['score'].max())
print(f'Highest score (PANDAS): {highest}')

# 3.4 Điểm thấp nhất
lowest = int(df['score'].min())
print(f'Lowest score (PANDAS): {lowest}')

# 3.5 Miền giá trị
score_range = highest - lowest
print(f'Range of scores (PANDAS): {score_range}')

# 3.6 Trung vị
sorted_scores = df['score'].sort_values().values
if n % 2 == 1:
    median = round(float(sorted_scores[n // 2]),3)
else:
    median = round((int(sorted_scores[n // 2 - 1]) + int(sorted_scores[n // 2])) / 2,3)

if median == int(median):
    median_str = str(int(median))
else:
    median_str = str(median)
print(f'Median score (PANDAS): {median_str}\n')

# 3.7 Câu bị bỏ nhiều nhất
skip_counts = (answers_df == '').sum()
max_skip = int(skip_counts.max())
skip_ratio = round(max_skip / n, 3)
print('Question that most people skip (PANDAS):')
for i in range(NUM_QUESTIONS):
    if skip_counts.iloc[i] == max_skip:
        print(f'{i+1} - {max_skip} - {skip_ratio}')

# 3.8 Câu bị sai nhiều nhất
wrong_counts = (score_df == SCORE_WRONG).sum()
max_wrong = int(wrong_counts.max())
wrong_ratio = round(max_wrong / n, 3)
print('\nQuestion that most people answer incorrectly (PANDAS):')
for i in range(NUM_QUESTIONS):
    if wrong_counts.iloc[i] == max_wrong:
        print(f'{i+1} - {max_wrong} - {wrong_ratio}')


# =========== Task 4: Write student IDs and scores to output file. ===========

output_filename = filename_input.strip() + "_grades.txt"
with open(output_filename, "w") as f:
    for student_id, score in grade_results:
        f.write(f"{student_id},{score}\n")