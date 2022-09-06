import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import dns.resolver
import time
import os





#current_directory = os.getcwd()


df_domains_list=[]
big_df_domains = []
k=1


def mx_validate(df,email_col_name,csvfile, current_directory):
    global  df_domains_list
    global big_df_domains
    global k

    final_directory = os.path.join(current_directory, r'mx valid emails')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


    df[['mail', 'domain']] = df[email_col_name].str.split('@', 1, expand=True)
    df = df[~df['domain'].isnull()]
    domains = list(df.domain.unique())

    if 'checked_domains.csv' in os.listdir(current_directory):
        big_df_domains = pd.read_csv(current_directory + '/' + 'checked_domains.csv')
        if k ==1:
            df_domains_list.append(big_df_domains)
        checked_domains_list = list(big_df_domains['domain'].unique())
        if 'type' in big_df_domains.columns:
            if 'invalid' in big_df_domains['type'].unique():
                invaid_domains = list(big_df_domains[big_df_domains['type'] == 'invalid']['domain'].unique())
                df = df[~df['domain'].isin(invaid_domains)]

    else:
        if len(df_domains_list) >0:
            checked_domains_list = list(big_df_domains['domain'].unique())
            if 'invalid' in big_df_domains['type'].unique():
                invaid_domains = list(big_df_domains[big_df_domains['type'] == 'invalid']['domain'].unique())
                df = df[~df['domain'].isin(invaid_domains)]
        else:
            checked_domains_list = []


    domains_dict = {}
    invalid_domains_list = []

    i = 0
    for domain in domains:
        i = i + 1
        if domain not in checked_domains_list:
            try:
                mxRecords = dns.resolver.resolve(domain, 'MX')
                exchanges = [exchange.to_text().split()[1] for exchange in mxRecords]
                domains_dict[domain] = ['valid', exchanges]
                print(str(len(os.listdir(current_directory)) - k) + ' files remaining')
                s = str(len(os.listdir(current_directory)) - k) + ' files remaining'
                yield s
                #plainTextEdit_Page6.appendPlainText(s)
                #QApplication.processEvents()

                print(domain + ' domain exist')
                s = domain + ' domain exist'
                yield s
                #plainTextEdit_Page6.appendPlainText(s)
                #QApplication.processEvents()
                

            except:
                print(str(len(os.listdir(current_directory)) - k) + ' files remaining')
                s = str(len(os.listdir(current_directory)) - k) + ' files remaining'
                #plainTextEdit_Page6.appendPlainText(s)
                #QApplication.processEvents()

                print(domain + ' domain does not exist')
                s = domain + ' domain does not exist'
                yield s
                #plainTextEdit_Page6.appendPlainText(s)
                #QApplication.processEvents()

                domains_dict[domain] = ['invalid',np.nan]
                invalid_domains_list.append(domain)

            time.sleep(0.2)
            per = i * 100 / len(domains)
            print(str(int(per)) + '%')
            yield str(int(per)) + '%'
            #plainTextEdit_Page6.appendPlainText(str(int(per)) + '%')
            #QApplication.processEvents()

            print('===================================================================================')
            yield '==================================================================================='
            #plainTextEdit_Page6.appendPlainText('===================================================================================')
            #QApplication.processEvents()

        else:
            print(str(len(os.listdir(current_directory)) - k) + ' files remaining')
            s = str(len(os.listdir(current_directory)) - k) + ' files remaining'
            yield s
            #plainTextEdit_Page6.appendPlainText(s)
            #QApplication.processEvents()

            print(domain + ' domain had been checked before')
            s = domain + ' domain had been checked before'
            yield s
            #plainTextEdit_Page6.appendPlainText(s)
            #QApplication.processEvents()

            per = i * 100 / len(domains)
            print(str(int(per)) + '%')
            yield str(int(per)) + '%'
            #plainTextEdit_Page6.appendPlainText(str(int(per)) + '%')
            #QApplication.processEvents()

            print('===================================================================================')
            yield '==================================================================================='
            #plainTextEdit_Page6.appendPlainText('===================================================================================')
            #QApplication.processEvents()

    df = df[~df['domain'].isin(invalid_domains_list)]
    df = df.drop(columns=['mail', 'domain'])

    df.to_csv(final_directory + '/' + csvfile, encoding="ISO-8859-1", index=None, header=True)

    df_domains = pd.DataFrame.from_dict(domains_dict, orient='index').reset_index().rename(columns={'index': 'domain', 0: 'type', 1: 'mx records'})

    df_domains_list.append(df_domains)
    big_df_domains = pd.concat(df_domains_list)
    big_df_domains.to_csv(current_directory + '/' +'checked_domains.csv', index=None, header=True)


    #save valid and invalid domains in separate files
    big_df_domains_valid = big_df_domains.copy()
    big_df_domains_invalid = big_df_domains.copy()
    
    big_df_domains_valid = big_df_domains_valid.drop('mx records', axis=1)
    big_df_domains_invalid = big_df_domains_invalid.drop('mx records', axis=1)


    big_df_domains_valid = big_df_domains_valid[big_df_domains_valid['type'].isin(['valid'])]
    big_df_domains_invalid = big_df_domains_invalid[big_df_domains_invalid['type'].isin(['invalid'])]


    big_df_domains_valid.to_csv(current_directory + '/' +'checked_domains_valid.csv', index=None, header=True)
    big_df_domains_invalid.to_csv(current_directory + '/' +'checked_domains_invalid.csv', index=None, header=True)

   
    k = k + 1





def DirctoryPathToValidation(current_directory):
    j=1
    
    for csvfile in os.listdir(current_directory):
        if csvfile.endswith(".csv") and not csvfile == 'checked_domains.csv':
            start_time = time.time()
            print('loading ' + csvfile + ' file: ' + str(j))
            s = 'loading ' + csvfile + ' file: ' + str(j)
            yield s
            #plainTextEdit_Page6.appendPlainText(s)
            #QApplication.processEvents()

            try:
                df = pd.read_csv(current_directory + '/' + csvfile, encoding="ISO-8859-1", error_bad_lines=False,dtype=str)
            except:
                print('problem reading ' + csvfile)
                s = 'problem reading ' + csvfile
                yield s
                #plainTextEdit_Page6.appendPlainText(s)
                #QApplication.processEvents()

            if 'EMAIL' in df.columns:
                email_col_name = 'EMAIL'
                df = df[df['EMAIL'].notna()].reset_index(drop=True)
                df = df[~df['EMAIL'].isnull()]
                print('MX filtering....')
                val = mx_validate(df,email_col_name,csvfile,current_directory)
                for value in val:
                    yield value
            elif 'Email' in df.columns:
                email_col_name = 'Email'
                df = df[df['Email'].notna()].reset_index(drop=True)
                df = df[~df['Email'].isnull()]
                print('MX filtering....')
                val = mx_validate(df,email_col_name,csvfile,current_directory)
                for value in val:
                    yield value

            j = j + 1

            #print("--- %s minuts ---" % ((time.time() - start_time)))
            #s = "--- %s minuts ---" % ((time.time() - start_time))
            #plainTextEdit_Page6.appendPlainText(s)
            #QApplication.processEvents()