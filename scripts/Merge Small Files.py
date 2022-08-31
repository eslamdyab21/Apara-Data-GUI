import pandas as pd
import numpy as np
import os

comulativeSizeMB = 0
def checkMaxSize(csvfile):
    global comulativeSizeMB
    maxSize = 49.0

    sizeMB = os.path.getsize(csvfile) / 1000000
    comulativeSizeMB = comulativeSizeMB + sizeMB

    if sizeMB < maxSize:
        if comulativeSizeMB < maxSize:
            return True
        else:
            comulativeSizeMB = sizeMB
            return False

    else:
        if comulativeSizeMB < maxSize:
            return True
        else:
            comulativeSizeMB = 0
            return False


current_directory = os.getcwd()

df_multi_list = [[0 for i in range(0)] for j in range(1)]
csvfiles_multi_list = [[0 for i in range(0)] for j in range(1)]
marker=0

wanted_list1 = ['EMAIL','FIRST NAME','LAST NAME','COUNTRY','NUMBER','SOURCE']
wanted_list2 = ['EMAIL','NAME','COUNTRY','NUMBER','SOURCE']
print('preparing files......')
for csvfile in os.listdir(current_directory):
    sizeKB = os.path.getsize(csvfile)/1000

    if csvfile.endswith(".csv") and sizeKB < 250:
        try:
            df = pd.read_csv(csvfile,encoding = "ISO-8859-1",error_bad_lines=False,dtype=str)
            df.columns = df.columns.str.strip()

            if 'SOURCE' in df.columns and 'COUNTRY' in df.columns:
                wanted_list1 = ['EMAIL', 'FIRST NAME', 'LAST NAME', 'COUNTRY', 'NUMBER', 'SOURCE']
                wanted_list2 = ['EMAIL', 'NAME', 'COUNTRY', 'NUMBER', 'SOURCE']
            elif 'SOURCE' in df.columns and not 'COUNTRY' in df.columns:
                wanted_list1 = ['EMAIL', 'FIRST NAME', 'LAST NAME', 'NUMBER', 'SOURCE']
                wanted_list2 = ['EMAIL', 'NAME', 'NUMBER', 'SOURCE']
            elif 'COUNTRY' in df.columns and not 'SOURCE' in df.columns:
                wanted_list1 = ['EMAIL', 'FIRST NAME', 'LAST NAME', 'NUMBER', 'COUNTRY']
                wanted_list2 = ['EMAIL', 'NAME', 'NUMBER', 'COUNTRY']
            else:
                wanted_list1 = ['EMAIL', 'FIRST NAME', 'LAST NAME', 'NUMBER']
                wanted_list2 = ['EMAIL', 'NAME', 'NUMBER']

            check1 = all(item in df.columns for item in wanted_list1)
            check2 = all(item in df.columns for item in wanted_list2)

        except:
            print('problem reading '+csvfile)
            check1 = False
            check2 = False


        if check1:
            statue = checkMaxSize(csvfile)
            df = df[wanted_list1]

        elif check2:
            statue = checkMaxSize(csvfile)
            df = df[wanted_list2]

            # split NAME column to FIRST NAME and LAST NAME
            df[['FIRST NAME', 'LAST NAME']] = df['NAME'].str.split(' ', 1, expand=True)
            df = df.drop(columns=['NAME'])

        if check1 or check2:
            if statue:
                df_multi_list[marker].append(df)
                csvfiles_multi_list[marker].append(csvfile)

            elif statue == False:
                if len(df_multi_list[marker]) ==0:
                    df_multi_list[marker].append(df)
                    csvfiles_multi_list[marker].append(csvfile)
                    df_multi_list.append([])
                    csvfiles_multi_list.append([])
                    marker = marker + 1

                else:
                    df_multi_list.append([])
                    csvfiles_multi_list.append([])
                    marker = marker + 1
                    df_multi_list[marker].append(df)
                    csvfiles_multi_list[marker].append(csvfile)
        else:
            print('columns do not match in '+csvfile)



if len(df_multi_list[0]) > 0:
    final_directory = os.path.join(current_directory, r'small merged csv files')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    print('merging files......')

    list_num = 0
    for df_list in df_multi_list:
        print('following files will be merged in: '+'"merged file'+str(list_num+1) + '.csv"')
        print(csvfiles_multi_list[list_num])
        if len(df_list) >0:
            big_df = pd.concat(df_list)
            big_df.to_csv(final_directory + '/' + 'merged file_1_'+str(list_num+1) + '.csv', index=None, header=True)
            list_num = list_num + 1

print('Done')