import pandas as pd

def save_csv(group_mean, group_count, file_name):
    date_list_1 = []
    score_list = []
    date_list_2 = []
    count_list = []
    for k, v in group_mean.items():
        date_list_1.append(k)
        score_list.append(v)
    for i, j in group_count.items():
        date_list_2.append(i)
        count_list.append(j)
    #print(count_list)
    a = {'date':date_list_1,'score':score_list,'count':count_list}
    df = pd.DataFrame(a)
    df.to_csv(file_name,index=False)

df_score = pd.read_csv('score.csv', names=['score'], skiprows=1)
df_data_clean = pd.read_csv('data_clean.csv', usecols=[0, 2])
df_data = pd.concat([df_data_clean, df_score], axis=1)
#print(df_data)
group = df_data.groupby('predicted_cluster')
group_0 = group.get_group(0)
group_1 = group.get_group(1)
group_2 = group.get_group(2)
group_3 = group.get_group(3)
group_4 = group.get_group(4)
group_5 = group.get_group(5)
group_6 = group.get_group(6)
#print(group_0)

group_all_mean = df_data.groupby('date').mean()['score']
group_0_mean = group_0.groupby('date').mean()['score']
group_1_mean = group_1.groupby('date').mean()['score']
group_2_mean = group_2.groupby('date').mean()['score']
group_3_mean = group_3.groupby('date').mean()['score']
group_4_mean = group_4.groupby('date').mean()['score']
group_5_mean = group_5.groupby('date').mean()['score']
group_6_mean = group_6.groupby('date').mean()['score']

group_all_count = df_data.groupby('date').count()['score']
group_0_count = group_0.groupby('date').count()['score']
group_1_count = group_1.groupby('date').count()['score']
group_2_count = group_2.groupby('date').count()['score']
group_3_count = group_3.groupby('date').count()['score']
group_4_count = group_4.groupby('date').count()['score']
group_5_count = group_5.groupby('date').count()['score']
group_6_count = group_6.groupby('date').count()['score']
#print(group_0_final)
save_csv(group_all_mean,group_all_count,'all.csv')
