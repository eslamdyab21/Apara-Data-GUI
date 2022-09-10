import pandas as pd
import os

geo_dict = {'AA': 'Aruba',
 'AC': 'Antigua and Barbuda',
 'AE': 'United Arab Emirates',
 'AF': 'Afghanistan',
 'AG': 'Algeria',
 'AJ': 'Azerbaijan',
 'AL': 'Albania',
 'AM': 'Armenia',
 'AN': 'Andorra',
 'AO': 'Angola',
 'AQ': 'American Samoa',
 'AR': 'Argentina',
 'AS': 'Australia',
 'AU': 'Austria',
 'AV': 'Anguilla',
 'AY': 'Antarctica',
 'BA': 'Bahrain',
 'BB': 'Barbados',
 'BC': 'Botswana',
 'BD': 'Bermuda',
 'BE': 'Belgium',
 'BF': 'Bahamas',
 'BG': 'Bangladesh',
 'BH': 'Belize',
 'BK': 'Bosnia',
 'BL': 'Bolivia',
 'BM': 'Myanmar',
 'BN': 'Benin',
 'BO': 'Belarus',
 'BP': 'Solomon Islands',
 'BR': 'Brazil',
 'BT': 'Bhutan',
 'BU': 'Bulgaria',
 'BV': 'Bouvet Island',
 'BX': 'Brunei',
 'BY': 'Burundi',
 'CA': 'Canada',
 'CB': 'Cambodia',
 'CD': 'Chad',
 'CE': 'Sri Lanka',
 'CF': 'Congo Republic',
 'CG': 'DR Congo',
 'CH': 'China',
 'CI': 'Chile',
 'CJ': 'Cayman Islands',
 'CK': 'Cocos (Keeling) Islands',
 'CM': 'Cameroon',
 'CN': 'Comoros',
 'CO': 'Colombia',
 'CQ': 'Northern Mariana Islands',
 'CS': 'Costa Rica',
 'CT': 'Central African Republic',
 'CU': 'Cuba',
 'CV': 'Cabo Verde',
 'CW': 'Cook Islands',
 'CY': 'Cyprus',
 'DA': 'Denmark',
 'DJ': 'Djibouti',
 'DO': 'Dominica',
 'DR': 'Dominican Republic',
 'EC': 'Ecuador',
 'EG': 'Egypt',
 'EI': 'Ireland',
 'EK': 'Equatorial Guinea',
 'EN': 'Estonia',
 'ER': 'Eritrea',
 'ES': 'El Salvador',
 'ET': 'Ethiopia',
 'EZ': 'Czechia',
 'FG': 'French Guiana',
 'FI': 'Finland',
 'FJ': 'Fiji',
 'FK': 'Falkland Islands',
 'FM': 'Micronesia',
 'FO': 'Faroe Islands',
 'FP': 'French Polynesia',
 'FR': 'France',
 'FS': 'French Southern Territories',
 'GA': 'The Gambia',
 'GB': 'Gabon',
 'GG': 'Georgia',
 'GH': 'Ghana',
 'GI': 'Gibraltar',
 'GJ': 'Grenada',
 'GK': 'Guernsey',
 'GL': 'Greenland',
 'GM': 'Germany',
 'GP': 'Guadeloupe',
 'GQ': 'Guam',
 'GR': 'Greece',
 'GT': 'Guatemala',
 'GV': 'Guinea',
 'GY': 'Guyana',
 'HA': 'Haiti',
 'HK': 'Hong Kong',
 'HM': 'Heard and McDonald Islands',
 'HO': 'Honduras',
 'HR': 'Croatia',
 'HU': 'Hungary',
 'IC': 'Iceland',
 'ID': 'Indonesia',
 'IM': 'Isle of Man',
 'IN': 'India',
 'IO': 'British Indian Ocean Territory',
 'IR': 'Iran',
 'IS': 'Israel',
 'IT': 'Italy',
 'IV': 'Ivory Coast',
 'IZ': 'Iraq',
 'JA': 'Japan',
 'JE': 'Jersey',
 'JM': 'Jamaica',
 'JO': 'Jordan',
 'KE': 'Kenya',
 'KG': 'Kyrgyzstan',
 'KN': 'North Korea',
 'KR': 'Kiribati',
 'KS': 'South Korea',
 'KT': 'Christmas Island',
 'KU': 'Kuwait',
 'KV': 'Kosovo',
 'KZ': 'Kazakhstan',
 'LA': 'Laos',
 'LE': 'Lebanon',
 'LG': 'Latvia',
 'LH': 'Lithuania',
 'LI': 'Liberia',
 'LO': 'Slovakia',
 'LS': 'Liechtenstein',
 'LT': 'Lesotho',
 'LU': 'Luxembourg',
 'LY': 'Libya',
 'MA': 'Madagascar',
 'MB': 'Martinique',
 'MC': 'Macao',
 'MD': 'Moldova',
 'MF': 'Mayotte',
 'MG': 'Mongolia',
 'MH': 'Montserrat',
 'MI': 'Malawi',
 'MJ': 'Montenegro',
 'MK': 'North Macedonia',
 'ML': 'Mali',
 'MN': 'Monaco',
 'MO': 'Morocco',
 'MP': 'Mauritius',
 'MR': 'Mauritania',
 'MT': 'Malta',
 'MU': 'Oman',
 'MV': 'Maldives',
 'MX': 'Mexico',
 'MY': 'Malaysia',
 'MZ': 'Mozambique',
 'NC': 'New Caledonia',
 'NE': 'Niue',
 'NF': 'Norfolk Island',
 'NG': 'Niger',
 'NH': 'Vanuatu',
 'NI': 'Nigeria',
 'NL': 'Netherlands',
 'NN': 'Sint Maarten',
 'NO': 'Norway',
 'NP': 'Nepal',
 'NR': 'Nauru',
 'NS': 'Suriname',
 'NU': 'Nicaragua',
 'NZ': 'New Zealand',
 'OD': 'South Sudan',
 'PA': 'Paraguay',
 'PC': 'Pitcairn Islands',
 'PE': 'Peru',
 'PK': 'Pakistan',
 'PL': 'Poland',
 'PM': 'Panama',
 'PO': 'Portugal',
 'PP': 'Papua New Guinea',
 'PS': 'Palau',
 'PU': 'Guinea-Bissau',
 'QA': 'Qatar',
 'RE': 'Réunion',
 'RI': 'Serbia',
 'RM': 'Marshall Islands',
 'RN': 'Saint Martin',
 'RO': 'Romania',
 'RP': 'Philippines',
 'RQ': 'Puerto Rico',
 'RS': 'Russia',
 'RW': 'Rwanda',
 'SA': 'Saudi Arabia',
 'SB': 'Saint Pierre and Miquelon',
 'SC': 'St Kitts and Nevis',
 'SE': 'Seychelles',
 'SF': 'South Africa',
 'SG': 'Senegal',
 'SH': 'Saint Helena',
 'SI': 'Slovenia',
 'SL': 'Sierra Leone',
 'SM': 'San Marino',
 'SN': 'Singapore',
 'SO': 'Somalia',
 'SP': 'Spain',
 'ST': 'Saint Lucia',
 'SU': 'Sudan',
 'SV': 'Svalbard and Jan Mayen',
 'SW': 'Sweden',
 'SX': 'South Georgia and South Sandwich Islands',
 'SY': 'Syria',
 'SZ': 'Switzerland',
 'TB': 'Saint Barthélemy',
 'TD': 'Trinidad and Tobago',
 'TH': 'Thailand',
 'TI': 'Tajikistan',
 'TK': 'Turks and Caicos Islands',
 'TL': 'Tokelau',
 'TN': 'Tonga',
 'TO': 'Togo',
 'TP': 'São Tomé and Príncipe',
 'TS': 'Tunisia',
 'TT': 'Timor-Leste',
 'TU': 'Turkey',
 'TV': 'Tuvalu',
 'TW': 'Taiwan',
 'TX': 'Turkmenistan',
 'TZ': 'Tanzania',
 'UC': 'Curaçao',
 'UG': 'Uganda',
 'UK': 'United Kingdom',
 'UP': 'Ukraine',
 'US': 'United States',
 'UV': 'Burkina Faso',
 'UY': 'Uruguay',
 'UZ': 'Uzbekistan',
 'VC': 'St Vincent and Grenadines',
 'VE': 'Venezuela',
 'VI': 'British Virgin Islands',
 'VM': 'Vietnam',
 'VQ': 'U.S. Virgin Islands',
 'VT': 'Vatican City',
 'WA': 'Namibia',
 'WE': 'Palestine',
 'WF': 'Wallis and Futuna',
 'WI': 'Western Sahara',
 'WS': 'Samoa',
 'WZ': 'Eswatini',
 'YM': 'Yemen',
 'ZA': 'Zambia',
 'ZI': 'Zimbabwe'}

