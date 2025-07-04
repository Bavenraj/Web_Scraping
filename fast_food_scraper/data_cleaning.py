import pandas as pd
import csv

kfc_data = pd.read_csv('data/kfc_data_3_1.csv', encoding='unicode_escape')
#print(kfc_data.head())
filter_data = kfc_data[['State', 'Store Name', 'Rating', 'Review Count', 'Store Status']]
print(filter_data.info())

unique = filter_data.drop_duplicates()
print(unique.head())

