import pandas as pd
import numpy as np
import os





def DirctoryPathToNumbersExtract(current_directory):
    #current_directory = os.getcwd()


    final_directory = os.path.join(current_directory, r'Numbers')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    for csvfile in os.listdir(current_directory):
        if csvfile.endswith(".csv"):
            df = pd.read_csv(current_directory + '/' + csvfile, encoding="ISO-8859-1", error_bad_lines=False,dtype=str)
            if 'NUMBER' in df.columns:
                print("Extracting numbers in " + csvfile + ' file')
                df['NUMBER'] = '+' + df['NUMBER'].astype(str)
                np.savetxt(final_directory + '/' + csvfile.split('.')[0]+ '.txt' , df['NUMBER'].values, fmt='%s')
                yield "Extracting numbers in " + csvfile + ' file'

            elif 'Number' in df.columns:
                print("Extracting numbers in " + csvfile + ' file')
                df['Number'] = '+' + df['Number'].astype(str)
                np.savetxt(final_directory + '/' + csvfile.split('.')[0]+ '.txt' , df['Number'].values, fmt='%s')
                yield "Extracting numbers in " + csvfile + ' file'
