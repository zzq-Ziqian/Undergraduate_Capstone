#用SnowNLP进行情感分析
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import jieba
import gensim

df_7cluster = pd.read_csv('comment_7cluster.csv',usecols=[0,1,2,3])
group = df_7cluster.groupby('predicted_cluster')
group_0 = group.get_group(0)
group_1 = group.get_group(1)
group_2 = group.get_group(2)
group_3 = group.get_group(3)
group_4 = group.get_group(4)
group_5 = group.get_group(5)
group_6 = group.get_group(6)


comment = group_6['comment'].astype(str).tolist()
stopwords = {}.fromkeys([line.rstrip() for line in open('D:/BA实习项目/stopword.txt',encoding='utf8')])
word = []
for i in comment:
    element = jieba.cut(i)
    for j in element:
        if j not in stopwords and j!=' ':
            word.append(j)
wcd = WordCloud(background_color='white',font_path='simkai.ttf',width=960,height=960,margin=10,colormap='Reds').generate(' '.join(word))

plt.imshow(wcd)
plt.axis('off')
plt.show()

'''
for i in comment:
    e = []
    element = jieba.cut(i)
    for j in element:   
        if j not in stopwords and j!=' ':
            e.append(j)
    comment_afterdivide.append(e)
'''