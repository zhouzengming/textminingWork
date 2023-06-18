import csv
import os
import re
import matplotlib.pyplot as plt

# 读取文件夹下所有csv文件（模型输出）的模型行（1行）最后一列（-1列）为x,y并绘制折线图

points={}

output_dir = "./outputs/"
savepath = "./outputs/accuracy.png"
# 获取当前文件夹下的所有文件
files = os.listdir(output_dir)
# 过滤出所有的.csv文件
csv_files = [file for file in files if file.endswith('.csv')]
for csv_file in csv_files:
    with open(output_dir+csv_file, 'r', encoding='utf-8')as file:
        reader = csv.reader(file)
        _ = next(reader)
        line = next(reader)
        match = re.search(r'\d+$', line[0])
        x = float(match.group())
        y = float(line[-1])
        points.update({x: y})
# 排序为x升序
sorted_points = sorted(points.items(), key=lambda x: x[0])  # 按照键升序排序
# 获取x,y
x = [point[0] for point in sorted_points]
y = [point[1] for point in sorted_points]
# 设置图像大小
plt.figure(figsize=(9, 4))
# 设置中文数据标签的字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10
plt.xlabel('分类数')
plt.ylabel('准确率')
plt.title('模型准确率')
plt.bar(x, y)
plt.savefig(savepath, dpi=300)
plt.show()
