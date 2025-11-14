import pandas as pd
from concurrent.futures import ProcessPoolExecutor

FILES = ['file1.csv', 'file2.csv', 'file3.csv', 'file4.csv', 'file5.csv']


def read_csv(file):
    df = pd.read_csv(file)
    return df


def compute(df, is_final=False):
    a_values = []
    b_values = []
    c_values = []
    d_values = []

    for i in range(len(df)):
        category = df.iloc[i]['category']

        if is_final:
            value = float(df.iloc[i]['median'])
        else:
            value = float(df.iloc[i]['value'])

        if category == 'A':
            a_values.append(value)
        elif category == 'B':
            b_values.append(value)
        elif category == 'C':
            c_values.append(value)
        elif category == 'D':
            d_values.append(value)

    result = []
    if a_values:
        a_median = pd.Series(a_values).median()
        a_std = pd.Series(a_values).std()
    else:
        a_median = 0
        a_std = 0
    result.append(['A', a_median, a_std])
    if b_values:
        b_median = pd.Series(b_values).median()
        b_std = pd.Series(b_values).std()
    else:
        b_median = 0
        b_std = 0
    result.append(['B', b_median, b_std])
    if c_values:
        c_median = pd.Series(c_values).median()
        c_std = pd.Series(c_values).std()
    else:
        c_median = 0
        c_std = 0
    result.append(['C', c_median, c_std])
    if d_values:
        d_median = pd.Series(d_values).median()
        d_std = pd.Series(d_values).std()
    else:
        d_median = 0
        d_std = 0
    result.append(['D', d_median, d_std])

    result_df = pd.DataFrame(result, columns=['category', 'median', 'std'])
    return result_df


def process_file(file):
    df = read_csv(file)
    return compute(df)


def main():
    with ProcessPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_file, FILES))

    print('Результаты для каждого файла:')
    for res in results:
        print(res)
        print()
    all_results = pd.concat(results, ignore_index=True)
    final_result = compute(all_results, is_final=True)

    print('Финальный результат:')
    print(final_result)


if __name__ == '__main__':
    main()