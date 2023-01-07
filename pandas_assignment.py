import pandas as pd
from datetime import date, timedelta, datetime
import calendar
import random

'''This function will drop null value records & duplicate records,
 and also filter only required ride locations'''
def filter_raw_data(df):
    print("===========Raw data Filtering started=============")
    print("total number of records before filtering are : ", df.shape[0])
    print("number of null value records in the give data frame : ", df.isna().sum()[1])
    df = df.dropna(how='any')
    print("null values have been dropped....")
    print("number of duplicate records in the give data frame : ", df.duplicated().sum())
    df = df.drop_duplicates(keep='first')
    print("duplicate records have been removed....")
    df.drop(df[df.Name.str.contains(r'[^a-zA-Z ]') |
               df.Location.str.contains(r'[^A-Za-z ]')].index, inplace=True)

    locations = ['coppell', 'broadwalk', 'mercer', 'courtyard', 'mansion', 'dom']

    # "filtering required ride locations..."
    df = df[(df['Location'].str.contains('|'.join(locations), regex=True, case=False))]

    print("numeric and special characteristic records have been dropped....")
    print("number of records after filtering : ", df.shape[0])
    print("===========Raw data Filtering ended=============")
    return df

'''
This function 
'''
def ride_schedule(data):
    temp_dic = {'Coppell': data[data['Location'] == 'Coppell']['Name'].tolist(),
                'Broadwalk&Mercer': data[(data['Location'] == 'Broadwalk') | (data['Location'] == 'Mercer')][
                    'Name'].tolist(), 'Courtyard&Mansion&Dom': data[
            (data['Location'] == 'Courtyard') | (data['Location'] == 'Mansion') | (data['Location'] == 'Dom')][
            'Name'].tolist()}
    cleaned_data = pd.DataFrame()
    cleaned_data.index = get_date()
    for loc in temp_dic:
        cleaned_data[loc] = list_of_names(temp_dic[loc], len(get_date()))
    cleaned_data.to_csv("file1.csv")
    # print(cleaned_data)


'''
Alternative approach for ride schedule
Ride will be assigned to a person on same day of every week
def list_of_names(li, n):
    new_list = []
    for i in range(n):
        new_list.append(li[i % len(li)])
    return new_list
'''


def list_of_names(li, n):
    new_list = []
    for i in range(n):
        if i % len(li) == 0:
            random.shuffle(li)
        new_list.append(li[i % len(li)])
    return new_list


def get_date():
    month = datetime.now().month
    year = datetime.now().year
    number_of_days = calendar.monthrange(year, month)[1]
    first_date = date(year, month, 1)
    last_date = date(year, month, number_of_days)
    delta = last_date - first_date

    return [(first_date + timedelta(i)).strftime('%m/%d/%y') for i in range(delta.days + 1)]


if __name__ == '__main__':
    raw_data = pd.read_csv('employee.csv')
    filtered_data = filter_raw_data(raw_data)
    ride_schedule(filtered_data)

