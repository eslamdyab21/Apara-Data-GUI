import pandas as pd
from validate_email import validate_email
from disposable_email_domains import blocklist
import os



def DirctoryPathToValidation(current_directory,plainTextEdit_Page6, QApplication):
    #current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'valid emails')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    j=1
    for csvfile in os.listdir(current_directory):
        if csvfile.endswith(".csv"):
            print('loading ' + csvfile + ' file: ' + str(j))
            s = 'loading ' + csvfile + ' file: ' + str(j)
            plainTextEdit_Page6.appendPlainText(s)
            QApplication.processEvents()

            try:
                df = pd.read_csv(current_directory + '/' + csvfile, encoding="ISO-8859-1", error_bad_lines=False,dtype=str)
            except:
                print('problem reading ' + csvfile)
                s = 'problem reading ' + csvfile
                plainTextEdit_Page6.appendPlainText(s)
                QApplication.processEvents()

            if 'EMAIL' in df.columns:
                print('filtering emails.....')
                plainTextEdit_Page6.appendPlainText('filtering emails.....')
                QApplication.processEvents()

                # delete invaled emails
                df = df[df['EMAIL'].notna()].reset_index(drop=True)

                print('first stage....')
                plainTextEdit_Page6.appendPlainText('first stage....')
                QApplication.processEvents()

                valid_email_list = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I',
                                    'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q',
                                    'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z',
                                    'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '@', '_', '.']

                try:
                    invalid_index_list = []
                    for i in range(df.shape[0]):
                        try:
                            for char in df['EMAIL'][i]:
                                if char not in valid_email_list:
                                    invalid_index_list.append(i)
                        except:
                            invalid_index_list.append(i)
                    df = df.drop(df.index[invalid_index_list])
                except:
                    print('first stage unsuccessful')
                    plainTextEdit_Page6.appendPlainText('first stage unsuccessful')
                    QApplication.processEvents()

                print('second stage....')
                plainTextEdit_Page6.appendPlainText('second stage....')
                QApplication.processEvents()

                # drop empty emails
                df = df[df['EMAIL'].notna()].reset_index(drop=True)

                try:
                    df = df[df['EMAIL'].apply(lambda x: validate_email(x))]
                except:
                    print('second stage unsuccessful')
                    plainTextEdit_Page6.appendPlainText('second stage unsuccessful')
                    QApplication.processEvents()

                print('third stage....')
                plainTextEdit_Page6.appendPlainText('third stage....')
                QApplication.processEvents()

                try:
                    invalid_index_list = []
                    for i in range(df.shape[0]):
                        try:
                            if df['EMAIL'][i].split('@')[1] in blocklist:
                                invalid_index_list.append(i)
                        except:
                            invalid_index_list.append(i)
                    df = df.drop(df.index[invalid_index_list])
                except:
                    print('third stage unsuccessful')
                    plainTextEdit_Page6.appendPlainText('third stage unsuccessful')
                    QApplication.processEvents()

                df = df[df['EMAIL'].notna()].reset_index(drop=True)
                df.to_csv(final_directory + '/' + csvfile, index=None, header=True)

            else:
                print('this file does not have EMAIL column')
                plainTextEdit_Page6.appendPlainText('this file does not have EMAIL column')
                QApplication.processEvents()

            print('===========================================================================================')
            plainTextEdit_Page6.appendPlainText('===========================================================================================')
            QApplication.processEvents()
            j = j + 1

    print('program has finished execution')
    plainTextEdit_Page6.appendPlainText('program has finished execution')
    QApplication.processEvents()
