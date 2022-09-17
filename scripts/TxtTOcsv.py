from lib2to3.pytree import convert
import pandas as pd
import os




def DirctoryPathToTextToCsv(current_directory):
    # current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'text to csv')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    for txtfile in os.listdir(current_directory):
        if txtfile.endswith(".txt"):
            print("Converting " + txtfile + " ......")
            yield "Converting " + txtfile + " ......"
            
            df = pd.read_fwf(current_directory + '/' + txtfile,header=None)
            df['Email'] = df[0].str.split(':', 1, expand=True)[0]
            df = df.loc[:, df.columns.intersection(['Email'])]
            df.to_csv(final_directory + '/' + txtfile[0:-4]+'.csv', index=None, header=True)