def create_country_folder(current_directory,csvfile):
    final_directory = os.path.join(current_directory, r''+csvfile)
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    return final_directory


def filter_by_country(df, country_col_name, current_directory, csvfile):

    # checking geo
    if df[df[country_col_name].isin(list(geo_dict.keys()))].shape[0] >0:
        df['COUNTRY2'] = df[country_col_name].map(geo_dict).fillna(df[country_col_name])

    if 'COUNTRY2' in df.columns:
        df_country_grouped = df.groupby('COUNTRY2')
        countries = df['COUNTRY2'].unique()
        print('----------- geo code countries in ' + csvfile + ' file updated-----------')
    else:
        df_country_grouped = df.groupby(country_col_name)
        countries = df[country_col_name].unique()

    final_directory = create_country_folder(current_directory, csvfile[0:-4])
    for country in countries:
        if '.' not in  country:
            df_country_grouped.get_group(country).to_csv(final_directory + '/' + country + '.csv', index=None, header=True)
    




def DirctoryPathToGeo(current_directory):
    # current_directory = os.getcwd()

    # wanted_list = ['EMAIL','NAME','FIRST NAME','LAST NAME','COUNTRY','NUMBER','SOURCE']
    wanted_list = ['EMAIL','Email', 'NAME','Name', 'FIRST NAME','Fname', 'LAST NAME','Lname','COUNTRY','Country','NUMBER','Number','SOURCE','Source']

    i =1
    for csvfile in os.listdir(current_directory):
        if csvfile.endswith(".csv"):
            try:
                df = pd.read_csv(current_directory + '/' + csvfile, encoding="ISO-8859-1", error_bad_lines=False, dtype=str)
                df.columns = df.columns.str.strip()
                flag = 'green'
            except:
                print('Problem reading '+csvfile + ' file')
                s = 'splitting NAME and filtering ' + csvfile + ' file: ' + str(i)
                yield s
                flag = 'red'

            if flag == 'green':
                wanted_columns_list = []
                if 'COUNTRY' in df.columns:
                    country_col_name = 'COUNTRY'
                if 'Country' in df.columns:
                    country_col_name = 'Country'

                if ('COUNTRY' in df.columns) or ('Country' in df.columns):
                    for column in df.columns:
                        if column in wanted_list:
                            wanted_columns_list.append(column)

                    df = df[wanted_columns_list]
                    df = df[df[country_col_name].notna()]
                    df = df[~df[country_col_name].str.isnumeric()]


                    if 'NAME' in df.columns:
                        name_col_name = 'NAME'
                    if 'Name' in df.columns:
                        name_col_name = 'Name'

                    if ('NAME' in df.columns) or ('Name' in df.columns):
                        # split NAME column to FIRST NAME and LAST NAME
                        print('splitting NAME and filtering ' + csvfile + ' file: ' + str(i))
                        s = 'splitting NAME and filtering ' + csvfile + ' file: ' + str(i)
                        yield s

                        try:
                            df[['Fname', 'Lname']] = df[name_col_name].str.split(' ', 1, expand=True)
                            df = df.drop(columns=[name_col_name])
                        except:
                            df.rename({name_col_name:'Fname'},axis=1, inplace=True)
                        df = df.drop(columns=[name_col_name])


                    print('filtering ' + csvfile + ' file: ' + str(i))
                    s = 'filtering ' + csvfile + ' file: ' + str(i)
                    yield s

                    filter_by_country(df, country_col_name, current_directory, csvfile)
                    print('Done')
                    yield s
                    s = 'Done'
                    yield s
                    print('===========================================================================================')
                    s = '==========================================================================================='
                    yield s
                    i = i + 1

                else:
                    print('columns in ' + csvfile + ' file does not have country')
                    s = 'columns in ' + csvfile + ' file does not have country'
                    yield s
                    print('===========================================================================================')
                    s = '==========================================================================================='
                    yield s

    print('program has finished execution')
    s = 'program has finished execution'
    yield s