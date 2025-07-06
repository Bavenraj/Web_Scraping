import pandas as pd
import csv
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="data_cleaning")
location = geolocator.reverse("5.3946111,98.0162054")
print(location.address)

"""kfc_data = pd.read_csv('data/kfc_data_3_1.csv', encoding='unicode_escape')
#print(kfc_data.head())
filter_data = kfc_data[['State', 'Store Name', 'Rating', 'Review Count', 'Store Status']]
print(filter_data.info())

unique = filter_data.drop_duplicates()
print(unique.head())"""

