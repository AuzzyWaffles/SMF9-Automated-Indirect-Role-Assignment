import os
import pandas as pd

file_name = 'Processing Compliance.xlsm'
desktop_path = os.path.expanduser('~\\Desktop')
file_path = os.path.join(desktop_path, file_name)


def get_uncompliant_processors():
    df = pd.read_excel(file_path, sheet_name='Processing Compliance')

    df.loc[0, 'Compliance'] = 0
    pd.to_numeric(df['Compliance'])

    uncompliant_rows = df[df['Compliance'] > 0]
    uncompliant_processors = uncompliant_rows['Unnamed: 1']
    uncompliant_processors = {associate for associate in uncompliant_processors}

    return uncompliant_processors
