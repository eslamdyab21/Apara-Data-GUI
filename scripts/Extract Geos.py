import pandas as pd
from validate_email import validate_email
import os

def create_country_folder(current_directory,csvfile):
    final_directory = os.path.join(current_directory, r''+csvfile)
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    return final_directory


def filter_by_country(df):
    # delete emails which have values in äëïöüÿÄËÏÖÜŸ
    df = df[~df['EMAIL'].str.contains(r'[äëïöüÿÄËÏÖÜŸ]',na=False)]

    # drop empty emails
    df = df[df['EMAIL'].notna()]

    # delete invaled emails
    try:
        df = df[df['EMAIL'].apply(lambda x: validate_email(x))]
    except:
        print('Problem in deleting invalid emails from this file')


    df_country_grouped = df.groupby('COUNTRY')
    countries = df['COUNTRY'].unique()

    final_directory = create_country_folder(current_directory, csvfile[0:-4])
    for country in countries:
        df_country_grouped.get_group(country).to_csv(final_directory + '/' + country + '.csv', index=None, header=True)
    print('Done')
    print('===========================================================================================')

current_directory = os.getcwd()

wanted_list1 = ['EMAIL','FIRST NAME','LAST NAME','COUNTRY','NUMBER','SOURCE']
wanted_list2 = ['EMAIL','NAME','COUNTRY','NUMBER','SOURCE']

i =1
for csvfile in os.listdir(current_directory):
    if csvfile.endswith(".csv"):
        df = pd.read_csv(csvfile)
        check1 = all(item in df.columns for item in wanted_list1)
        check2 = all(item in df.columns for item in wanted_list2)
        if check1:
            print('filtering ' + csvfile+ ' file: '+str(i))
            df = df[wanted_list1]
            df = df[df['COUNTRY'].notna()]
            df = df[~df['COUNTRY'].str.isnumeric()]
            filter_by_country(df)
            i = i + 1
        elif check2:
            print('splitting NAME and filtering ' + csvfile + ' file: ' + str(i))
            df = df[wanted_list2]
            df = df[df['COUNTRY'].notna()]
            df = df[~df['COUNTRY'].str.isnumeric()]

            # split NAME column to FIRST NAME and LAST NAME
            df[['FIRST NAME', 'LAST NAME']] = df['NAME'].str.split(' ', 1, expand=True)
            df = df.drop(columns=['NAME'])
            filter_by_country(df)
            i = i + 1
        else:
            print('columns in ' + csvfile + ' file does not match')
            print('===========================================================================================')


print('program has finished execution')
