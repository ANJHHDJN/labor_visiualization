import pandas as pd
import numpy as np

list_id = []
list_month = []
list_city = []
list_flow_num = []
longitude_latitude = {
    '昆明市': {
        'longitude_out': 102.73,
        'latitude_out': 25.04,
        'longitude_in': 102.48,
        'latitude_in': 25.21
    },
    '昭通市': {
        'longitude_out': 103.7,
        'latitude_out': 27.12,
        'longitude_in': 103.63,
        'latitude_in':28.22
    },
    '曲靖市': {
        'longitude_out': 103.79,
        'latitude_out': 25.51,
        'longitude_in': 104.09,
        'latitude_in': 26.24
    },
    '玉溪市': {
        'longitude_out': 102.52,
        'latitude_out': 24.35,
        'longitude_in': 102.93,
        'latitude_in': 24.26
    },
    '普洱市': {
        'longitude_out': 101,
        'latitude_out': 22.79,
        'longitude_in': 101.03,
        'latitude_in': 23.07
    },
    '临沧市': {
        'longitude_out': 100.09,
        'latitude_out': 23.88,
        'longitude_in': 100.12,
        'latitude_in': 24.44
    },
    '保山市': {
        'longitude_out': 99.18,
        'latitude_out': 25.12,
        'longitude_in': 99.15,
        'latitude_in': 24.69
    },
    '丽江市': {
        'longitude_out': 100.25,
        'latitude_out': 26.86,
        'longitude_in': 101.24,
        'latitude_in': 26.63
    },
    '文山州': {
        'longitude_out': 104.24,
        'latitude_out': 23.37,
        'longitude_in':105.09,
        'latitude_in': 24.05
    },
    '红河州': {
        'longitude_out': 103.43,
        'latitude_out': 23.41,
        'longitude_in': 103.41,
        'latitude_in': 23.36
    },
    '西双版纳州': {
        'longitude_out': 100.79,
        'latitude_out': 22,
        'longitude_in': 100.5,
        'latitude_in': 21.95
    },
    '楚雄州': {
        'longitude_out': 101.54,
        'latitude_out': 25.01,
        'longitude_in':101.85,
        'latitude_in': 25.7
    },
    '大理州': {
        'longitude_out': 100.19,
        'latitude_out': 25.69,
        'longitude_in': 100.24,
        'latitude_in': 25.45
    },
    '德宏州': {
        'longitude_out': 98.6,
        'latitude_out': 24.41,
        'longitude_in': 97.96,
        'latitude_in': 24.33
    },
    '怒江州': {
        'longitude_out': 98.82,
        'latitude_out': 25.97,
        'longitude_in': 98.92,
        'latitude_in': 26.89
    },
    '迪庆州': {
        'longitude_out': 99.72,
        'latitude_out': 27.78,
        'longitude_in': 98.93,
        'latitude_in': 28.49
    }
}

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

for i in range(len(list_id)):
    df_id = df[df['id'] == list_id[i]]
    list_message = df_id.values.tolist()
    for j in range(len(list_message)-1):
        if not list_message[j][2] == list_message[j+1][2]:
            flow_num[list_month.index(list_message[j+1][1])][list_city.index(list_message[j][2])][list_city.index(list_message[j+1][2])] += 1

for i in range(len(list_month)):
    for j in range(len(list_city)):
        for k in range(len(list_city)):
            list_flow_num.append([list_month[i], list_city[j], list_city[k], flow_num[i][j][k], longitude_latitude[list_city[j]]['longitude_out'], longitude_latitude[list_city[j]]['latitude_out'], longitude_latitude[list_city[k]]['longitude_out'], longitude_latitude[list_city[k]]['latitude_out']])

df_flow_num = pd.DataFrame(list_flow_num, columns=['month', 'from', 'out', 'value', 'lng1', 'lat1', 'lng2', 'lat2'])
df_flow_num = df_flow_num[~df_flow_num['value'].isin([0])]
df_flow_num.to_csv(r'./data/allData.csv', index=False)

for i in range(len(list_month)):
    df_flow_month = df_flow_num[df_flow_num['month'].isin([list_month[i]])]
    df_flow_month = df_flow_month.drop('month', axis=1)
    df_flow_month.to_csv(r'./data/' + str(list_month[i]) + '.csv', index=False)
