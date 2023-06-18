import csv
import datetime
import multiprocessing

import jieba
import thulac
import re
import os
import time


def fenci(input_file, output_file, thu):
    with open(input_file, 'r', encoding='utf-8') as input_csv:
        reader = csv.reader(input_csv)
        header = next(reader)  # 读取标题行
        rows = list(reader)
    texts = [row[4] for row in rows]

    ## thulac
    # thu = thulac.thulac(seg_only=True)  # 只进行分词，不进行词性标注
    segmented_texts = [thu.cut(text, text=True) for text in texts]
    # 正则匹配删除符号
    segmented_texts = [re.sub(r'[^\u4e00-\u9fa5]+', ' ', segmented_text) for segmented_text in segmented_texts]
    segmented_texts = [segmented_text.split(' ') for segmented_text in segmented_texts]

    # ## jieba
    # segmented_texts = [jieba.lcut(text) for text in texts]
    # segmented_texts = [[word for word in segmented_text if not re.search(r'[^\u4e00-\u9fa5]+', word)] for segmented_text in segmented_texts]

    # 导入停用词表
    stopwords_path = '../utils/hit_stopwords.txt'
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
    # stopwords转为set,处理速度快很多
    stopwords = set(stopwords)
    # 去除停用词
    filtered_texts = [[word for word in segmented_text if word not in stopwords] for segmented_text in segmented_texts]

    # 文档整合
    segmented_texts = [' '.join(segmented_text) for segmented_text in filtered_texts]

    # 整合为csv
    rows_save = [row[:4] + [segmented_texts[i]] + row[5:] for i, row in enumerate(rows)]

    # 保存
    with open(output_file, 'w', encoding='utf-8', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(header)
        writer.writerows(rows_save)


def thuProcess(csv_files):
    # print(len(csv_files))
    # return
    # 创建thu对象
    thu = thulac.thulac(seg_only=True)  # 只进行分词，不进行词性标注
    for file in csv_files:
        input_file = "../news/"+file
        output_file = "../news/segmented/"+file
        fenci(input_file, output_file, thu)
    print("Process finished.")


def split_list(lst, num_parts):
    avg_length = len(lst) // num_parts  # 平均每份的长度
    remainder = len(lst) % num_parts  # 余数，用于处理无法平均分的情况

    result = []  # 存储分割后的列表

    start = 0  # 分割的起始位置
    for i in range(num_parts):
        length = avg_length + (i < remainder)  # 每份的长度，如果 i 小于余数，则长度加1
        end = start + length  # 分割的结束位置
        result.append(lst[start:end])  # 将分割后的部分添加到结果列表中
        start = end  # 更新下一份的起始位置

    return result


if __name__ == '__main__':
    # 获取当前文件夹下的所有文件
    files = os.listdir("../news")
    # 过滤出所有的.csv文件
    csv_files = [file for file in files if file.endswith('.csv')]
    # 分为max_process份
    max_processes = 10
    csv_files = split_list(csv_files, max_processes)
    # 创建进程池
    pool = multiprocessing.Pool(processes=max_processes)
    # 添加任务
    for i in range(len(csv_files)):
        pool.apply_async(func=thuProcess, args=(csv_files[i],))
        time.sleep(10)
    # 等待子进程结束
    pool.close()
    pool.join()


