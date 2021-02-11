import pandas as pd
import pickle

df = pickle.load(open("../xy_Static/dataframe.p", "rb"))

dv = {'Left': {}, 'Right': {}}
videos = {'Front': dv, 'Side': dict(dv)}

for index, row in df.iterrows():
    view = videos[row['View']]
    if row['Move'] in view[row['Side']]:
        side = view[row['Side']]
        side[row['Move']].add(row['Upload video here'][row['Upload video here'].find('id') + 3:])
    else:
        side = view[row['Side']]
        side[row['Move']] = set()
        url = row['Upload video here']
        # print(url)
        i = url.find('id') + 3
        # print(i)
        side[row['Move']].add(url[i:])

# for k in videos:
#     print(k)
#     print('\tMoves')
#     moves = videos[k]
#     for m in moves:
#         print(f'\t\t{m} Len {len(moves[m])}: {moves[m]}')
