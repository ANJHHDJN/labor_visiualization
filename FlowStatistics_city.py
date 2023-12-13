import pandas as pd
import numpy as np

list_id = []
list_month = []
list_city = []
list_flow_num = []

df = pd.read_csv('data/data_city.csv', usecols=[0, 1, 41, 42])
df.columns = ['id', 'month', 'identity', 'city']
for i in df.columns:
    df = df[~df[i].isin(['None'])]
df = df[df['identity'].isin([1])]
df = df.drop('identity', axis=1)
df = df.sort_values(by=['id', 'month'])

list_id = list(set(df['id']))
list_month = list(set(df['month']))
list_city = list(set(df['city']))
flow_num = np.zeros((len(list_month), len(list_city), len(list_city)))
flow_num_city = np.zeros((len(list_month), len(list_city), 2))

for i in range(len(list_id)):
    df_id = df[df['id'] == list_id[i]]
    list_message = df_id.values.tolist()
    for j in range(len(list_message)-1):
        if not list_message[j][2] == list_message[j+1][2]:
            flow_num[list_month.index(list_message[j+1][1])][list_city.index(list_message[j][2])][list_city.index(list_message[j+1][2])] += 1

for i in range(len(list_month)):
    for j in range(len(list_city)):
        for k in range(len(list_city)):
            flow_num_city[i][j][0] += flow_num[i][k][j]
            flow_num_city[i][j][1] += flow_num[i][j][k]

list_flow_message=[]
for i in range(len(list_month)):
    list_flow_city = []
    for j in range(len(list_city)):
        di_1 = dict(item=list_city[j], 劳动力流入=flow_num_city[i][j][0], 劳动力流出=flow_num_city[i][j][1])
        list_flow_city.append(di_1)
    di_2 = dict(month=list_month[i], data=list_flow_city)
    list_flow_message.append(di_2)
di = dict(message=list_flow_message)

print(di)
