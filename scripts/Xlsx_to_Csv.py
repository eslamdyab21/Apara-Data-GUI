import pandas as pd
import os


def DirctoryPathToXlxsFiles(current_directory):
    #current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'csv')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    for filename in os.listdir(current_directory):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(current_directory + '/' + filename)
            df.to_csv(final_directory + '/' + filename[0:-5] + '.csv',index = None,header=True)
