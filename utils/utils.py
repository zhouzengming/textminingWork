import csv
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as colors

def save_model(model, model_file):
    """
    保存模型为文件
    :param model: 模型
    :param model_file: 模型文件名
    :return: None
    """
    with open(model_file, 'wb') as file:
        pickle.dump(model, file)


def load_model(model_file):
    """
    加载模型
    :param model_file: 模型文件名
    :return: lda模型
    """
    with open(model_file, 'rb') as file:
        lda_model = pickle.load(file)
    return lda_model


def my_heatmap(data, ticks=None, savepath=''):
    """
    热力图绘制
    :param data: 热力图数据矩阵
    :param ticks: [x_ticks, y_ticks]
    :param savepath: 图像保存位置
    :return: None
    """
    # data=np.random.rand(4,6)
    # data[0,1]=1

    # font_path = 'simhei.ttf'
    # my_font = FontProperties(fname=font_path)
    plt.figure(figsize=(30, 8))
    # # 计算每列的最小和最大值
    # column_min = np.min(data, axis=0)
    # column_max = np.max(data, axis=0)
    # # 按列归一化数据
    # data = (data - column_min) / (column_max - column_min)
    # 计算列和
    column_sum = np.sum(data, axis=0)
    # 归一化
    data = np.divide(data, column_sum)
    # 设置中文数据标签的字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 20
    # 绘图
    ax = sns.heatmap(data, cmap='coolwarm', annot=True, fmt=".2f", cbar=True)
    # plt.imshow(data, cmap='coolwarm', aspect='auto', vmin=np.min(data), vmax=np.max(data))
    # 获取热力图中的文本对象
    texts = ax.collections[0].axes.texts
    # 遍历每个文本对象，设置旋转角度为 90 度
    [text.set_rotation(270) for text in texts]
    # 修改标题和轴标
    plt.title('Heatmap')
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')
    plt.subplots_adjust(left=0.05, right=1.1, bottom=0.2, top=0.95)
    if ticks:
        plt.xticks([i for i in range(len(ticks[0]))], ticks[0], rotation=270)
        plt.yticks([i for i in range(len(ticks[1]))], ticks[1], rotation=0)
    if savepath:
        plt.savefig(savepath, dpi=300)
    plt.show()


def analyse_ans(xticks, yticks, rows_withPredict, lda_cluster_Num, output_file=''):
    """
    分析lda结果
    :param xticks:
    :param yticks:
    :param rows_withPredict:
    :param lda_cluster_Num:
    :param output_file:
    :return:
    """
    # 初始化输出行
    header = ['板块名', '样本总量'] + [i for i in range(len(yticks))] + ['分类号', '正确率']
    model_row = ['lda_c' + str(lda_cluster_Num), len(rows_withPredict)]
    model_row.extend([0 for _ in range(lda_cluster_Num + 1)])

    ans_row = []
    # 初始化分类正确数
    clust_curr_num = 0
    # 寻找每个tick对应最多的分类
    for tick in xticks:
        # 筛选tick的行
        tick_rows = [row for row in rows_withPredict if row[0] == tick]
        # 统计分类信息
        row = [tick]
        # tick总数
        tick_sum = len(tick_rows)
        row.append(tick_sum)
        # 统计各分类数
        clust = []
        for i in range(lda_cluster_Num):
            clust.append(sum(row[5] == i for row in tick_rows))
        row.extend(clust)
        # 寻找分类号
        clust_num = clust.index(max(clust))
        row.append(clust_num)
        # 统计分类正确比例
        clust_curr_num += clust[clust_num]
        curr_per = clust[clust_num] / tick_sum
        row.append(curr_per)
        # 加入结果行
        ans_row.append(row)

    # 添加模型准确率
    model_row.append(clust_curr_num / len(rows_withPredict))
    ans_row.insert(0, model_row)

    # 将测试结果写入新的输出文件，包括标题行
    if output_file:
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(ans_row)
