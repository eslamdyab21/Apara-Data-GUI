import pandas as pd
import os



def create_csv_folder(current_directory):
    final_directory = os.path.join(current_directory, r'csv')
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    return final_directory




def DirctoryPathToXlxsFiles(current_directory):
    #current_directory = os.getcwd()
    folders = []
    for folder in os.listdir(current_directory):
        if '.' not in folder:
            folders.append(folder)

    for folder in folders:
        final_directory = create_csv_folder(current_directory + '/' + folder)
        for xfile in os.listdir(current_directory + '/' + folder):
            path = current_directory + '/' + folder + '/'
            if xfile.endswith(".xlsx"):
                df = pd.read_excel(path + xfile)
                df.to_csv(final_directory + '/' + xfile[0:-5] + '.csv',index = None,header=True)
    
    return 'done'

