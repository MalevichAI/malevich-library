import pandas as pd

classes = {
    'Троллейбус': 3,
    'большой автобус': 3,
    'средний автобус': 2,
    'микроавтобус': 1,
    'Легковой трансп.': 1,
    'до 2-х т': 1,
    'от 2 до 6 т': 1.5,
    'от 6 до 12 т': 1.8,
    'от 12 до 20 т': 2,
    'более 20 т.': 2.2
}

ways_id = {}

directions = ['left', 'through', 'right', 'backward', 'overall']

def combine_columns(row):
    tmp1 = str(row['0']) if not pd.isna(row['0']) else ''
    tmp2 = str(row['1']) if not pd.isna(row['1']) else ''
    return tmp1 + tmp2

def reset_idx(df: pd.DataFrame):
    df.reset_index(inplace=True)
    df.drop(columns='index', axis=1, inplace=True)
    return df

def clean_df(df: pd.DataFrame):
    start_column = ''
    for _, row in df.iterrows():
        if 'Вид транспорта' in row.to_list():
            start_column = row.to_list().index('Вид транспорта')
            break
    df.drop(axis=1, columns=df.columns[:start_column], inplace=True)
    df.dropna(axis = 0, how = 'all', inplace = True)
    df = reset_idx(df)
    cols = [str(x) for x in range(len(df.columns))]
    keys = {}
    for c1, c2 in zip(df.columns.to_list(), cols):
        keys[c1] = c2
    df.rename(columns=keys, inplace=True)
    return df

def get_intervals(df: pd.DataFrame()):
    intervals_idx = []
    intervals = []
    for i, row in df.iterrows():
        if str(row['0']).startswith('Вид транспорта'):
            intervals_idx.append([i])
        elif str(row['0']) == 'Итого':
            intervals_idx[-1].append(i)
        elif str(row['0']) == 'Грузовые':
            df.at[i, '0'] = ''
    for i in intervals_idx:
        intervals.append(pd.DataFrame(df[i[0]:i[1]], columns=df.columns))
    return intervals

def get_ways(ways_list):
    ways = []
    for k, val in enumerate(ways_list):
            if not pd.isna(val) and not str(val).startswith('Всего'):
                ways.append((k ,val))
                ways_id[val] = {}
    return ways

def get_froms(from_list, ways):
    idx = 0
    froms = []
    for k, val in enumerate(from_list):
        if not pd.isna(val):
            froms.append((k, val))
            if k >= ways[idx+1][0]:
                idx += 1
            ways_id[ways[idx][1]][val] = {}
    return froms

def get_units(units_list, ways, froms):
    start_row = 0
    for i, row in units_list.iterrows():
        if 'ФЕ' in row.to_list() and 'ПЕ' in row.to_list():
            start_row = i+1
            break
    for _, row in units_list[start_row:].iterrows():
            cls = row.iloc[0]
            fepe = row[1:].to_list()
            where_idx = 0
            ways_id[ways[0][1]][froms[0][1]][cls] = {}
            for i in range(0, len(froms)*10, 10):
                if i >= ways[where_idx+1][0]:
                    where_idx += 1
                ways_id[ways[where_idx][1]][froms[i//10][1]][cls] = {}

                for fe in range(0, 10, 2):
                    ways_id[ways[where_idx][1]] \
                    [froms[i//10][1]][cls][directions[fe//2]] = {
                        'FE': fepe[i+fe],
                        'PE': fepe[i+fe+1]
                    }

def check(filepath: str):
    xls = pd.read_excel(filepath)
    xls = clean_df(xls)
    intervals = get_intervals(xls)
    output_df = []

    for interval in intervals:
        interval['1'] = interval.apply(combine_columns, axis=1)
        interval.drop(columns='0', axis=1, inplace=True)
        interval = reset_idx(interval)
        ways = get_ways(interval.iloc[0, 1:].to_list())
        ways.append((len(interval.columns), 'end'))
        froms = get_froms(interval.iloc[1, 1:], ways)
        get_units(interval, ways, froms)
        out = []
        for way in ways_id.keys():
            for fr in ways_id[way].keys():
                for cls in ways_id[way][fr].keys():
                    for dir in ways_id[way][fr][cls].keys():
                        val = ways_id[way][fr][cls][dir]
                        out.append([way + ' ' + fr,
                                    dir, classes[cls],
                                    val['FE'],
                                    val['PE']])

        out = pd.DataFrame(out, columns=['name', 'direction', 'class', 'unit',
                                         'reduced_unit'])
        out = out[out['direction'] != 'overall']
        out = reset_idx(out)
        output_df.append(out)

    output_df = reset_idx(pd.concat(output_df))

    return output_df
