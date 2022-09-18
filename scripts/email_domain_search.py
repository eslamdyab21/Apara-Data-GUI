import pandas as pd
import os
import scripts.merge_search_domain_files as merge_search_domain_files

def DirctoryPathToEmailDomainSearch(current_directory, wanted_email):
    #wanted_email = input('Enter an email: ')

    #current_directory = os.getcwd()
    folders = []
    for folder in os.listdir(current_directory):
        if '.' not in folder:
            folders.append(folder)

    final_directory = os.path.join(current_directory, r'domain-search-results')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    
    file_num = 0
    wanted_mlist = [[0 for i in range(0)] for j in range(3)]
    for folder in folders:
        for csvfile in os.listdir(current_directory + '/' + folder):
            path = current_directory + '/' + folder + '/'
            if csvfile.endswith(".csv"):
                try:
                    df = pd.read_csv(path + csvfile,encoding="ISO-8859-1",dtype=str)
                    flag = 'green'
                except:
                    print('problem reading ' + csvfile + ' file')
                    yield 'problem reading ' + csvfile + ' file'
                    flag = 'red'

                if flag == 'green':
                    print('searching in ' + folder + '/' + csvfile + '.......')
                    yield 'searching in ' + folder + '/' + csvfile + '.......'

                    if 'EMAIL' in df.columns:
                        email_col_name = 'EMAIL'

                    elif 'Email' in df.columns:
                        email_col_name = 'Email'

                    if ('EMAIL' in df.columns) or ('Email' in df.columns):
                        if '@' in wanted_email:
                            if wanted_email in list(df[email_col_name]):
                                wanted_data = df[df[email_col_name] == wanted_email]
                                wanted_mlist[0].append(folder)
                                wanted_mlist[1].append(csvfile)
                                wanted_mlist[2].append(wanted_data)
                                #print(wanted_email + ' found in ' + "'" + folder + "'" + ' folder and in ' +  "'" + csvfile + "'" + ' file')
                                #print("Email row's data: ")
                                #print(str(wanted_data))
                                #print('==============================================================')

                        if '@' not in wanted_email:
                            domains_col = df[email_col_name].str.split('@', 1, expand=True)[1]
                            domains = list(domains_col.unique())
                            if wanted_email in domains:
                                wanted_data = df[domains_col == wanted_email]
                                wanted_data.to_csv(final_directory + '/' + 'domain_search_result_'+str(file_num+1) + '.csv', index=None, header=True)
                                
                                file_num = file_num + 1

                                wanted_mlist[0].append(folder)
                                wanted_mlist[1].append(csvfile)
                                wanted_mlist[2].append(wanted_data)

    if len(wanted_mlist[0]) == 0:
        print(wanted_email + ' was not found')
        yield wanted_email + ' was not found'

    else:
        for i in range(len(wanted_mlist[0])):
            print(wanted_email + ' found in ' + "'" + wanted_mlist[0][i] + "'" + ' folder and in ' + "'" + wanted_mlist[1][i] + "'" + ' file')
            s = str(wanted_email + ' found in ' + "'" + wanted_mlist[0][i] + "'" + ' folder and in ' + "'" + wanted_mlist[1][i] + "'" + ' file')
            yield s
            print("Email row's data: ")
            yield "Email row's data: "
            print(str(wanted_mlist[2][i]))
            yield str(wanted_mlist[2][i])
            print('==============================================================')
            yield '=============================================================='
        
        val = merge_search_domain_files.DirctoryPathToMergeSmallFiles(final_directory,0, 1000)
        print(final_directory)
        yield final_directory
        for value in val:
            yield value

