import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from validate_email import validate_email
import numpy as np
import os
import math

j = 1

def filter_eamils(df):
    print('filtering emails in this file: ' + str(j))
    s = 'filtering emails in this file: ' + str(j)
    # plainTextEdit_Page3.appendPlainText(s)
    # QApplication.processEvents()

    if 'EMAIL' in df.columns:
        # delete emails which have values in äëïöüÿÄËÏÖÜŸ
        df = df[~df['EMAIL'].str.contains(r'[äëïöüÿÄËÏÖÜŸ]', na=False)]

        # drop empty emails
        df = df[df['EMAIL'].notna()]

        # delete invaled emails

        try:
            df = df[df['EMAIL'].apply(lambda x: validate_email(x))]
            print('eamil filtering was successful')
            # plainTextEdit_Page3.appendPlainText('eamil filtering was successful')
            # QApplication.processEvents()
        except:
            print('Problem in deleting invalid emails from this file')
            # plainTextEdit_Page3.appendPlainText('Problem in deleting invalid emails from this file')
            # QApplication.processEvents()
    else:
        print('this file does ot have EMAIL column')
        # plainTextEdit_Page3.appendPlainText('this file does ot have EMAIL column')
        # QApplication.processEvents()
    return df


def DirctoryPathToLargeFilesToSplit(current_directory):
    global j
    #current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'splited files')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    #current_directory = os.getcwd()
    
    for csvfile in os.listdir(current_directory):
        if csvfile.endswith(".csv"):
            sizeMB = os.path.getsize(current_directory + '/' + csvfile) / 1000000

            if sizeMB > 49.0:
                #splited_files_number = int(sizeMB / 95) + (sizeMB % 95 > 0)
                splited_files_number = int(math.ceil(sizeMB / 49))
                print('loading ' + csvfile + ' file: ' + str(j))
                s = 'loading ' + csvfile + ' file: ' + str(j)
                yield s
                # plainTextEdit_Page3.appendPlainText(s)
                # QApplication.processEvents()

                df = pd.read_csv(current_directory + '/' + csvfile,encoding = "ISO-8859-1",error_bad_lines=False)
                # df = filter_eamils(df)

                df_list = np.array_split(df, splited_files_number)

                i=1
                print('splitting ' + csvfile + ' file: ' + str(j))
                s = 'splitting ' + csvfile + ' file: ' + str(j)
                yield s
                # plainTextEdit_Page3.appendPlainText(s)
                # QApplication.processEvents()

                for dfS in df_list:
                    dfS.to_csv(final_directory + '/' + csvfile[0:-4] + ' splited' + str(i) + '.csv', index=None, header=True)
                    i = i + 1

                print('Done')
                print('===========================================================================================')
                yield 'Done'
                yield '==========================================================================================='
                # plainTextEdit_Page3.appendPlainText('Done')
                # QApplication.processEvents()
                j = j + 1

    print('program has finished execution')
    yield 'program has finished execution'
    # plainTextEdit_Page3.appendPlainText('program has finished execution')
    # QApplication.processEvents()
