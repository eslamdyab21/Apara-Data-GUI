import pandas as pd
import os


def create_country_folder(current_directory):
    final_directory = os.path.join(current_directory, r'countries')
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    return final_directory



def DirctoryPathToGeo(current_directory):
    print('Merging....')
    s = 'Merging....'
    yield s
    # plainTextEdit_Page5.appendPlainText(s)
    # QApplication.processEvents()

    #current_directory = os.getcwd()
    folders = []
    Coutries = []
    for folder in os.listdir(current_directory):
        if os.path.isdir(current_directory + '/' + folder):
            folders.append(folder)
            Coutries.extend(os.listdir(current_directory + '/' + folder))


    csvCoutries = list(set(Coutries))
    final_directory = create_country_folder(current_directory)

    for csvCountry in csvCoutries:
        df_list = []
        for i in range(len(folders)):
            if csvCountry in os.listdir(current_directory + '/' + folders[i]):
                df = pd.read_csv(current_directory + '/' + folders[i] + '/' + csvCountry,encoding = "ISO-8859-1",error_bad_lines=False)
                df_list.append(df)

        if len(df_list) >1:
            result = pd.concat(df_list)
            result.to_csv(final_directory + '/' + csvCountry, index=None, header=True)

        elif len(df_list) ==1:
            df.to_csv(final_directory + '/' + csvCountry, index=None, header=True)

    print('program has finished execution')
    s = 'program has finished execution'
    yield s
    # plainTextEdit_Page5.appendPlainText(s)
    # QApplication.processEvents()
