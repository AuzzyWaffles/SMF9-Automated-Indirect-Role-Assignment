import pandas as pd
import os


class UncompliantFinder:
    def __init__(self):
        self.file_name = 'Processing Compliance.xlsm'
        self.desktop_path = os.path.expanduser('~\\Desktop')
        self.file_path = os.path.join(self.desktop_path, self.file_name)

    def get_uncompliant_processors(self):
        df = pd.read_excel(self.file_path, sheet_name='Processing Compliance')

        df.loc[0, 'Compliance'] = 0
        pd.to_numeric(df['Compliance'])

        uncompliant_rows = df[df['Compliance'] > 0]
        uncompliant_processors = uncompliant_rows['Unnamed: 1']
        uncompliant_processors = {associate for associate in uncompliant_processors}

        return uncompliant_processors
