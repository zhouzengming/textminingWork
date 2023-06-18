import csv
import random

orig_file = './utils/filtered_output.csv'
picked_file = './utils/train_sample.csv'
test_file = './utils/test_sample.csv'

with open(orig_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # 读取标题行
    rows = list(reader)  # 读取数据行

# 获取板块名
xticks = list({line[0] for line in rows})
# 初始化挑选结果列表
picked_rows = []
# 每个板块名选600条
tick_num = 600
for tick in xticks:
    tick_list = [row for row in rows if row[0] == tick]
    if len(tick_list) < 100:
        continue
    if len(tick_list) > tick_num:
        picked_rows.extend(random.sample(tick_list, tick_num))
    else:
        picked_rows.extend(tick_list)

# 将挑选后的行写入新的输出文件，包括标题行
with open(picked_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(picked_rows)

# 测试集为原数据中任意抽取15000行
test_num = 15000
test_rows = []
for tick in xticks:
    tick_list = [row for row in rows if row[0] == tick]
    if len(tick_list) < 100:
        continue
    test_rows.extend(tick_list)
test_rows = random.sample(test_rows, test_num)

# 将挑选后的行写入新的输出文件，包括标题行
with open(test_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(test_rows)

