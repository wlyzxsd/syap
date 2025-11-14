import random
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

FILE_NAMES = ['file1.csv', 'file2.csv', 'file3.csv', 'file4.csv', 'file5.csv']
CATEGORIES = ['A', 'B', 'C', 'D']

def generate_random_data():
    data_records = []
    for _ in range(50):
        category = random.choice(CATEGORIES)
        value = random.uniform(1, 10)
        data_records.append([category, value])
    return data_records

def save_to_csv(data_records, filename):
    dataframe = pd.DataFrame(data_records, columns=['category', 'value'])
    dataframe.to_csv(filename, index=False)

def process_file(filename):
    data = generate_random_data()
    save_to_csv(data, filename)

def main():
    with ProcessPoolExecutor() as executor:
        executor.map(process_file, FILE_NAMES)

if __name__ == '__main__':
    main()