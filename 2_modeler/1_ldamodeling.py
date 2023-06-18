import csv
import thulac
from gensim import corpora, models
import re
import jieba
import multiprocessing
import numpy as np
import random
from utils import *
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
# from pytagcloud import create_tag_image, make_tags


def lda_build(texts, num_topics):
    """

    :param texts: 文档列表
    :return: lda模型
    """
    print("training lda...")
    segmented_texts = [segmented_text.split(' ') for segmented_text in texts]

    dictionary = corpora.Dictionary(segmented_texts)
    corpus = [dictionary.doc2bow(filtered_text) for filtered_text in segmented_texts]
    # 保存词典
    output_file = './models/dictionary_c' + str(num_topics) + '.pkl'
    save_model(dictionary, output_file)

    # 训练模型
    np.random.seed(42)
    random.seed(42)
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=40)
    for topic in lda_model.print_topics():
        print(topic)
    # 保存模型
    output_file = './models/lda_c' + str(num_topics) + '.pkl'
    save_model(lda_model, output_file)

# 获取分类
def get_document_topic(lda_model, document_vector):
    """
    将词袋放入lda模型预测分类
    :param lda_model:
    :param document_vector:
    :return:
    """
    document_topics = lda_model.get_document_topics(document_vector)
    sorted_topics = sorted(document_topics, key=lambda x: x[1], reverse=True)
    top_topic = sorted_topics[0]
    return top_topic[0]

def model_test(rows, lda_model, dictionary):
    """
    通过lda模型预测分类
    :param rows: 分词后csv文件的数据行
    :param lda_model: 要使用的lda模型
    :param dictionary: 构造lda模型时的词典
    :return: 分类结果向量
    """
    # 获取文档
    texts = [row[4] for row in rows]
    # 分成词
    segmented_texts = [segmented_text.split(' ') for segmented_text in texts]
    # 文档转为词袋
    corpus = [dictionary.doc2bow(filtered_text) for filtered_text in segmented_texts]
    # 测试文档分类
    predicted_topics = [get_document_topic(lda_model, document_vector) for document_vector in corpus]

    return predicted_topics


def lda_test(lda_cluster_Num, test_sample = ""):
    flag = 0
    if test_sample:
        flag = 1
    else:
        test_sample = "./utils/test_sample.csv"
    # 验证一个模型
    print("testing lda...")
    # 加载验证集
    # test_sample = "./utils/test_sample.csv"
    with open(test_sample, 'r', encoding='utf-8')as file:
        reader = csv.reader(file)
        _ = next(reader)  # 读取标题行
        rows = list(reader)  # 读取数据行
    lda_model = load_model('./models/lda_c'+str(lda_cluster_Num)+'.pkl')
    dictionary = load_model('./models/dictionary_c'+str(lda_cluster_Num)+'.pkl')
    predict = model_test(rows, lda_model, dictionary)

    rows_withPredict = [row + [predict[i]] for i, row in enumerate(rows)]

    # 构造x、y轴标签
    xticks = list({line[0] for line in rows_withPredict})
    yticks = [i for i in range(lda_cluster_Num)]

    data = np.zeros((len(yticks), len(xticks)))
    for i in range(len(rows_withPredict)):
        x = xticks.index(rows_withPredict[i][0])
        y = rows_withPredict[i][5]
        data[y, x] += 1
    # 绘图
    my_heatmap(data, [xticks, yticks], './outputs/check_c'+str(lda_cluster_Num)+'.png')

    # 分析
    # xticks, yticks, rows_withPredict, lda_cluster_Num
    if flag:
        output_file = './outputs/full_lda_c' + str(lda_cluster_Num) + '.csv'
    else:
        output_file = './outputs/lda_c' + str(lda_cluster_Num) + '.csv'
    analyse_ans(xticks, yticks, rows_withPredict, lda_cluster_Num, output_file)

    # 绘制词云
    # 从LDA模型的print_topics()返回的数据中提取主题词和权重
    topics = lda_model.print_topics(num_words=200)  # 每个主题显示10个词
    # 构建词云文本
    for i in range(len(topics)):
        topic = topics[i]
        wordcloud_text = ' '.join([word for word in topic[1].split(' + ')])
        # 创建词云对象
        # wordcloud = WordCloud(font_path='wqy-zenhei.ttc', width=800, height=600)
        wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=600, background_color='white')
        # 生成词云图像
        wordcloud.generate(wordcloud_text)
        # 显示词云图像
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        if flag:
            plt.savefig("./outputs/full_lda_c" + str(lda_cluster_Num) + "_wordcloud_c" + str(i) + ".png", dpi=600)
        else:
            plt.savefig("./outputs/lda_c"+str(lda_cluster_Num)+"_wordcloud_c"+str(i)+".png", dpi=600)
        plt.show()





if __name__ == "__main__":
    """
    读取并处理已分好词的文件
    """
    # 读取文件并格式化
    input_file = "./utils/train_sample.csv"
    with open(input_file, 'r', encoding='utf-8') as input_csv:
        reader = csv.reader(input_csv)
        header = next(reader)  # 读取标题行
        rows = list(reader)
    texts = [row[4] for row in rows]
    # 多线程训练lda 2-13类模型
    max_processes = 6
    # 创建线程池
    pool = multiprocessing.Pool(processes=max_processes)
    # 添加任务
    for lda_cluster_Num in range(2, 14):
        pool.apply_async(func=lda_build, args=(texts, lda_cluster_Num,))
    # 等待子线程结束
    pool.close()
    pool.join()

    # 多线程验证lda 2-13类模型
    max_processes = 6
    # 创建线程池
    pool = multiprocessing.Pool(processes=max_processes)
    # 添加任务
    for lda_cluster_Num in range(2, 14):
        pool.apply_async(func=lda_test, args=(lda_cluster_Num,))
    # 等待子线程结束
    pool.close()
    pool.join()
    print("lda modeling finished!")

    # 全数据集验证
    lda_test(3, "./utils/filtered_output.csv")
