import pandas as pd
import numpy as np
import gensim
import jieba

df_data = pd.read_csv('comment_data.csv',header=None,names=['Date','user_id','user_name','comment'])
df_data_afterdrop = df_data.drop_duplicates().reset_index(drop=True)
#print(df_data_afterdrop)
#df_data_afterdrop.to_csv('',index=False)

comment = df_data_afterdrop['comment'].astype(str).tolist()
stopwords = {}.fromkeys([line.rstrip() for line in open('D:/BA实习项目/stopword.txt',encoding='utf8')])
comment_afterdivide = list()

for i in comment:
    e = []
    element = jieba.cut(i)
    for j in element:
        if j not in stopwords and j!=' ':
            e.append(j)
    comment_afterdivide.append(e)
#df_comment_afterdivide = pd.DataFrame(comment_afterdivide)
#print(df_comment_afterdivide)

model = gensim.models.KeyedVectors.load_word2vec_format('D:/BA实习项目/pre-train model/baike_26g_news_13g_novel_229g.bin', binary=True)

vecs_sentence = []
for sentence in comment_afterdivide:
    vecs_word = np.array(np.zeros(128,dtype='float64'))
    count = 0
    for word in sentence:
        try:
            count = count+1
            vecs_word = model[word]+vecs_word
        except KeyError:
            continue
    if count!=0:
        vecs_word = vecs_word/count
        vecs_sentence.append(vecs_word)
    else:
        vecs_sentence.append(np.zeros(128,dtype='float64'))
    #vecs_sentence.append(vecs_word)
df_vecs_sentence = pd.DataFrame(vecs_sentence)
data_input = np.array(vecs_sentence)
df_all = pd.concat([df_data_afterdrop,df_vecs_sentence],axis=1)
df_all_clear = df_all.drop(df_all[df_all[100].isin([0])].index).reset_index(drop=True)
df_vector = pd.DataFrame(df_all_clear,columns=[x for x in range(128)])

#利用nltk做Kmeans主题聚类
from nltk.cluster.kmeans import KMeansClusterer
import nltk

obj = KMeansClusterer(num_means=7, distance=nltk.cluster.util.cosine_distance,avoid_empty_clusters=True)
vectors = [np.array(f) for f in df_vector.values]
df_vector['predicted_cluster'] = obj.cluster(vectors,assign_clusters=True)

df_vector['centroid'] = df_vector['predicted_cluster'].apply(lambda x:obj.means()[x])
#df_vector['topic'] = df_vector['centroid'].apply(lambda x:model.similar_by_vector(x,topn=3))

df_cluster = pd.concat([pd.DataFrame(df_all_clear,columns=['Date','comment']),pd.DataFrame(df_vector,columns=['centroid','predicted_cluster'])],axis=1)
#print(df_cluster)
df_cluster.to_csv('comment_7cluster.csv',index=False)

for i in obj.means():
    key_vector = model.similar_by_vector(i, topn=3)
    print(key_vector)

'''
#用SnowNLP进行情感分析
from wordcloud import WordCloud
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import jieba
group = df_cluster.groupby('predicted_cluster')
group_0 = group.get_group(0)
group_1 = group.get_group(1)
group_2 = group.get_group(2)
group_3 = group.get_group(3)
group_4 = group.get_group(4)
group_5 = group.get_group(5)
group_6 = group.get_group(6)
'''


