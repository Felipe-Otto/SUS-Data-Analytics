

import pandas as pd

pd.options.display.max_columns = None

class DataUtils:
    def __init__(self):
        pass


    def create_dataframe(self, path):
        pd.set_option('display.width', 1000)
        datas = pd.read_csv(f'{path}', encoding='latin1', low_memory=False)
        print('\033[92mDataframe created based on the SUS data released by SINAN in CSV format:\033[0m')
        print(datas)
        self.countdown(15)
        self.get_dataframe_columns(datas)

    def get_dataframe_columns(self, datas):
        datas_columns = datas.columns.tolist()
        print('\n\033[92mThese are the columns of the dataframe:\033[0m')
        self.format_and_print_list(datas_columns)
        self.countdown(15)
        self.delete_dataframe_columns(datas, datas_columns)

    def delete_dataframe_columns(self, datas, datas_columns):
        columns_to_maintain = datas_columns[2:]
        print(f'\n\033[92mWe will exclude these two columns: \033[0m')
        self.format_and_print_list(columns_to_maintain)
        datas = datas[columns_to_maintain].reset_index(drop=True)
        print('\n\033[92mThe dataframe will look like this:\033[0m')
        print(datas)
        self.countdown(5)
        self.recode_columns_yes_no_values(datas)


    def recode_columns_yes_no_values(self, datas):
        columns_yes_no_values = ['MCLI_LOCAL', 'CLI_DOR', 'CLI_EDEMA', 'CLI_EQUIMO',
                                  'CLI_NECROS', 'CLI_LOCAL_', 'MCLI_SIST', 'CLI_NEURO',
                                  'CLI_HEMORR', 'CLI_VAGAIS', 'CLI_MIOLIT', 'CLI_RENAL',
                                  'CLI_OUTR_2', 'CON_SOROTE', 'COM_LOC', 'COM_SECUND',
                                  'COM_NECROS', 'COM_COMPOR',  'COM_DEFICT', 'COM_APUTAC',
                                  'COM_SISTEM', 'COM_RENAL',  'COM_EDEMA', 'COM_SEPTIC',
                                  'COM_CHOQUE', 'DOENCA_TRA']
        print('\n\033[92mAccording to the SINAN data dictionary, these are the columns of the Dataframe that contains\n\'Yes\', \'No\' and \'Unknown\' values referred consecutively as 1, 2 and 9:\033[0m')
        self.format_and_print_list(columns_yes_no_values)
        self.countdown(10)
        column_values = {1: 'Yes', 2: 'No', 9: 'Unknown'}
        for column in columns_yes_no_values:
            datas[column] = datas[column].replace(column_values)
        print('\n\033[92mAfter modifying those values, these columns will look like this:\033[0m')
        print(datas[columns_yes_no_values])
        self.countdown(15)
        self.recode_columns_date_values(datas)

    def recode_columns_date_values(self, datas):
        columns_date_values = ['DT_NOTIFIC', 'DT_SIN_PRI', 'DT_INVEST', 'DT_OBITO',
                               'DT_ENCERRA', 'DT_DIGITA', 'ANT_DT_ACI']
        print('\n\033[92mAccording to the SINAN data dictionary, these are the columns of the Dataframe that contains date values:\033[0m')
        self.format_and_print_list(columns_date_values)
        print('\033[90mTransforming data...\033[0m')
        for column in columns_date_values:
            datas[column] = pd.to_datetime(datas[column], format='%Y%m%d', errors='coerce').dt.strftime('%m/%d/%Y')
        print('\n\033[92mAfter modifying those values, these date columns will looks like this:\033[0m')
        print(datas[columns_date_values])
        self.countdown(15)
        self.recode_columns_foreign_values(datas)

    def recode_columns_foreign_values(self, datas):
        columns_foreign_values = []
        replacement_dict = {'ANT_TEMPO_':
                                {1: '0 - 1h', 2: '1 - 3h', 3: '3 - 6h', 4: '6 - 12h', 5: '12 e 24h', 6: '24 and +h', 9: 'Unknown'},
                            'ANT_LOCA_1':
                                {1: 'Head', 2: 'Arm', 3: 'Forearm', 4: 'Hand', 5: 'Finger of Hand', 6: 'Trunk', 7: 'Thigh', 8: 'Leg', 9: 'Foot', 10: 'Toe', 99: 'Unknown'},
                            'CLI_TEMPO_':
                                {1: 'Normal', 2: 'Altered', 9: 'Not Performed'},
                            'TP_ACIDENT':
                                {1: 'Snake', 2: 'Spider', 3: 'Scorpion', 4: 'Caterpillar', 5: 'Bee', 6: 'Others', 9: 'Unknown'},
                            'ANI_SERPEN':
                                {1: 'Viper', 2: 'Crotalid', 3: 'Elapid', 4: 'Laquetic', 5: 'Non-venomous Snake', 9: 'Unknown'},
                            'ANI_ARANHA':
                                {1: 'Phoneutrism', 2: 'Loxoscelism', 3: 'Latrodectism', 4: 'Other Spider', 9: 'Unknown'},
                            'ANI_LAGART':
                                {1: 'Lonomia', 2: 'Other Caterpillar', 9: 'Unknown'},
                            'TRA_CLASSI':
                                {1: 'Mild', 2: 'Moderate', 3: 'Severe', 9: 'Unknown'},
                            'EVOLUCAO':
                                {1: 'Cure', 2: 'Death by Accidental Poisoning by Venomous Animals', 3: 'Death by Other Causes', 9: 'Unknown'},
                            'CS_GESTANT':
                                {1: '1st Trimester', 2: '2nd Trimester', 3: '3rd Trimester', 4: 'Unknown Gestational Age', 5: 'No', 6: 'Not Applicable', 9: 'Unknown'},
                            'CS_RACA':
                                {1: 'White', 2: 'Black', 3: 'Yellow', 4: 'Brown', 5: 'Indigenous', 9: 'Unknown'},
                            'CS_ESCOL_N':
                                {1: '1st to 4th Incomplete Grade of Elementary School', 2: '4th Complete Grade of Elementary School',
                                 3: '5th to 8th Incomplete Grade of Elementary School',
                                 4: 'Complete Elementary School',
                                 5: 'Incomplete High School',
                                 6: 'Complete High School',
                                 7: 'Incomplete Higher Education', 8: 'Complete Higher Education', 9: 'Unknown', 10: 'Not Applicable'}}
        for key in replacement_dict:
            columns_foreign_values.append(key)
        print('\n\033[92mAccording to the SINAN data dictionary, these are the columns of the Dataframe that contains specific values related by codes:\033[0m')
        self.format_and_print_list(columns_foreign_values)
        for key in replacement_dict:
            datas[key] = datas[key].replace(replacement_dict[key])
        print('\n\033[92mAfter modifying those values, these specific columns will look like this:\033[0m')
        print(datas[columns_foreign_values])
        self.countdown(15)
        self.recode_column_age_values(datas)


    def recode_column_age_values(self, datas):
        ages = []
        print('\n\033[92mAccording to SINAN, the age of patients is stored in the column \'NU_IDADE_N\' and its values are '
              'defined based on the first digit (1: Hours, 2: Days, 3: Months, and 4: Years). \nTherefore, the value 4018 '
              'refers to someone who is 18 years old, while the value 3010 refers to someone who is 10 months old.:\033[0m')
        for age in datas['NU_IDADE_N']:
            if age > 4000:
                ages.append(age - 4000)
            else:
                ages.append(0)
        datas['NU_IDADE_N'] = ages
        print('\n\033[92mAfter modifying those values, these age column will look like this:\033[0m')
        print(f'  NU_IDADE_N\n{datas["NU_IDADE_N"]}')
        self.countdown(15)
        self.recode_columns_municipalities(datas)

    def recode_columns_municipalities(self, datas):
        columns_municipalities_values = ['ID_MUNICIP', 'ID_MN_RESI', 'ANT_MUNIC_']
        print('\n\033[92mAccording to the SINAN data dictionary, these are the columns of the Dataframe that contains date values:\033[0m')
        self.format_and_print_list(columns_municipalities_values)
        municipalities = self.create_municipalities_dataframe()
        municipalities = self.create_municipalities_dictionary(municipalities)
        for column in columns_municipalities_values:
            datas[column] = datas[column].map(municipalities)
        print('\n\033[92mAfter recoding the values in these municipalities columns type, our DataFrame looks like this:\033[0m')
        print(datas[columns_municipalities_values])
        self.recode_column_occupations(datas)


    def create_municipalities_dataframe(self):
        municipalities_repository = 'https://raw.githubusercontent.com/Felipe-Otto/SUS-Data-Analytics/main/CSV/Municipality.csv'
        print('\n\033[92mIt is necessary to create a DataFrame with this data so that we can relate them with foreign keys.'
              f'\nWe will use the following repository to extract this data:\n{municipalities_repository}\033[0m')
        municipalities = pd.read_csv(municipalities_repository)
        print('\n\033[92mMunicipalities DataFrame looks like this:\033[0m')
        print(municipalities)
        self.countdown(15)
        print('\n\033[92mSome adjustments are needed. The \'Population\' column isn\'t necessary, and it is necessary '
              'to index the \'Key\' column so that it can be used for key relationships...\033[0m')
        columns_to_maintain = ['Key', 'Municipality']
        print('\033[90mModifying DataFrame...\033[0m')
        municipalities = municipalities[columns_to_maintain].set_index('Key')
        print('\033[92mAfter these modifications, the Municipalities DataFrame will look like this:\033[0m')
        print(municipalities)
        self.countdown(15)
        return municipalities


    def create_municipalities_dictionary(self, municipalities):
        print('\n\033[92mTo finalize this process, it is necessary to transform this DataFrame into a dictionary of data!\033[0m')
        print('\033[90mCreating dictionary...\033[0m')
        municipalities = municipalities.to_dict()['Municipality']
        return municipalities


    def recode_column_occupations(self, datas):
        print('\n\033[92mAccording to the SINAN data dictionary, this are the column of the Dataframe that contains occupations values:\033[0m')
        occupations = self.create_occupations_dataframe()
        occupations = self.create_occupations_dictionary(occupations)
        datas['ID_OCUPA_N'] = datas['ID_OCUPA_N'].map(occupations)
        print('\n\033[92mAfter recoding the values in these occupation column type, our DataFrame looks like this:\033[0m')
        print(f'    ID_OCUPA_N\n{datas["ID_OCUPA_N"]}')
        self.countdown(15)
        self.recode_columns_federal_units(datas)

    def create_occupations_dictionary(self, occupations):
        print('\n\033[92mTo finalize this process, it is necessary to transform this DataFrame into a dictionary of data!\033[0m')
        print('\033[90mCreating dictionary...\033[0m')
        occupations = occupations.to_dict()['Occupations']
        return occupations


    def create_occupations_dataframe(self):
        occupations_repository = 'https://raw.githubusercontent.com/Felipe-Otto/SUS-Data-Analytics/main/CSV/Occupation.csv'
        print('\n\033[92mIt is necessary to create a DataFrame with this data so that we can relate them with foreign keys.'
              f'\nWe will use the following repository to extract this data:\n{occupations_repository}\033[0m')
        occupations = pd.read_csv(occupations_repository)
        print('\n\033[92mOccupations DataFrame looks like this:\033[0m')
        print(occupations)
        print('\n\033[92mSome adjustments are needed. It is necessary to index the \'Key\' column so that it can be used for key relationships...\033[0m')
        occupations = occupations.set_index('Key')
        print('\033[92mAfter these modifications, the Occupations DataFrame will look like this:\033[0m')
        print(occupations)
        self.countdown(15)
        return occupations


    def recode_columns_federal_units(self, datas):
        print('\n\033[92mAccording to the SINAN data dictionary, these are the columns of the Dataframe that contains federal units values:\033[0m')
        columns_federal_units_values = ['SG_UF', 'SG_UF_NOT', 'ANT_UF']
        self.format_and_print_list(columns_federal_units_values)
        federal_units = self.create_federal_units_dataframe()
        federal_units = self.create_federal_units_dictionary(federal_units)
        for column in columns_federal_units_values:
            datas[column] = datas[column].map(federal_units)
        print('\n\033[92mAfter recoding the values in these federal unity columns type, our DataFrame looks like this:\033[0m')
        print(datas[columns_federal_units_values])
        self.countdown(15)
        self.rename_dataframe_columns(datas)


    def create_federal_units_dictionary(self, federal_units):
        print('\n\033[92mTo finalize this process, it is necessary to transform this DataFrame into a dictionary of data!\033[0m')
        print('\033[90mCreating dictionary...\033[0m')
        federal_units = federal_units.to_dict()['UF']
        return federal_units


    def create_federal_units_dataframe(self):
        federal_units_repository = 'https://raw.githubusercontent.com/Felipe-Otto/SUS-Data-Analytics/main/CSV/UF.csv'
        self.countdown(15)
        print('\n\033[92mIt is necessary to create a DataFrame with this data so that we can relate them with foreign keys.'
              f'\nWe will use the following repository to extract this data:\n{federal_units_repository}\033[0m')
        federal_units = pd.read_csv(federal_units_repository)
        print('\n\033[92mOur new dataframe looks like this:\033[0m')
        print(federal_units)
        print('\n\033[92mSome adjustments are needed. The \'Population\' and \'Federal Unity\' columns aren\'t necessary, and it is necessary '
              'to index the \'Key\' column so that it can be used for key relationships...\033[0m')
        columns_to_maintain = ['Key', 'UF']
        federal_units = federal_units[columns_to_maintain].set_index('Key')
        print('\033[92mAfter these modifications, the Federal Units DataFrame will look like this:\033[0m')
        print(federal_units)
        self.countdown(15)
        return federal_units


    def rename_dataframe_columns(self, datas):
        columns_renamed = {'DT_NOTIFIC': 'Notification Date',
                           'SEM_NOT': 'Week of Notification',
                           'NU_ANO': 'Year of Notification',
                           'SG_UF_NOT': 'Notification UF',
                           'ID_MUNICIP': 'Notification Municipality',
                           'ID_REGIONA': 'Notification Regional ID',
                           'DT_SIN_PRI': 'Date of First Symptoms',
                           'SEM_PRI': 'Week of First Symptoms',
                           'ANO_NASC': 'Year of Birth',
                           'NU_IDADE_N': 'Age',
                           'CS_SEXO': 'Gender',
                           'CS_GESTANT': 'Pregnancy',
                           'CS_RACA': 'Race',
                           'CS_ESCOL_N': 'Education',
                           'SG_UF': 'UF',
                           'ID_MN_RESI': 'Residence Municipality',
                           'ID_RG_RESI': 'Residence Municipality ID',
                           'ID_PAIS': 'Country (If Resident Outside Brazil)',
                           'DT_INVEST': 'Investigation Date',
                           'ID_OCUPA_N': 'Occupation',
                           'ANT_DT_ACI': 'Accident Date',
                           'ANT_UF': 'UF',
                           'ANT_MUNIC_': 'Accident Occurrence Municipality',
                           'ANT_LOCALI': 'Accident Occurrence Locality',
                           'ANT_TEMPO_': 'Time Elapsed Bite/First Aid',
                           'ANT_LOCA_1': 'Bite Location',
                           'MCLI_LOCAL': 'Local Manifestations',
                           'CLI_DOR': 'Pain',
                           'CLI_EDEMA': 'Edema',
                           'CLI_EQUIMO': 'Ecchymosis',
                           'CLI_NECROS': 'Necrosis',
                           'CLI_LOCAL_': 'Others Manifestations',
                           'CLI_LOCA_1': 'In Case of Others Manifestations (Specify)',
                           'MCLI_SIST': 'Systemic Manifestations',
                           'CLI_NEURO': 'Neuroparalytic (Ptosis, Blurred Vision)',
                           'CLI_HEMORR': 'Hemorrhagic (Gingival Bleeding, Other Bleedings)',
                           'CLI_VAGAIS': 'Vagal (Vomiting/Diarrhea)',
                           'CLI_MIOLIT': 'Myolytic/Hemolytic (Myalgia, Anemia, Dark Urine)',
                           'CLI_RENAL': 'Renal (Oliguria/Anuria)',
                           'CLI_OUTR_2': 'Others Systemic Manifestations',
                           'CLI_OUTR_3': 'In Case of Others Systemic Manifestations (Specify)',
                           'CLI_TEMPO_': 'Coagulation Time',
                           'TP_ACIDENT': 'Accident Type',
                           'ANI_TIPO_1': 'In Case of Others, Specify',
                           'ANI_SERPEN': 'Snake - Accident Type',
                           'ANI_ARANHA': 'Spider - Accident Type',
                           'ANI_LAGART': 'Caterpillar - Accident Type',
                           'TRA_CLASSI': 'Case Classification',
                           'CON_SOROTE': 'Serotherapy',
                           'NU_AMPOLAS': 'Number of SAB Ampoules',
                           'NU_AMPOL_1': 'Number of SAC Ampoules',
                           'NU_AMPOL_8': 'Number of SAAr Ampoules',
                           'NU_AMPOL_6': 'Number of SABL Ampoules',
                           'NU_AMPOL_4': 'Number of SAEL Ampoules',
                           'NU_AMPO_7': 'Number of SALox Ampoules',
                           'NU_AMPO_5': 'Number of SABC Ampoules',
                           'NU_AMPOL_9': 'Number of ASAEsc Ampoules',
                           'NU_AMPOL_3': 'Number of SALon Ampoules',
                           'COM_LOC': 'Local Complications',
                           'COM_SECUND': 'Secondary Infection',
                           'COM_NECROS': 'Extensive Necrosis',
                           'COM_COMPOR': 'Behavioral Syndrome',
                           'COM_DEFICT': 'Functional Deficit',
                           'COM_APUTAC': 'Amputation',
                           'COM_SISTEM': 'Systemic Complications',
                           'COM_RENAL': 'Renal Insufficiency',
                           'COM_EDEMA': 'Respiratory Insufficiency/Acute Pulmonary Edema',
                           'COM_SEPTIC': 'Septicemia',
                           'COM_CHOQUE': 'Shock',
                           'DOENCA_TRA': 'Work-Related Accident',
                           'EVOLUCAO': 'Case Outcome',
                           'DT_OBITO': 'Date of Death',
                           'DT_ENCERRA': 'Closure Date',
                           'DT_DIGITA': 'Data Entry Date'}
        print('\n\033[92mWith the transformations made, it is now necessary to change the column names to more meaningful names for the analysis to be viable.\033[0m')
        datas = datas.rename(columns=columns_renamed)
        print('\n\033[92mThis is the final result of the dataframe:\033[0m')
        print(datas)
        self.countdown(15)
        self.create_csv_from_dataframe(datas)


    def create_csv_from_dataframe(self, datas):
        print('\033[92mTo conclude, the dataframe will be exported to a file called \'sinan_data_transformed.csv\' in the data_analysis package. This file can be exported to other data visualization tools, enabling data analysis.\033[0m')
        print('\033[90mCreating file...\033[0m')
        datas.to_csv('../data_analysis/sinan_data_transformed.csv', index=False, sep=';')
        print('\033[92mProgram successfully completed!\033[0m')


    def countdown(self, seconds):
        from sys import stdout
        from time import sleep
        for i in range(seconds, 0, -1):
            stdout.write(f'\033[91mProgram will resume in {i} seconds...\033[0m')
            stdout.flush()
            sleep(1)
            stdout.write('\r')
        print('\033[90mCountdown completed. Resuming the program...\033[0m')

    def format_and_print_list(self, list):
        for i, item in enumerate(list, 1):
            if i < (len(list) - 1):
                if i % 5 == 0:
                    print(f'{item},', end='\n')
                else:
                    print(f'{item},', end=' ')
            else:
                if i == (len(list) - 1):
                    print(f'{item} and ', end='')
                else:
                    print(item)
