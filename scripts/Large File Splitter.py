import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from validate_email import validate_email
import numpy as np
import os
import math


def filter_eamils(df):
    print('filtering emails in this file: ' + str(j))
    if 'EMAIL' in df.columns:
        # delete emails which have values in äëïöüÿÄËÏÖÜŸ
        df = df[~df['EMAIL'].str.contains(r'[äëïöüÿÄËÏÖÜŸ]', na=False)]

        # drop empty emails
        df = df[df['EMAIL'].notna()]

        # delete invaled emails

        try:
            df = df[df['EMAIL'].apply(lambda x: validate_email(x))]
            print('eamil filtering was successful')
        except:
            print('Problem in deleting invalid emails from this file')
    else:
        print('this file does ot have EMAIL column')
    return df

current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'splited files')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)

current_directory = os.getcwd()
j = 1
for csvfile in os.listdir(current_directory):
    if csvfile.endswith(".csv"):
        sizeMB = os.path.getsize(csvfile) / 1000000

        if sizeMB > 49.0:
            #splited_files_number = int(sizeMB / 95) + (sizeMB % 95 > 0)
            splited_files_number = int(math.ceil(sizeMB / 49))
            print('loading ' + csvfile + ' file: ' + str(j))
            df = pd.read_csv(csvfile,encoding = "ISO-8859-1",error_bad_lines=False)
            df = filter_eamils(df)

            df_list = np.array_split(df, splited_files_number)

            i=1
            print('splitting ' + csvfile + ' file: ' + str(j))
            for dfS in df_list:
                dfS.to_csv(final_directory + '/' + csvfile[0:-4] + ' splited' + str(i) + '.csv', index=None, header=True)
                i = i + 1

            print('Done')
            print('===========================================================================================')
            j = j + 1

print('program has finished execution')
