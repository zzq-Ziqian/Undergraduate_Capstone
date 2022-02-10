import pandas as pd

df_date = pd.read_csv('comment_7cluster.csv',usecols=[0,1,3])
date = df_date['Date'].tolist()
date_clean1 = []
date_clean2 = []
for i in date:
    date_clean1.append(i.split()[1])
for i in date:
    date_clean2.append(i.split()[2])
df_date_clean1 = pd.DataFrame(date_clean1)
df_date_clean2 = pd.DataFrame(date_clean2)
df_date['date'] = df_date_clean1 + '-' + df_date_clean2
df = pd.concat([pd.DataFrame(df_date['date']),
               pd.DataFrame(df_date['comment'])],axis=1)
df_normalized = pd.concat([df,pd.DataFrame(df_date['predicted_cluster'])],axis=1)
df_normalized.to_csv('data_clean.csv',index=False)