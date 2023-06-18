import os
import csv
import re
from datetime import datetime

# 定义文件夹路径和输出文件名
folder_path = './news/segmented'
output_file = './utils/origin_output.csv'

# 获取news文件夹下的所有csv文件
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# 按照文件名的日期顺序排序csv文件列表
csv_files.sort(key=lambda x: datetime.strptime(x[:-4], '%Y-%m-%d'))

# 打开输出文件，准备写入数据
with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
    writer = csv.writer(output_csv)

    # 遍历csv文件列表，依次读取并写入输出文件
    for idx, file in enumerate(csv_files):
        file_path = os.path.join(folder_path, file)
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as input_csv:
            reader = csv.reader(input_csv)
            rows = list(reader)  # 读取数据行

        # 按照日期列升序排列，跳过标题行
        sorted_rows = sorted(rows[1:], key=lambda x: datetime.strptime(x[3], '%Y年%m月%d日 %H:%M'), reverse=False)

        # 写入标题行（仅在第一个文件时写入）
        if idx == 0:
            writer.writerow(rows[0])

        # 写入排序后的数据行
        writer.writerows(sorted_rows)

# 读取输出文件并过滤重复行
with open(output_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # 读取标题行
    rows = list(reader)  # 读取数据行

# 获取列索引
content_index = header.index('新闻内容')
# 删除新闻内容为空的行, 删除错误板块名, 删除含数字的板块名
pattern = r'\d'  # 匹配任意数字的正则表达式
rows = [row for row in rows if row[4] and len(row[0]) <= 4 and not re.search(pattern, row[0])]
# 使用集合去除重复行，并按照日期列升序排列
filtered_rows = sorted(set(tuple(row) for row in rows), key=lambda x: datetime.strptime(x[3], '%Y年%m月%d日 %H:%M'))

output_file_filtered = './utils/filtered_output.csv'
# 将过滤后的行写入新的输出文件，包括标题行
with open(output_file_filtered, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(filtered_rows)


