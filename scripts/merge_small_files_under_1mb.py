import pandas as pd
import os

comulativeSizeMB = 0
def checkMaxSize(current_directory, csvfile, merged_file_max_size_mb):
    global comulativeSizeMB
    maxSize = merged_file_max_size_mb
    #maxSize = 49.0

    sizeMB = os.path.getsize(current_directory + '/' + csvfile) / 1000000
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


def DirctoryPathToMergeSmallFiles(current_directory, small_file_max_size_kb, merged_file_max_size_mb, plainTextEdit_Page4, QApplication):
    #current_directory = os.getcwd()
    #small_file_max_size_kb = 1000
    #merged_file_max_size_mb = 49.0

    df_multi_list = [[0 for i in range(0)] for j in range(1)]
    csvfiles_multi_list = [[0 for i in range(0)] for j in range(1)]
    marker=0

    wanted_list = ['EMAIL','Email', 'NAME','Name', 'FIRST NAME','Fname', 'LAST NAME','Lname','COUNTRY','Country','NUMBER','Number','SOURCE','Source']

    print('preparing files......')
    s = 'preparing files......'
    plainTextEdit_Page4.appendPlainText(s)
    QApplication.processEvents()

    for csvfile in os.listdir(current_directory):
        sizeKB = os.path.getsize(current_directory + '/' + csvfile)/1000

        if csvfile.endswith(".csv") and sizeKB < small_file_max_size_kb:
            try:
                df = pd.read_csv(current_directory + '/' + csvfile,encoding = "ISO-8859-1",error_bad_lines=False,dtype=str)
                df.columns = df.columns.str.replace('[^a-zA-Z]', ' ',regex=True)
                df.columns = df.columns.str.strip()

                wanted_columns_list = []
                for column in df.columns:
                    if column in wanted_list:
                        wanted_columns_list.append(column)
                df = df[wanted_columns_list]
                flag = 'green'

            except:
                print('problem reading '+csvfile)
                s = 'problem reading '+csvfile
                plainTextEdit_Page4.appendPlainText(s)
                QApplication.processEvents()
                flag = 'red'


            if flag == 'green':
                if 'NAME' in df.columns:
                    name_col_name = 'NAME'
                if 'Name' in df.columns:
                    name_col_name = 'Name'

                if ('NAME' in df.columns) or ('Name' in df.columns):
                    # split NAME column to FIRST NAME and LAST NAME
                    try:
                        df[['Fname', 'Lname']] = df[name_col_name].str.split(' ', 1, expand=True)
                        df = df.drop(columns=[name_col_name])
                    except:
                        df.rename({name_col_name:'Fname'},axis=1, inplace=True)

                statue = checkMaxSize(current_directory, csvfile, merged_file_max_size_mb)

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
                s = 'columns do not match in '+csvfile
                plainTextEdit_Page4.appendPlainText(s)
                QApplication.processEvents()



    if len(df_multi_list[0]) > 0:
        final_directory = os.path.join(current_directory, r'small merged csv files')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        print('merging files......')
        plainTextEdit_Page4.appendPlainText('merging files......')
        QApplication.processEvents()

        list_num = 0
        for df_list in df_multi_list:
            print('following files will be merged in: '+'"merged file'+str(list_num+1) + '.csv"')
            s = 'following files will be merged in: '+'"merged file'+str(list_num+1) + '.csv"'
            plainTextEdit_Page4.appendPlainText(s)
            QApplication.processEvents()

            print(csvfiles_multi_list[list_num])
            s = str(csvfiles_multi_list[list_num])
            plainTextEdit_Page4.appendPlainText(s)
            QApplication.processEvents()

            if len(df_list) >0:
                big_df = pd.concat(df_list)
                big_df.to_csv(final_directory + '/' + 'merged file_1_'+str(list_num+1) + '.csv', index=None, header=True)
                list_num = list_num + 1

    print('Done')