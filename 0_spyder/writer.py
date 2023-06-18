import csv
import os

def write(filename, data):
    # 检查文件是否存在
    file_exists = os.path.isfile(filename)

    # 打开文件并创建 CSV writer 对象
    with open(filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # 如果文件不存在，则写入表头
        if not file_exists:
            writer.writerow(['板块名', '标题', '作者', '日期', '新闻内容'])

        # 写入数据
        writer.writerows([data])